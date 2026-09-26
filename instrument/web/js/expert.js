const $ = (id) => document.getElementById(id);
let sid = new URLSearchParams(location.search).get("session") || "";
let stream = null, recorder = null, chunks = [], recStart = 0, strokes = [];
let view = null, lastKey = "", busy = false, pending = null;

async function api(path, opts = {}) {
  const r = await fetch(`/api/sessions/${sid}${path}`, opts);
  if (!r.ok) throw new Error(`${r.status}: ${await r.text()}`);
  return r.json();
}

function show(id) {
  for (const s of document.querySelectorAll("main > section")) s.hidden = s.id !== id;
}

function startRecording() {
  chunks = [];
  recorder = new MediaRecorder(stream, { mimeType: "audio/webm;codecs=opus" });
  recorder.ondataavailable = (e) => chunks.push(e.data);
  recorder.start(1000);
  recStart = performance.now();
}

function stopRecording() {
  return new Promise((resolve) => {
    recorder.onstop = () => resolve(new Blob(chunks, { type: "audio/webm" }));
    recorder.stop();
  });
}

const pad = $("pad");
const ctx = pad.getContext("2d");
let stroke = null;

function resetPad() {
  ctx.fillStyle = "#fff";
  ctx.fillRect(0, 0, pad.width, pad.height);
  ctx.lineWidth = 3; ctx.lineCap = "round"; ctx.strokeStyle = "#111";
  strokes = [];
}

function point(e) {
  const r = pad.getBoundingClientRect();
  return [(e.clientX - r.left) * pad.width / r.width, (e.clientY - r.top) * pad.height / r.height,
          Math.round(performance.now() - recStart)];
}

pad.addEventListener("pointerdown", (e) => {
  pad.setPointerCapture(e.pointerId);
  const p = point(e);
  stroke = { points: [p] };
  ctx.beginPath(); ctx.moveTo(p[0], p[1]);
});
pad.addEventListener("pointermove", (e) => {
  if (!stroke) return;
  const p = point(e);
  stroke.points.push(p);
  ctx.lineTo(p[0], p[1]); ctx.stroke();
});
pad.addEventListener("pointerup", () => { if (stroke) strokes.push(stroke); stroke = null; });

async function send(path, form, label) {
  pending = { path, form, label };
  $("status").textContent = label;
  try {
    await api(path, { method: "POST", body: form });
    pending = null;
    $("status").textContent = "";
  } catch (err) {
    $("status").textContent = `Could not send (${err.message}). Tap to retry.`;
  }
}

$("status").addEventListener("click", () => { if (pending) send(pending.path, pending.form, pending.label); });

$("joinBtn").onclick = async () => {
  sid = sid || $("sid").value.trim();
  stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  show("waiting");
  poll();
};

$("doneBtn").onclick = async () => {
  if (busy) return;
  busy = true; $("doneBtn").disabled = true;
  const audio = await stopRecording();
  const snapshot = await new Promise((r) => pad.toBlob(r, "image/png"));
  const form = new FormData();
  form.append("audio", audio, "think.webm");
  form.append("snapshot", snapshot, "snapshot.png");
  form.append("strokes", JSON.stringify(strokes));
  await send(`/think-aloud/${view.current_problem}/end`, form, "Saving…");
  busy = false; $("doneBtn").disabled = false;
};

$("talkBtn").onclick = async () => {
  if (recorder && recorder.state === "recording") {
    $("talkBtn").disabled = true;
    const audio = await stopRecording();
    const form = new FormData();
    form.append("audio", audio, "answer.webm");
    form.append("turn_index", String(view.expected_answer_index));
    await send("/probe/answer", form, "Listening to your answer…");
    $("talkBtn").textContent = "Start answer";
    $("talkBtn").disabled = false;
  } else {
    startRecording();
    $("talkBtn").textContent = "Finish answer";
  }
};

function renderAnchor(anchor, textId, imgId) {
  $(textId).hidden = !(anchor && anchor.kind === "segments");
  $(imgId).hidden = !(anchor && anchor.kind === "canvas");
  if (anchor && anchor.kind === "segments") $(textId).textContent = anchor.text;
  if (anchor && anchor.kind === "canvas") $(imgId).src = anchor.image_url;
}

async function uploadHumanProbe(setId) {
  busy = true;
  const audio = await stopRecording();
  const form = new FormData();
  form.append("audio", audio, "probe.webm");
  await send(`/probe/${setId}/audio`, form, "Saving…");
  busy = false;
}

function render(s) {
  const key = `${s.phase}|${s.current_problem}|${s.current_set}`;
  const entering = key !== lastKey;
  lastKey = key;
  view = s;
  if (s.phase === "think_aloud") {
    if (entering) { resetPad(); $("problemText").textContent = s.problem_text; startRecording(); }
    show("thinkaloud");
  } else if (s.phase === "probe" && s.arm === "ai") {
    show("probe");
    $("question").textContent = s.question || "One moment…";
    $("talkBtn").hidden = s.question === null;
    renderAnchor(s.anchor_view, "anchorText", "anchorImg");
  } else if (s.phase === "probe" && s.arm === "human") {
    if (entering) startRecording();
    show("human");
    renderAnchor(s.anchor_view, "humanText", "humanImg");
  } else if (s.phase === "probe_uploading") {
    if (!busy && recorder && recorder.state === "recording") uploadHumanProbe(s.current_set);
  } else if (s.phase === "done") {
    show("done");
  } else {
    show("waiting");
  }
}

async function poll() {
  try { render(await api("/expert-view")); }
  catch (err) { $("status").textContent = err.message; }
  setTimeout(poll, 1000);
}
