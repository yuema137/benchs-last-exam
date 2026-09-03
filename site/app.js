const state = { data: null, x: "age", y: "raw", sort: "release" };
const $ = (id) => document.getElementById(id);

function formatScore(value) { return value == null ? "N/A" : `${(value * 100).toFixed(1)}%`; }
function formatDays(days) { return days == null ? "Not reached" : `${(days / 30.44).toFixed(1)} mo`; }
function ageMonths(release) { return (new Date(state.data.snapshot_id) - new Date(release)) / 86400000 / 30.44; }
function normalized(row) { return state.y === "normalized" && row.floor != null && row.ceiling != null; }

function chart(row) {
  const points = row.frontier;
  if (!points.length) return "<p class='small'>No plottable observations.</p>";
  const values = points.map(p => normalized(row) ? Math.max(0, Math.min(1, (p.score-row.floor)/(row.ceiling-row.floor))) : p.score);
  const minDate = new Date(row.release), maxDate = new Date(state.data.snapshot_id);
  const width=520, height=150, left=34, right=8, top=14, bottom=24;
  const x = p => state.x === "age" ? left + ((new Date(p.date)-minDate)/(maxDate-minDate || 1))*(width-left-right) : left + ((new Date(p.date)-new Date("2020-01-01"))/(maxDate-new Date("2020-01-01") || 1))*(width-left-right);
  const y = v => top + (1-v)*(height-top-bottom);
  const path = points.map((p,i) => `${i ? "L":"M"}${x(p).toFixed(1)},${y(values[i]).toFixed(1)}`).join(" ");
  const dots = points.map((p,i) => `<circle class="dot" cx="${x(p).toFixed(1)}" cy="${y(values[i]).toFixed(1)}" r="3"><title>${p.model}: ${formatScore(p.score)} (${p.date})</title></circle>`).join("");
  const labels = state.y === "normalized" ? ["100%","50%","0%"] : ["100%","50%","0%"];
  return `<svg viewBox="0 0 ${width} ${height}" role="img" aria-label="Historical SOTA frontier for ${row.name}"><line class="gridline" x1="${left}" y1="${y(1)}" x2="${width-right}" y2="${y(1)}"/><line class="gridline" x1="${left}" y1="${y(.5)}" x2="${width-right}" y2="${y(.5)}"/><line class="gridline" x1="${left}" y1="${y(0)}" x2="${width-right}" y2="${y(0)}"/><text x="2" y="${y(1)+4}">${labels[0]}</text><text x="2" y="${y(.5)+4}">${labels[1]}</text><text x="2" y="${y(0)+4}">${labels[2]}</text><path class="curve" d="${path}"/>${dots}<text x="${left}" y="${height-5}">${state.x === "age" ? "release" : "2020"}</text><text x="${width-35}" y="${height-5}">now</text></svg>`;
}

function card(row) {
  const current = normalized(row) ? row.normalized_progress : row.current_frontier;
  const headroom = normalized(row) ? row.normalized_headroom : null;
  const cov = `${Math.round(row.coverage.value*100)}%`;
  const highlight = state.sort === "coverage" ? "coverage" : state.sort === "headroom" ? "headroom" : state.sort === "current_frontier" ? "frontier" : "";
  const provenance = row.frontier.slice(-8).reverse().map(p => `<div><strong>${formatScore(p.score)}</strong> · ${p.model} · ${p.date}<br><a href="${p.source}" target="_blank" rel="noreferrer">source</a></div>`).join("");
  return `<article class="card"><div class="card-head"><div><h2>${row.name}</h2><div class="domain">${row.domain}</div><div class="meta">Released ${row.release} · ${ageMonths(row.release).toFixed(0)} months old</div></div><span class="status">${row.coverage.status.toUpperCase()} COVERAGE</span></div><div class="chart">${chart(row)}</div><div class="kpis"><div class="kpi ${highlight==='frontier'?'highlight':''}"><span class="small">Current SOTA</span><strong>${formatScore(current)}</strong></div><div class="kpi ${highlight==='headroom'?'highlight':''}"><span class="small">Headroom</span><strong>${headroom == null ? "N/A" : formatScore(headroom)}</strong></div><div class="kpi"><span class="small">T50</span><strong>${formatDays(row.threshold_days.T50)}</strong></div><div class="kpi"><span class="small">T90</span><strong>${formatDays(row.threshold_days.T90)}</strong></div><div class="kpi"><span class="small">Coverage</span><strong class="${highlight==='coverage'?'highlight':''}">${cov}</strong></div><div class="kpi"><span class="small">Observations</span><strong>${row.observation_count}</strong></div></div><details><summary>Frontier provenance and caveats</summary><p>${row.date_policy}</p><p>Reference organizations represented: ${row.coverage.represented_organizations.join(", ") || "None"}.</p><div class="provenance">${provenance}</div></details></article>`;
}

function render() {
  let rows = [...state.data.benchmarks];
  rows.sort((a,b) => { const v = key => key === "release" ? new Date(a.release)-new Date(b.release) : key === "coverage" ? b.coverage.value-a.coverage.value : key === "headroom" ? (a.normalized_headroom ?? 2)-(b.normalized_headroom ?? 2) : key === "t50" ? (a.threshold_days.T50 ?? 1e9)-(b.threshold_days.T50 ?? 1e9) : key === "t90" ? (a.threshold_days.T90 ?? 1e9)-(b.threshold_days.T90 ?? 1e9) : (b.current_frontier ?? -1)-(a.current_frontier ?? -1); return v(state.sort); });
  $("cards").innerHTML = rows.map(card).join("");
}

Promise.all([fetch("data/benchmarks.json").then(r=>r.json())]).then(([data]) => { state.data=data; $("snapshot").textContent=`Snapshot ${data.snapshot_id} · ${data.benchmarks.length} benchmarks`; render(); $("x-axis").onchange=e=>{state.x=e.target.value;render()}; $("y-axis").onchange=e=>{state.y=e.target.value;render()}; $("sort").onchange=e=>{state.sort=e.target.value;render()}; }).catch(error => { $("cards").innerHTML=`<div class="notice">Could not load snapshot: ${error}</div>`; });
