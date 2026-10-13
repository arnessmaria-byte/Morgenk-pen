// ---------- Visninger ----------
const SEX = { M: '♂', F: '♀' };
const STATUS_TXT = { voksen: 'Klar for tur', valp: 'Valp', veteran: 'Veteran' };
const STATUS_CLS = { voksen: 'klar', valp: 'valp', veteran: 'veteran' };

function topBar(narrow) {
  return `<header class="top${narrow ? ' narrow' : ''}"><div><div class="logo">Voffgenics</div><div class="tagline">Avl, mutasjoner og bakgårdskrig mot kattene</div></div>
  <div class="meters"><span class="meter">Dag ${S.day}</span><span class="meter">${S.bones} bein</span><span class="meter">Kongen slått: ${S.wins}</span></div></header>`;
}
function infoChip(cls, name, text) { return `<button class="chip ${cls}" data-act="info" data-text="${esc(name + ': ' + text)}">${esc(name)}</button>`; }
function statRows(d) {
  return STATS.map(k => {
    const base = d.stats[k], e = eff(d, k);
    let pips = '';
    for (let i = 1; i <= 10; i++) {
      let c = '';
      if (i <= Math.min(base, e)) c = 'on';
      else if (i <= e) c = 'plus';
      else if (i <= base) c = 'minus';
      pips += `<i class="${c}"></i>`;
    }
    return `<div class="stat" title="${STAT_NAME[k]}: ${STAT_HELP[k]}"><span>${STAT_ABBR[k]}</span><span class="pips">${pips}</span><span class="v">${e}</span></div>`;
  }).join('');
}
function chipsFor(d) {
  const m = d.muts.map(id => infoChip(MUTS[id].bad ? 'mut bad' : 'mut', MUTS[id].name, MUTS[id].desc));
  const a = d.learned.map(id => infoChip('abil', abil(id).name, abil(id).desc));
  return m.concat(a).join('') || '<span class="muted" style="font-size:12.5px">Ingen evner eller mutasjoner ennå</span>';
}
function lineage(d) {
  if (!d.mom && !d.dad) return 'Gatehund, ukjente foreldre';
  const n = id => (S.reg[id] && S.reg[id].name) || 'ukjent';
  return `Mor: ${esc(n(d.mom))} · Far: ${esc(n(d.dad))} · Gen. ${d.gen}`;
}
function dogCard(d) {
  const D = derive(d);
  let cls = `dog ${d.status}`, actions = '';
  if (UI.pairing) {
    const a = dogById(UI.pairing);
    if (d.id === UI.pairing) actions = `<button class="btn ghost small" data-act="cancel-pair">Avbryt</button>`;
    else {
      const prob = pairProblem(a, d);
      if (prob) { cls += ' dim'; actions = `<span class="muted" style="font-size:12.5px">${prob}</span>`; }
      else {
        const rel = relation(a.id, d.id); cls += ' cand';
        actions = `<button class="btn small go" data-act="pair-with" data-id="${d.id}">Par med ${esc(a.name)}</button><span class="warnline ${rel}">${REL_TXT[rel]}</span>`;
      }
    }
  } else {
    const p = pairedWith(d.id);
    if (p) actions += `<span class="warnline">Paret med ${esc(dogById(p).name)} i natt</span>`;
    else if (canBreed(d)) actions += `<button class="btn small" data-act="pair" data-id="${d.id}">Finn partner</button>`;
    if (d.status === 'valp' && !d.kurs) actions += `<button class="btn small ghost" data-act="kurs" data-id="${d.id}" ${S.bones >= KURS_COST ? '' : 'disabled'}>Valpekurs · ${KURS_COST} bein</button>`;
    actions += `<button class="btn small ghost" data-act="give" data-id="${d.id}">Gi bort</button>`;
  }
  return `<article class="${cls}" data-dog="${d.id}">
    <div class="dog-head"><div class="pic">${dogSVG(d)}</div>
      <div class="id"><h3>${esc(d.name)} <span class="sex">${SEX[d.sex]}</span></h3><div class="reg">${d.reg}</div>
      <div class="row" style="gap:5px"><span class="pill ${STATUS_CLS[d.status]}">${STATUS_TXT[d.status]}</span><span class="pill">Nivå ${d.level}</span>${d.scars ? `<span class="pill">${d.scars} arr</span>` : ''}</div></div></div>
    <div class="stats">${statRows(d)}</div>
    <div class="derived">Helse ${D.maxHp} · Går ${D.move} · Bitt ${D.melee}</div>
    <div class="chips">${chipsFor(d)}</div>
    <div class="lineage">${lineage(d)}</div>
    <div class="card-actions">${actions}</div>
  </article>`;
}
function helpList() {
  return `<ol>
    <li><b>Avl.</b> Par en hann og en tispe. I natt får de valper som arver egenskaper, lærte evner og mutasjoner. Nær slekt gir defekter.</li>
    <li><b>Tur.</b> Send opptil fire voksne hunder ut. Hvert halsbånd gir en klasse. Slå Kattekongen på slutten.</li>
    <li><b>Kamp.</b> Trykk på en hund, trykk på en lys rute for å gå, velg en handling og et mål. Avslutt turen når du er ferdig.</li>
    <li><b>Død.</b> Hunder som faller, kan dø for godt. De som kommer hjem, blir veteraner og kan bare brukes til avl.</li>
  </ol>`;
}
function viewKennel() {
  const order = { voksen: 0, valp: 1, veteran: 2 };
  const dogs = S.dogs.slice().sort((a, b) => order[a.status] - order[b.status] || (+a.id.slice(1)) - (+b.id.slice(1)));
  const ready = S.dogs.filter(d => d.status === 'voksen').length;
  const pairs = S.pairs.map(([a, b]) => {
    const A = dogById(a), Bd = dogById(b); if (!A || !Bd) return '';
    const rel = relation(a, b);
    return `<div class="pair"><div class="pic sm">${dogSVG(A)}</div><span class="heart">+</span><div class="pic sm">${dogSVG(Bd)}</div>
      <div><b>${esc(A.name)} og ${esc(Bd.name)}</b><div class="warnline ${rel}">${REL_TXT[rel]}</div></div>
      <button class="btn small ghost" data-act="unpair" data-id="${a}">Fjern</button></div>`;
  }).join('');
  const pairing = UI.pairing && dogById(UI.pairing);
  return `${topBar()}<main class="wrap">
    ${S.intro ? `<section class="panel intro"><h2 class="sec">Velkommen til kennelen</h2>${helpList()}<div><button class="btn" data-act="intro-ok">Skjønner, la oss starte</button></div></section>` : ''}
    <section class="panel news"><div class="eyebrow">${S.day === 1 ? 'Dag 1' : `I natt · nå er det dag ${S.day}`}</div><ul>${S.news.map(n => `<li>${esc(n)}</li>`).join('')}</ul></section>
    <section class="row">
      <button class="btn big" data-act="setup" ${ready ? '' : 'disabled'}>Send på tur</button>
      <button class="btn" data-act="adopt" ${S.bones >= ADOPT_COST && S.dogs.length < CAP ? '' : 'disabled'}>Adopter gatehund · ${ADOPT_COST} bein</button>
      <button class="btn ghost" data-act="sleep">Sov til i morgen</button>
    </section>
    ${pairing ? `<div class="banner"><span>Velg en partner til ${esc(pairing.name)} ${SEX[pairing.sex]}</span><button class="btn small ghost" data-act="cancel-pair">Avbryt</button></div>` : ''}
    ${pairs ? `<section><div class="sec-head"><h2 class="sec">Parringer i natt</h2><span class="muted">Valpene kommer når dere sover</span></div><div class="pairs">${pairs}</div></section>` : ''}
    <section><div class="sec-head"><h2 class="sec">Kennelen</h2><span class="mono">${S.dogs.length}/${CAP} plasser</span></div>
      <div class="grid">${dogs.map(dogCard).join('')}</div></section>
    <section class="panel"><details class="fold"><summary>Minnelunden (${S.grave.length})</summary>
      ${S.grave.length ? `<ul class="grave">${S.grave.map(g => `<li><b>${esc(g.name)}</b> <span class="reg">${g.reg}</span>, nivå ${g.level}, ${esc(g.cause)} på dag ${g.day}.</li>`).join('')}</ul>` : '<p class="muted" style="margin-top:6px">Ingen har dødd ennå.</p>'}
    </details></section>
    ${S.intro ? '' : `<section class="panel"><details class="fold"><summary>Slik spiller du</summary><div style="margin-top:8px">${helpList()}</div></details></section>`}
    <div><button class="btn small ghost" data-act="new-game">Start et nytt spill</button></div>
  </main>`;
}

