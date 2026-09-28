import argparse
import json
from dataclasses import asdict
from pathlib import Path

from dotenv import load_dotenv

from probe_app.backup import KEY_ENV, backup, restore
from probe_app.config import INSTRUMENT_DIR, PREREG_PATH, current_config, freeze, load_models


def tablet_origin(host: str, port: int, tls: bool) -> str | None:
    """The address the expert's tablet must use; None when the console's own origin works (loopback)."""
    if host in ("127.0.0.1", "localhost", "::1"):
        return None
    if host in ("0.0.0.0", "::"):
        import socket
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            try:
                s.connect(("192.0.2.1", 9))  # UDP connect sends nothing; it only picks the outgoing interface
                host = s.getsockname()[0]
            except OSError:
                return None
    return f"{'https' if tls else 'http'}://{host}:{port}"


def main(argv: list[str] | None = None) -> None:
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
    bk = sub.add_parser("backup", help="write an encrypted, verified copy of session directories to --dest")
    bk.add_argument("sessions", nargs="*", help="session IDs under --root (default: every session)")
    bk.add_argument("--root", type=Path, default=INSTRUMENT_DIR.parent / "sessions")
    bk.add_argument("--dest", type=Path, required=True)
    bk.add_argument("--key-env", default=KEY_ENV, help="environment variable holding the passphrase")
    rs = sub.add_parser("restore", help="decrypt a backup into --out and check every file against its manifest")
    rs.add_argument("archive", type=Path)
    rs.add_argument("--out", type=Path, required=True)
    rs.add_argument("--key-env", default=KEY_ENV, help="environment variable holding the passphrase")
    args = parser.parse_args(argv)
    if args.cmd not in ("backup", "restore"):
        # The backup passphrase must come from the shell, never from a file in the repository.
        load_dotenv(INSTRUMENT_DIR / ".env")

    if args.cmd == "backup":
        for out, n in backup(args.root, args.dest, args.sessions, args.key_env):
            print(f"{out.name}: {n} files, decrypted and verified -> {out}")
    elif args.cmd == "restore":
        print(f"restored and verified: {restore(args.archive, args.out, args.key_env)}")
    elif args.cmd == "hashes":
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
        origin = tablet_origin(args.host, args.port, tls=bool(args.ssl_certfile))
        app = create_app(args.root, Deps(make_transcriber(), backends), expert_origin=origin)
        if origin:
            print(f"Tablet: {origin}/expert (the certificate must cover this address)")
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
