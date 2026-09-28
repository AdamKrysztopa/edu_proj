const $ = (id) => document.getElementById(id);
let sid = new URLSearchParams(location.search).get("session");
let view = null;

async function call(path, body) {
  const opts = { method: "POST" };
  if (body !== undefined) { opts.headers = { "Content-Type": "application/json" }; opts.body = JSON.stringify(body); }
  const r = await fetch(`/api/sessions/${sid}${path}`, opts);
  if (!r.ok) { $("error").textContent = `${r.status}: ${await r.text()}`; return null; }
  $("error").textContent = "";
  view = await r.json();
  render();
  return view;
}

$("createBtn").onclick = async () => {
  const order = $("setOrder").value.split(",");
  const first = $("firstArm").value;
  const arms = { [order[0]]: first, [order[1]]: first === "ai" ? "human" : "ai" };
  const r = await fetch("/api/sessions", {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ expert_id: $("expertId").value, cell: Number($("cell").value),
                           set_order: order, arms, pilot: $("pilot").checked }),
  });
  if (!r.ok) { alert(await r.text()); return; }
  sid = (await r.json()).session_id;
  history.replaceState(null, "", `?session=${sid}`);
  start();
};

for (const b of document.querySelectorAll("[data-post]")) b.onclick = () => call(b.dataset.post);
$("markI").onclick = () => call("/human/marker", { speaker: "interviewer" });
$("markE").onclick = () => call("/human/marker", { speaker: "expert" });
document.addEventListener("keydown", (e) => {
  if (e.target.tagName === "INPUT" || e.target.isContentEditable) return;
  if (e.key === "i") $("markI").click();
  if (e.key === "e") $("markE").click();
});
$("typedBtn").onclick = () => {
  const idx = view.state.dialogue[view.state.current_set].length;
  call("/probe/answer-text", { turn_index: idx, text: $("typedAnswer").value }).then(() => { $("typedAnswer").value = ""; });
};
$("addBtn").onclick = () => call("/segments", { problem_id: $("addPid").value, text: $("addText").value });

function fmt(s) { const m = Math.floor(s / 60), r = Math.floor(s % 60); return `${m}:${String(r).padStart(2, "0")}`; }

function render() {
  const st = view.state;
  const arm = st.current_set ? st.arms[st.current_set] : null;
  $("title").textContent = `Session ${view.session_id}${view.manifest.pilot ? " (pilot)" : ""}`;
  const link = `${view.expert_origin || location.origin}/expert?session=${view.session_id}`;
  $("expertLink").textContent = link; $("expertLink").href = link;
  $("phase").textContent = `${st.phase}${st.current_problem ? " · " + st.current_problem : ""}${st.current_set ? " · set " + st.current_set + " (" + arm + ")" : ""}${st.paused ? " · PAUSED" : ""}`;
  $("clock").textContent = st.current_set ? `elapsed ${fmt(view.elapsed)} · remaining ${fmt(Math.max(0, view.remaining))}` : "";
  if (st.error) $("error").textContent = st.error;
  $("humanPanel").hidden = arm !== "human";
  $("aiPanel").hidden = arm !== "ai";
  if (arm === "ai") $("uncovered").textContent = (view.uncovered || []).join(", ") || "none";
  if (arm === "human") {
    const ticked = new Set((st.ticks[st.current_set] || []).map((t) => `${t.problem_id}/${t.stem_id}`));
    $("stemChips").replaceChildren(...st.sets[st.current_set].flatMap((pid) => Object.keys(view.stems).map((stem) => {
      const chip = document.createElement("span");
      chip.className = `chip${ticked.has(`${pid}/${stem}`) ? " done" : ""}`;
      chip.textContent = `${pid}/${stem}`;
      chip.onclick = () => call("/human/stem", { problem_id: pid, stem_id: stem });
      return chip;
    })));
  }
  const dialogue = st.current_set ? st.dialogue[st.current_set] : [];
  $("dialogue").replaceChildren(...dialogue.map((d) => {
    const p = document.createElement("p");
    p.textContent = d.speaker === "interviewer"
      ? `Q [${d.problem_id || "?"}/${d.stem_id || "?"}${d.is_followup ? " follow-up" : ""}, ${d.source}]: ${d.text}`
      : `A: ${d.text}`;
    return p;
  }));
  if (!document.activeElement || document.activeElement.tagName !== "TD") {
    $("trace").replaceChildren(...st.segments.map((s) => {
      const tr = document.createElement("tr");
      const id = document.createElement("td"); id.textContent = s.id;
      const time = document.createElement("td"); time.textContent = `${s.start.toFixed(1)}s`;
      const text = document.createElement("td"); text.textContent = s.text; text.contentEditable = "true";
      text.onkeydown = (e) => { if (e.key === "Enter") { e.preventDefault(); text.blur(); call(`/segments/${s.id}`, { text: text.textContent }); } };
      tr.onclick = (e) => {
        if (e.target === text || arm !== "human" || !st.sets[st.current_set].includes(s.problem_id)) return;
        call("/human/anchor", { problem_id: s.problem_id, kind: "segments", segment_ids: [s.id] });
      };
      tr.append(id, time, text);
      return tr;
    }));
  }
  $("addPid").replaceChildren(...st.think_aloud_done.map((p) => new Option(p, p)));
}

async function poll() {
  try {
    const r = await fetch(`/api/sessions/${sid}/console-view`);
    if (r.ok) { view = await r.json(); render(); }
  } catch (err) { $("error").textContent = err.message; }
  setTimeout(poll, 1000);
}

function start() { $("create").hidden = true; $("run").hidden = false; poll(); }
if (sid) start();