function viewSetup() {
  const dogs = S.dogs.filter(d => d.status === 'voksen');
  const cards = dogs.map(d => {
    const sel = UI.setup.find(s => s.dogId === d.id);
    const clsRow = sel ? `<div class="clsrow">${CLS_ORDER.map(c => `<button class="cls-btn ${sel.cls === c ? 'on' : ''}" style="--cc:var(--c-${c})" data-act="set-cls" data-id="${d.id}" data-cls="${c}">${CLASSES[c].name}</button>`).join('')}</div>` : '';
    return `<div class="pick ${sel ? 'on' : ''}"><button class="pick-top" data-act="toggle-dog" data-id="${d.id}" aria-pressed="${sel ? 'true' : 'false'}">
      <div class="pic sm">${dogSVG(d, sel ? { cls: sel.cls } : {})}</div>
      <div style="min-width:0"><b>${esc(d.name)} ${SEX[d.sex]}</b><span class="mono">${STATS.map(k => `${STAT_ABBR[k]} ${eff(d, k)}`).join(' · ')}</span></div>
      <span class="check">${sel ? '✓' : ''}</span></button>${clsRow}</div>`;
  }).join('');
  return `${topBar()}<main class="wrap">
    <div><div class="eyebrow">Dag ${S.day}</div><h1 class="screen-title">Velg turlaget</h1>
    <p class="muted" style="max-width:62ch;margin-top:6px">Velg opptil fire voksne hunder og gi hver et halsbånd. De som kommer hjem, blir veteraner og går aldri på tur igjen.</p></div>
    <div class="picks">${cards || '<p>Ingen voksne hunder er klare. Sov en natt, eller adopter en gatehund.</p>'}</div>
    <section class="panel"><h3 style="margin-bottom:8px">Halsbånd</h3><div class="legend">${CLS_ORDER.map(c => `<div style="--cc:var(--c-${c})"><b>${CLASSES[c].name}</b>${CLASSES[c].desc}</div>`).join('')}</div></section>
    <div class="sticky-bar"><button class="btn ghost" data-act="cancel-setup">Tilbake</button>
      <button class="btn big go" data-act="start-run" ${UI.setup.length ? '' : 'disabled'}>Start turen${UI.setup.length ? ` med ${UI.setup.length}` : ''}</button></div>
  </main>`;
}

