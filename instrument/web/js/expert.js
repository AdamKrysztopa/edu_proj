const $ = (id) => document.getElementById(id);
let sid = new URLSearchParams(location.search).get("session") || "";
let mic = null, live = null, answerRec = null, answerChunks = [], recStart = 0, strokes = [];
let view = null, lastKey = "", busy = false, pending = null;

async function api(path, opts = {}) {
  const r = await fetch(`/api/sessions/${sid}${path}`, opts);
  if (!r.ok) throw new Error(`${r.status}: ${await r.text()}`);
  return r.json();
}

function show(id) {
  for (const s of document.querySelectorAll("main > section")) s.hidden = s.id !== id;
}

const MIME = "audio/webm;codecs=opus";

async function sendChunk(rec, seq, blob) {
  const url = `/api/sessions/${sid}/recording/chunk?stream=${rec.stream}&part=${rec.part}&seq=${seq}`;
  // Never give up on a network or 5xx error: a missing chunk loses audio until a new part starts.
  for (let attempt = 1; ; attempt++) {
    try {
      const r = await fetch(url, { method: "POST", headers: { "Content-Type": "application/octet-stream" }, body: blob });
      if (r.ok) {
        if (attempt > 1) $("status").textContent = "";
        if ((await r.json()).gap) restartStream(rec);
        return;
      }
      if (r.status < 500 && r.status !== 408 && r.status !== 429) {
        $("status").textContent = `Audio chunk refused (${r.status}). Tell the researcher.`;
        return;
      }
    } catch (err) { /* network: retry */ }
    $("status").textContent = "Audio upload retrying…";
    await sleep(1000 * Math.min(attempt, 5));
  }
}

const sleep = (ms) => new Promise((res) => setTimeout(res, ms));

// Bumped by every stop and every fresh start, so a restart that resolves late cannot claim `live`.
let epoch = 0;

async function startStream(streamName, t0 = null, mine = ++epoch) {
  const r = await fetch(`/api/sessions/${sid}/recording/start`, {
    method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ stream: streamName }) });
  if (mine !== epoch) return;
  if (!r.ok) { $("status").textContent = `Could not start recording (${r.status}). Tell the researcher.`; return; }
  const rec = { stream: streamName, part: (await r.json()).part, seq: 0, uploads: Promise.resolve() };
  if (mine !== epoch) return;
  rec.recorder = new MediaRecorder(mic, { mimeType: MIME });
  rec.recorder.ondataavailable = (e) => {
    if (!e.data.size) return;
    const seq = rec.seq++;
    rec.uploads = rec.uploads.then(() => sendChunk(rec, seq, e.data));
  };
  rec.recorder.start(1000);
  recStart = t0 ?? performance.now();
  live = rec;
}

// A new part carries its own server start time, so audio after a gap stays aligned; strokes keep recStart.
async function restartStream(rec) {
  if (live !== rec) return;
  live = null;
  rec.recorder.ondataavailable = null;
  rec.recorder.stop();
  const t0 = recStart, mine = epoch;
  for (let attempt = 1; mine === epoch; attempt++) {
    try {
      await startStream(rec.stream, t0, mine);
      return;
    } catch (err) { /* network: retry */ }
    $("status").textContent = "Audio restarting… Tell the researcher if this stays.";
    await sleep(1000 * Math.min(attempt, 5));
  }
}

function stopStream() {
  epoch++;
  const rec = live;
  live = null;
  if (!rec) return Promise.resolve();
  return new Promise((resolve) => {
    rec.recorder.onstop = () => resolve(rec.uploads);
    rec.recorder.stop();
  });
}

function startAnswer() {
  answerChunks = [];
  answerRec = new MediaRecorder(mic, { mimeType: MIME });
  answerRec.ondataavailable = (e) => answerChunks.push(e.data);
  answerRec.start();
}

function stopAnswer() {
  return new Promise((resolve) => {
    answerRec.onstop = () => resolve(new Blob(answerChunks, { type: "audio/webm" }));
    answerRec.stop();
    answerRec = null;
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
  mic = await navigator.mediaDevices.getUserMedia({ audio: true });
  show("waiting");
  poll();
};

$("doneBtn").onclick = async () => {
  if (busy) return;
  busy = true; $("doneBtn").disabled = true;
  await stopStream();
  const snapshot = await new Promise((r) => pad.toBlob(r, "image/png"));
  const form = new FormData();
  form.append("snapshot", snapshot, "snapshot.png");
  form.append("strokes", JSON.stringify(strokes));
  await send(`/think-aloud/${view.current_problem}/end`, form, "Saving…");
  busy = false; $("doneBtn").disabled = false;
};

$("talkBtn").onclick = async () => {
  if (answerRec) {
    $("talkBtn").disabled = true;
    const audio = await stopAnswer();
    const form = new FormData();
    form.append("audio", audio, "answer.webm");
    form.append("turn_index", String(view.expected_answer_index));
    await send("/probe/answer", form, "Listening to your answer…");
    $("talkBtn").textContent = "Start answer";
    $("talkBtn").disabled = false;
  } else {
    startAnswer();
    $("talkBtn").textContent = "Finish answer";
  }
};

function renderAnchor(anchor, textId, imgId) {
  $(textId).hidden = !(anchor && anchor.kind === "segments");
  $(imgId).hidden = !(anchor && anchor.kind === "canvas");
  if (anchor && anchor.kind === "segments") $(textId).textContent = anchor.text;
  if (anchor && anchor.kind === "canvas") $(imgId).src = anchor.image_url;
}

async function finishHumanProbe() {
  busy = true;
  await stopStream();
  await send("/probe/finalize", undefined, "Saving…");
  busy = false;
}

function render(s) {
  const key = `${s.phase}|${s.current_problem}|${s.current_set}`;
  const entering = key !== lastKey;
  lastKey = key;
  view = s;
  if (s.phase === "think_aloud") {
    if (entering) { resetPad(); $("problemText").textContent = s.problem_text; startStream(`think_${s.current_problem}`); }
    show("thinkaloud");
  } else if (s.phase === "probe" && s.arm === "ai") {
    show("probe");
    $("question").textContent = s.question || "One moment…";
    $("talkBtn").hidden = s.question === null;
    renderAnchor(s.anchor_view, "anchorText", "anchorImg");
  } else if (s.phase === "probe" && s.arm === "human") {
    if (entering) startStream(`probe_${s.current_set}`);
    show("human");
    renderAnchor(s.anchor_view, "humanText", "humanImg");
  } else if (s.phase === "probe_uploading") {
    if (entering && !busy) finishHumanProbe();
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
