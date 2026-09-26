import argparse
import json
from dataclasses import asdict
from pathlib import Path

from dotenv import load_dotenv

from probe_app.config import INSTRUMENT_DIR, PREREG_PATH, current_config, freeze, load_models


def main(argv: list[str] | None = None) -> None:
    load_dotenv(INSTRUMENT_DIR / ".env")
    parser = argparse.ArgumentParser(prog="probe-app")
    sub = parser.add_subparsers(dest="cmd", required=True)
    serve = sub.add_parser("serve", help="run the session app")
    serve.add_argument("--root", type=Path, default=INSTRUMENT_DIR.parent / "sessions")
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", type=int, default=8000)
    serve.add_argument("--ssl-certfile")
    serve.add_argument("--ssl-keyfile")
    sub.add_parser("hashes", help="print the current frozen configuration")
    tr = sub.add_parser("transcribe", help="transcribe one audio file, to compare transcribers in the pilot")
    tr.add_argument("audio", type=Path)
    tr.add_argument("--model", default=None, help="default: models.json transcriber; scribe_v2 or whisper-1")
    sub.add_parser("freeze", help="write the current configuration to prereg.json")
    sim = sub.add_parser("simulate", help="run a simulated AI-arm session against the real APIs")
    sim.add_argument("--root", type=Path, default=INSTRUMENT_DIR.parent / "sessions")
    sim.add_argument("--set-order", default="A,B")
    args = parser.parse_args(argv)

    if args.cmd == "hashes":
        print(json.dumps(asdict(current_config()), indent=2))
    elif args.cmd == "transcribe":
        from probe_app.trace import build_segments, render_transcript
        from probe_app.transcribe import make_transcriber

        raw = make_transcriber(args.model).transcribe(args.audio)
        print(render_transcript(build_segments("X", 0.0, raw)))
    elif args.cmd == "freeze":
        freeze(current_config(), PREREG_PATH)
        print(f"wrote {PREREG_PATH}")
    elif args.cmd == "serve":
        import uvicorn

        from probe_app.backends import make_backends
        from probe_app.server import create_app
        from probe_app.session import Deps
        from probe_app.transcribe import make_transcriber

        backends = make_backends(load_models())
        app = create_app(args.root, Deps(make_transcriber(), backends))
        uvicorn.run(app, host=args.host, port=args.port,
                    ssl_certfile=args.ssl_certfile, ssl_keyfile=args.ssl_keyfile)
    elif args.cmd == "simulate":
        from probe_app.backends import make_backend, make_backends
        from probe_app.session import Deps
        from probe_app.simulate import FixtureTranscriber, SimulatedExpert, run_simulation

        models = load_models()
        expert = SimulatedExpert(make_backend("simulated expert", models.simulated_expert))
        fixture = json.loads((INSTRUMENT_DIR / "problems" / "simulated_think_aloud.json").read_text())
        sid = run_simulation(args.root, Deps(FixtureTranscriber(fixture), make_backends(models)), expert,
                             args.set_order.split(","))
        print(f"simulated session: {args.root / sid}")