function hpBar(hp, max) { return `<div class="bar"><i style="width:${Math.round(100 * hp / max)}%"></i></div>`; }
function partyStrip() {
  return `<div class="party">${S.run.party.map(pm => {
    const d = dogById(pm.dogId);
    if (pm.dead || !d) return `<div class="pm dead"><div><div class="nm">${esc(pm.name)}</div><div class="sub">Død</div></div></div>`;
    const mx = maxHpOf(pm);
    return `<div class="pm"><div class="pic sm">${dogSVG(d, { cls: pm.cls })}</div><div style="flex:1;min-width:0"><div class="nm">${esc(d.name)}</div>
      <div class="sub">${CLASSES[pm.cls].name} · nivå ${d.level}</div>${hpBar(pm.hp, mx)}<div class="mono">${pm.hp}/${mx} helse</div></div></div>`;
  }).join('')}</div>`;
}
function nodeIcon(t) {
  const c = { kamp: '#c3362b', elite: '#7b3fb0', hendelse: '#2a52be', hvil: '#2e8745', boss: '#e2a524' }[t];
  const inner = {
    kamp: '<path d="M12 26 L26 12 M12 12 L26 26" stroke="#fff8ea" stroke-width="3.5" stroke-linecap="round"/>',
    elite: '<path d="M10 24 Q19 6 28 24 Z" fill="#fff8ea"/><circle cx="16" cy="20" r="1.6" fill="#24180d"/><circle cx="22" cy="20" r="1.6" fill="#24180d"/>',
    hendelse: '<text x="19" y="26" text-anchor="middle" font-size="18" font-family="Arial Black, sans-serif" fill="#fff8ea">?</text>',
    hvil: '<path d="M11 22 Q19 30 27 22" stroke="#fff8ea" stroke-width="3" fill="none" stroke-linecap="round"/><text x="25" y="15" font-size="9" font-family="Arial Black, sans-serif" fill="#fff8ea">z</text>',
    boss: '<path d="M10 26 L9 12 L15 18 L19 9 L23 18 L29 12 L28 26 Z" fill="#fff8ea" stroke="#24180d" stroke-width="1.5"/>',
  }[t];
  return `<svg class="ico" viewBox="0 0 38 38" aria-hidden="true"><circle cx="19" cy="19" r="17" fill="${c}" stroke="#24180d" stroke-width="2.5"/>${inner}</svg>`;
}
function nodeLabel(n) { return `${nodeIcon(n.t)}<span><b>${NODE_INFO[n.t].name}${n.t === 'kamp' || n.t === 'elite' ? `: ${esc(n.place)}` : ''}</b><small>${NODE_INFO[n.t].desc}</small></span>`; }
function runTop() {
  const run = S.run;
  return `<header class="top narrow"><div><div class="logo">Voffgenics</div><div class="tagline">På tur · steg ${Math.min(run.step + 1, STEPS)} av ${STEPS}</div></div>
  <div class="meters"><span class="meter">Dag ${S.day}</span><span class="meter">${S.bones} bein</span><span class="meter">Funnet: ${run.bones}</span></div></header>`;
}
function viewMap() {
  const run = S.run;
  const steps = run.nodes.map((opts, s) => {
    const label = s === STEPS - 1 ? 'Sjef' : `Steg ${s + 1}`;
    let body;
    if (s < run.step) body = opts.map((n, i) => `<div class="node past ${run.choice[s] === i ? 'chosen' : ''}">${nodeLabel(n)}</div>`).join('');
    else if (s === run.step) body = opts.map((n, i) => `<button class="node" data-act="choose-node" data-i="${i}">${nodeLabel(n)}</button>`).join('');
    else body = opts.map(n => `<div class="node future">${nodeLabel(n)}</div>`).join('');
    return `<li class="step"><span class="step-label">${label}</span><div class="nodes">${body}</div></li>`;
  }).join('');
  return `${runTop()}<main class="wrap narrow">
    <div><h1 class="screen-title">Turløypa</h1><p class="muted" style="margin-top:4px">Velg hvor laget går videre. Kattekongen venter på slutten.</p></div>
    ${partyStrip()}
    ${run.note ? `<p class="result">${esc(run.note)}</p>` : ''}
    <ol class="route">${steps}</ol>
    <div><button class="btn ghost" data-act="go-home">Gå hjem med laget</button></div>
  </main>`;
}
function viewEvent() {
  const run = S.run, ev = EVENTS.find(e => e.id === run.event.id);
  const body = run.event.result
    ? `<p class="result">${esc(run.event.result)}</p><div><button class="btn big" data-act="event-next">Gå videre</button></div>`
    : `<div class="row">${ev.opts.map((o, i) => `<button class="btn ${i ? 'ghost' : ''}" data-act="event-opt" data-i="${i}" ${o.need && !o.need() ? 'disabled' : ''}>${esc(o.label)}</button>`).join('')}</div>`;
  return `${runTop()}<main class="wrap narrow"><section class="panel story">
    <div class="eyebrow">Hendelse</div><h1 class="screen-title">${esc(ev.title)}</h1><p class="lead">${esc(ev.text)}</p>${body}</section>${partyStrip()}</main>`;
}
function viewLevel() {
  const run = S.run, q = run.levelQueue[0], d = dogById(q.dogId), pm = pmOf(q.dogId);
  const offers = q.offers.map((o, i) => o.kind === 'learn'
    ? `<button class="offer" data-act="offer" data-i="${i}"><span class="pill">Ny evne</span><b>${abil(o.id).name}</b><small>${abil(o.id).desc}</small></button>`
    : `<button class="offer" data-act="offer" data-i="${i}"><span class="pill">Egenskap</span><b>+1 ${STAT_NAME[o.k]}</b><small>${d.stats[o.k]} blir ${d.stats[o.k] + 1}. ${STAT_HELP[o.k]}.</small></button>`).join('');
  return `${runTop()}<main class="wrap narrow">
    <div class="lvl"><div class="pic big">${dogSVG(d, pm ? { cls: pm.cls } : {})}</div>
    <div style="flex:1;min-width:0"><div class="eyebrow">Nivå ${q.level}</div><h1 class="screen-title">${esc(d.name)} blir sterkere</h1>
    <p class="muted" style="margin-top:6px;max-width:52ch">Velg én belønning. Lærte evner og egenskaper kan arves av valpene. En hund kan kunne to evner.</p></div></div>
    <div class="offers">${offers}</div></main>`;
}
function viewEnd() {
  const r = S.run.result;
  const title = { seier: 'Kattekongen er slått!', tap: 'Laget falt', hjem: 'Hjemme igjen' }[r.kind];
  const text = {
    seier: 'De overlevende er nå veteraner. Kattekongen kommer tilbake, og han blir sterkere for hver gang.',
    tap: 'Hundene som overlevde, ble båret hjem. De er nå veteraner og kan brukes til avl.',
    hjem: 'Laget gikk hjem før det ble for farlig. De er nå veteraner og kan brukes til avl.',
  }[r.kind];
  return `${topBar(true)}<main class="wrap narrow"><section class="panel story">
    <div class="eyebrow">Turen er over</div><h1 class="screen-title">${title}</h1><p class="lead">${text}</p>
    <ul class="res">${r.lines.map(l => `<li class="${l.kind}"><b>${esc(l.who)}</b> ${esc(l.txt)}</li>`).join('')}</ul>
    <p>Bein funnet på turen: <b>${r.bones}</b>.</p>
    <div><button class="btn big" data-act="close-run">Tilbake til kennelen</button></div></section></main>`;
}

// ---------- Kampvisning ----------
const POOP_SVG = `<svg viewBox="0 0 40 40" aria-hidden="true"><path d="M11 32 Q6 32 7.5 27.5 Q9 24 13 24 Q11 19.5 16 18 Q16 12 21 10 Q23 14.5 25 16.5 Q30.5 18 28.5 23 Q33 24 32 28.5 Q31.5 32 27 32 Z" fill="#6b4422" stroke="#24180d" stroke-width="2"/><path d="M13 9 q2 -3 0 -6 M28 10 q2 -3 0 -6" stroke="#4d5e1f" stroke-width="1.6" fill="none"/></svg>`;
const OBSTACLES = [
  `<svg viewBox="0 0 40 40" aria-hidden="true"><path d="M7 31 Q4 18 14 11 Q23 5 31 13 Q38 21 33 31 Z" fill="#a39c92" stroke="#24180d" stroke-width="2.5"/><path d="M14 17 q4 -3 8 -1" stroke="#24180d" stroke-width="1.5" fill="none" opacity=".5"/></svg>`,
  `<svg viewBox="0 0 40 40" aria-hidden="true"><rect x="7" y="8" width="26" height="25" rx="2" fill="#b47a44" stroke="#24180d" stroke-width="2.5"/><path d="M7 8 L33 33 M33 8 L7 33" stroke="#24180d" stroke-width="2"/></svg>`,
  `<svg viewBox="0 0 40 40" aria-hidden="true"><circle cx="13" cy="23" r="9" fill="#3f6b2a" stroke="#24180d" stroke-width="2.5"/><circle cx="27" cy="23" r="9" fill="#3f6b2a" stroke="#24180d" stroke-width="2.5"/><circle cx="20" cy="14" r="9" fill="#4b7c31" stroke="#24180d" stroke-width="2.5"/><circle cx="17" cy="13" r="1.6" fill="#c3362b"/><circle cx="25" cy="22" r="1.6" fill="#c3362b"/></svg>`,
];
function tilesHTML(B) {
  let h = '';
  for (let y = 0; y < B.h; y++) for (let x = 0; x < B.w; x++) {
    const t = tileAt(B, x, y);
    h += `<button class="tile ${(x + y) % 2 ? 'alt' : ''}" data-act="tile" data-x="${x}" data-y="${y}" aria-label="Rute ${x + 1},${y + 1}">${t === 1 ? OBSTACLES[clamp(B.deco[y * B.w + x], 0, 2)] : t === 2 ? POOP_SVG : ''}</button>`;
  }
  return h;
}
const selUnit = B => B && UI.sel ? B.units.find(u => u.id === UI.sel && !u.dead && u.side === 'dog') : null;
function viewBattle() {
  const run = S.run, B = run.battle, node = run.current;
  return `<div class="battle" data-battle="${B.id}">
    <header class="bt-top"><div><div class="eyebrow">${esc(B.place)} · steg ${Math.min(run.step + 1, STEPS)} av ${STEPS}${node.t === 'elite' ? ' · elitekamp' : ''}</div><h1 id="turn-title"></h1></div>
      <div class="meters"><span class="meter">${S.bones} bein</span></div></header>
    <div class="bt-main">
      <div><div class="board-wrap"><div class="board" id="board">${tilesHTML(B)}<div class="units" id="units"></div><div class="fxl" id="fxl"></div></div></div>
      <p class="legend-line" style="margin-top:8px">Lys rute: kan gå. Rød ring: kan angripes. Grønn ring: kan helbredes. Trykk på en fiende for å se hva den gjør.</p></div>
      <aside class="bt-side" id="bt-side"></aside>
    </div>
    <div id="bt-overlay"></div>
  </div>`;
}
function battlePanel(B) {
  const sel = selUnit(B);
  let h = '';
  if (B.phase === 'enemy') h += `<div class="panel"><h3>Fiendens tur</h3><p class="hint">Rotter, måker og katter flytter seg.</p></div>`;
  else if (sel) h += selPanel(B, sel);
  else h += `<div class="panel"><h3>Velg en hund</h3><p class="hint">Trykk på en hund på brettet eller i lista.</p><div class="roster">${B.units.filter(u => u.side === 'dog').map(u =>
    `<button data-act="sel-dog" data-id="${u.id}" ${u.down ? 'disabled' : ''}><div class="pic sm">${dogSVG(dogById(u.dogId), { cls: u.cls })}</div><span><b>${esc(u.name)}</b><span class="sub" style="display:block">${u.down ? 'Ligger nede' : u.acted ? 'Ferdig denne runden' : 'Klar'} · ${u.hp}/${u.maxHp}</span></span></button>`).join('')}</div></div>`;
  const info = UI.info && B.units.find(u => u.id === UI.info && !u.dead && u.side === 'enemy');
  if (info) h += `<div class="panel"><div class="sel-head"><div class="pic sm">${foeSVG(info.type)}</div><div><h3>${esc(info.name)}</h3>
    <div class="sub">${info.hp}/${info.maxHp} helse · ${info.dmg} skade · rekker ${info.range[0] === info.range[1] ? info.range[0] : info.range.join('-')} · går ${info.move}</div>
    <div class="sub">Unnviker ${pct(info.dodge)}. ${ENEMY_INFO[info.type]}${info.poison ? ` Har lopper (${info.poison}).` : ''}</div></div></div></div>`;
  h += `<button class="btn big endturn" data-act="end-turn" ${B.phase !== 'player' || UI.busy || B.over ? 'disabled' : ''}>Avslutt tur</button>`;
  h += `<div class="panel log"><h3>Logg</h3><ol>${B.log.slice(-7).reverse().map(l => `<li>${esc(l)}</li>`).join('')}</ol></div>`;
  return h;
}
function selPanel(B, u) {
  const d = dogById(u.dogId);
  const acts = u.actions.map(id => {
    const A = ACTIONS[id], cd = u.cds[id] || 0;
    const ok = !u.acted && cd === 0 && B.phase === 'player' && A.targets(B, u).length > 0;
    return `<button class="act ${UI.mode === 'act:' + id ? 'on' : ''}" data-act="action" data-id="${id}" ${ok ? '' : 'disabled'}>
      <b>${A.name}</b><span class="cd">${cd > 0 ? `klar om ${cd}` : A.val(u)}</span><small>${A.desc}</small></button>`;
  }).join('');
  let hint;
  if (u.acted) hint = `${esc(u.name)} har gjort sitt denne runden.`;
  else if (UI.mode.startsWith('act:')) hint = 'Trykk på et markert mål. Trykk på handlingen igjen for å avbryte.';
  else hint = u.moved ? 'Velg en handling, eller trykk på en fiende for å angripe.' : 'Trykk på en lys rute for å gå, eller angrip direkte.';
  return `<div class="panel">
    <div class="sel-head"><div class="pic sm">${dogSVG(d, { cls: u.cls })}</div><div style="min-width:0"><h3>${esc(u.name)}</h3>
      <div class="sub">${CLASSES[u.cls].name} · ${u.hp}/${u.maxHp} helse${u.shield ? ` · ${u.shield} skjold` : ''}${u.poison ? ` · lopper ${u.poison}` : ''}</div>
      <div class="sub mono">Går ${u.move} · unnviker ${pct(u.dodge)} · krit ${pct(u.crit)}</div></div></div>
    <p class="hint">${hint}</p>
    <div class="acts">${acts}</div>
    <div class="row" style="margin-top:10px">${u.moved && !u.acted && u.from ? '<button class="btn ghost small" data-act="undo">Angre flytt</button>' : ''}${!u.acted ? `<button class="btn ghost small" data-act="wait">Ferdig med ${esc(u.name)}</button>` : ''}</div>
  </div>`;
}
function resultOverlay(res) {
  return `<div class="overlay"><div class="modal" role="dialog" aria-modal="true"><h2>${res.win ? (res.boss ? 'Kattekongen er slått!' : 'Seier!') : 'Laget falt'}</h2>
    <p>${res.win ? `Dere fant ${res.bones} bein.` : 'Alle hundene ligger nede. Turen er over.'}</p>
    ${res.lines.length ? `<ul class="res">${res.lines.map(l => `<li class="${l.kind}"><b>${esc(l.who)}</b> ${esc(l.txt)}</li>`).join('')}</ul>` : ''}
    <div><button class="btn big" data-act="battle-continue">Fortsett</button></div></div></div>`;
}
function highlights(B) {
  const sel = selUnit(B), H = { move: new Set(), tgt: new Set(), ally: new Set(), area: new Set(), aoe: new Set() };
  if (B.phase !== 'player' || !sel || sel.acted || UI.busy || B.over) return H;
  if (UI.mode === 'move') {
    if (!sel.moved) for (const k of reach(B, sel).ends.keys()) H.move.add(k);
    const atk = sel.actions[0];
    if (!(sel.cds[atk] > 0)) for (const t of ACTIONS[atk].targets(B, sel)) H.tgt.add(t.x + ',' + t.y);
  } else if (UI.mode.startsWith('act:')) {
    const id = UI.mode.slice(4), A = ACTIONS[id], ts = A.targets(B, sel);
    for (const t of ts) {
      const k = t.x + ',' + t.y;
      if (A.area) H.area.add(k);
      else if (A.ally) H.ally.add(k);
      else if (id === 'grav' || id === 'baesj') H.move.add(k);
      else H.tgt.add(k);
    }
    if (A.area && UI.hover && H.area.has(UI.hover.x + ',' + UI.hover.y))
      for (let dy = -1; dy <= 1; dy++) for (let dx = -1; dx <= 1; dx++) H.aoe.add((UI.hover.x + dx) + ',' + (UI.hover.y + dy));
  }
  return H;
}
function refreshTiles(B) {
  const H = highlights(B);
  for (const el of document.querySelectorAll('#board .tile')) {
    const k = el.dataset.x + ',' + el.dataset.y;
    el.classList.toggle('hl-move', H.move.has(k)); el.classList.toggle('hl-tgt', H.tgt.has(k));
    el.classList.toggle('hl-ally', H.ally.has(k)); el.classList.toggle('hl-area', H.area.has(k)); el.classList.toggle('hl-aoe', H.aoe.has(k));
    const t = tileAt(B, +el.dataset.x, +el.dataset.y);
    if (t === 2 && !el.dataset.poop) { el.dataset.poop = '1'; el.innerHTML = POOP_SVG; }
  }
}
function syncUnits(B) {
  const layer = $('#units'); if (!layer) return;
  const sel = selUnit(B), ids = new Set();
  for (const u of B.units) {
    ids.add(u.id);
    let el = layer.querySelector(`[data-uid="${u.id}"]`);
    if (!el) {
      el = document.createElement('div'); el.className = `unit ${u.side === 'dog' ? 'ally' : 'foe'}`; el.dataset.uid = u.id;
      el.style.setProperty('--ring', u.side === 'dog' ? CLASSES[u.cls].hex : '#c3362b');
      el.innerHTML = `<div class="u-pic">${u.side === 'dog' ? dogSVG(dogById(u.dogId) || { look: randomLook(), muts: [], status: 'voksen' }, { cls: u.cls }) : foeSVG(u.type)}</div><div class="u-hp"><i></i></div><div class="badges"></div>`;
      layer.appendChild(el);
    }
    el.style.setProperty('--x', u.x); el.style.setProperty('--y', u.y);
    el.classList.toggle('sel', !!sel && sel.id === u.id);
    el.classList.toggle('done', u.side === 'dog' && u.acted && !u.down && B.phase === 'player');
    el.classList.toggle('down', !!u.down); el.classList.toggle('dead', !!u.dead);
    el.querySelector('.u-hp i').style.width = Math.round(100 * u.hp / u.maxHp) + '%';
    el.querySelector('.badges').innerHTML = (u.shield ? `<span class="badge sh">${u.shield}</span>` : '') + (u.poison ? `<span class="badge po">${u.poison}</span>` : '') + (u.taunt ? '<span class="badge ta">!</span>' : '');
    el.setAttribute('title', `${u.name}: ${u.hp}/${u.maxHp}`);
  }
  for (const el of [...layer.children]) if (!ids.has(el.dataset.uid)) el.remove();
  const fxl = $('#fxl');
  for (const f of B.fx) {
    const unitEl = layer.querySelector(`[data-uid="${f.id}"]`);
    const u = B.units.find(o => o.id === f.id);
    if (f.t === 'dmg' || f.t === 'crit') { if (unitEl) { unitEl.classList.remove('hit'); void unitEl.offsetWidth; unitEl.classList.add('hit'); } }
    const txt = f.t === 'miss' ? 'Bom!' : f.t === 'heal' ? `+${f.v}` : f.t === 'shield' ? `+${f.v}` : `-${f.v}${f.t === 'crit' ? '!' : ''}`;
    if ((f.t === 'dmg' || f.t === 'heal') && !f.v) continue;
    const el = document.createElement('div'); el.className = `float ${f.t}`; el.textContent = txt;
    el.style.setProperty('--x', u ? u.x : f.x); el.style.setProperty('--y', u ? u.y : f.y);
    fxl.appendChild(el); setTimeout(() => el.remove(), 1000);
  }
  B.fx = [];
}
function updateBattle() {
  const run = S.run, B = run.battle;
  const title = $('#turn-title');
  if (title) title.textContent = B.over ? (B.over === 'win' ? 'Seier!' : 'Laget falt') : B.phase === 'player' ? `Runde ${B.round} · din tur` : `Runde ${B.round} · fiendens tur`;
  refreshTiles(B); syncUnits(B);
  const side = $('#bt-side'); if (side) side.innerHTML = battlePanel(B);
  const ov = $('#bt-overlay'); if (ov) ov.innerHTML = run.battleResult ? resultOverlay(run.battleResult) : '';
}
