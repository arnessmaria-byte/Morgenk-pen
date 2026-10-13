// ---------- Tegning ----------
function render() {
  if (HEADLESS || !S) return;
  const app = $('#app');
  if (S.screen === 'run' && S.run && S.run.screen === 'battle' && S.run.battle) {
    const B = S.run.battle;
    if (!app.querySelector(`[data-battle="${B.id}"]`)) { app.innerHTML = viewBattle(); window.scrollTo(0, 0); }
    updateBattle();
  } else {
    let html;
    if (S.screen === 'setup') html = viewSetup();
    else if (S.screen === 'run' && S.run) html = { map: viewMap, event: viewEvent, levelup: viewLevel, end: viewEnd }[S.run.screen]();
    else html = viewKennel();
    const key = S.screen + ':' + (S.run ? S.run.screen + S.run.step : '');
    app.innerHTML = html;
    if (app.dataset.key !== key) { app.dataset.key = key; window.scrollTo(0, 0); }
  }
  $('#modal-root').innerHTML = UI.confirm ? `<div class="overlay"><div class="modal" role="dialog" aria-modal="true"><h2>${esc(UI.confirm.title)}</h2><p>${esc(UI.confirm.text)}</p>
    <div class="row"><button class="btn warn" data-act="confirm-yes">${esc(UI.confirm.yesLabel)}</button><button class="btn ghost" data-act="confirm-no">Avbryt</button></div></div></div>` : '';
  if (!UI.busy) save();
}
function toast(txt) {
  if (HEADLESS) return;
  const el = $('#toast'); el.textContent = txt; el.hidden = false;
  clearTimeout(UI.toastTimer); UI.toastTimer = setTimeout(() => { el.hidden = true; }, 3800);
}
function ask(title, text, yesLabel, yes) { UI.confirm = { title, text, yesLabel, yes }; }

// ---------- Kampinput ----------
function autoSelect() {
  const B = S.run && S.run.battle; if (!B) return;
  const d = B.units.find(u => u.side === 'dog' && !u.down && !u.acted);
  UI.sel = d ? d.id : null; UI.mode = 'move';
}
const canClick = B => B && !B.over && B.phase === 'player' && !UI.busy;
async function onTile(x, y) {
  const B = S.run && S.run.battle; if (!canClick(B)) return;
  const sel = selUnit(B), u = unitAt(B, x, y);
  if (sel && UI.mode.startsWith('act:')) {
    const id = UI.mode.slice(4);
    const usable = !sel.acted && sel.actions.includes(id) && !(sel.cds[id] > 0);
    if (usable && ACTIONS[id].targets(B, sel).some(t => t.x === x && t.y === y)) return playerAction(sel, id, x, y);
    UI.mode = 'move';
    if (!u) return;
  }
  if (u && u.side === 'dog' && !u.down) { UI.sel = u.id; UI.mode = 'move'; return; }
  if (sel && !sel.acted) {
    if (!sel.moved && !u) {
      const R = reach(B, sel);
      if (R.ends.has(x + ',' + y)) {
        sel.from = { x: sel.x, y: sel.y }; sel.moved = true; UI.busy = true;
        await animatePath(B, sel, pathTo(R.map, x, y));
        UI.busy = false; return;
      }
    }
    if (u && u.side === 'enemy') {
      const atk = sel.actions[0];
      if (!(sel.cds[atk] > 0) && ACTIONS[atk].targets(B, sel).some(t => t.x === x && t.y === y)) return playerAction(sel, atk, x, y);
    }
  }
  if (u) { UI.info = u.id; return; }
  UI.info = null;
}
async function playerAction(u, id, x, y) {
  const B = S.run.battle;
  execAction(B, u, id, x, y);
  UI.mode = 'move';
  await afterDogDone(B);
}
async function afterDogDone(B) {
  render();
  if (B.over) { finishBattle(); return; }
  UI.mode = 'move';
  const next = B.units.find(o => o.side === 'dog' && !o.down && !o.acted);
  if (next) { UI.sel = next.id; return; }
  UI.busy = true; render(); await wait(350); UI.busy = false;
  await endTurn();
}
function onAction(id) {
  const B = S.run && S.run.battle, u = selUnit(B);
  if (!canClick(B) || !u || u.acted) return;
  const A = ACTIONS[id]; if (!A || !u.actions.includes(id) || (u.cds[id] || 0) > 0) return;
  if (UI.mode === 'act:' + id) { UI.mode = 'move'; return; }
  const ts = A.targets(B, u); if (!ts.length) return;
  if (A.self) return playerAction(u, id, u.x, u.y);
  UI.mode = 'act:' + id;
}
async function endTurn() {
  const B = S.run && S.run.battle;
  if (!B || B.over || B.phase !== 'player' || UI.busy) return;
  UI.sel = null; UI.mode = 'move'; UI.info = null;
  for (const u of B.units) if (u.side === 'dog') u.acted = true;
  await enemyPhase(B);
  if (B.over) finishBattle(); else autoSelect();
  render();
}

// ---------- Handlinger fra knapper ----------
const H = {
  'intro-ok'() { S.intro = false; },
  info(ds) { toast(ds.text); },
  setup() { UI.setup = []; UI.pairing = null; S.screen = 'setup'; },
  'cancel-setup'() { S.screen = 'kennel'; },
  'toggle-dog'(ds) {
    const i = UI.setup.findIndex(s => s.dogId === ds.id);
    if (i >= 0) UI.setup.splice(i, 1);
    else if (UI.setup.length >= 4) toast('Maks fire hunder på tur.');
    else UI.setup.push({ dogId: ds.id, cls: suggestClass(dogById(ds.id), UI.setup.map(s => s.cls)) });
  },
  'set-cls'(ds) { const s = UI.setup.find(x => x.dogId === ds.id); if (s) s.cls = ds.cls; },
  'start-run'() { if (startRun(UI.setup.map(s => ({ dogId: s.dogId, cls: s.cls })))) UI.setup = []; },
  adopt() { const d = adopt(); if (d) toast(`${d.name} flyttet inn i kennelen.`); },
  sleep() { nightFall(); UI.pairing = null; toast(`God morgen! Dag ${S.day}.`); },
  pair(ds) { UI.pairing = ds.id; },
  'pair-with'(ds) { if (addPair(UI.pairing, ds.id)) toast('Paret. Valpene kommer når dere sover.'); UI.pairing = null; },
  'cancel-pair'() { UI.pairing = null; },
  unpair(ds) { S.pairs = S.pairs.filter(p => !p.includes(ds.id)); },
  kurs(ds) { const k = puppyCourse(ds.id); if (k) toast(`${dogById(ds.id).name} lærte mye på valpekurset. +1 ${STAT_NAME[k]}.`); },
  give(ds) { const d = dogById(ds.id); if (d) ask(`Gi bort ${d.name}?`, `${d.name} flytter til en snill familie på landet, og du får ${GIVE_BONES} bein. Hunden kommer ikke tilbake.`, 'Gi bort', () => giveAway(d.id)); },
  'new-game'() { ask('Starte på nytt?', 'Kennelen, alle hundene og minnelunden forsvinner.', 'Start nytt spill', () => newGame()); },
  'confirm-yes'() { const f = UI.confirm && UI.confirm.yes; UI.confirm = null; if (f) f(); },
  'confirm-no'() { UI.confirm = null; },
  'choose-node'(ds) { chooseNode(+ds.i); },
  'go-home'() { ask('Gå hjem?', 'Laget går hjem nå. Hundene blir veteraner og kan ikke gå på tur igjen.', 'Gå hjem', () => endRun('hjem')); },
  'event-opt'(ds) { chooseEvent(+ds.i); },
  'event-next'() { continueEvent(); },
  offer(ds) { chooseOffer(+ds.i); },
  'close-run'() { closeRun(); },
  tile(ds) { return onTile(+ds.x, +ds.y); },
  action(ds) { return onAction(ds.id); },
  'end-turn'() { return endTurn(); },
  'sel-dog'(ds) { UI.sel = ds.id; UI.mode = 'move'; },
  wait() { const B = S.run && S.run.battle, u = selUnit(B); if (!canClick(B) || !u) return; u.acted = true; u.moved = true; return afterDogDone(B); },
  undo() {
    const B = S.run && S.run.battle, u = selUnit(B);
    if (canClick(B) && u && u.from && u.moved && !u.acted && isFree(B, u.from.x, u.from.y)) { u.x = u.from.x; u.y = u.from.y; u.from = null; u.moved = false; }
  },
  'battle-continue'() { continueAfterBattle(); },
};
let pending = Promise.resolve();
function dispatch(act, ds = {}) {
  const h = H[act]; if (!h) return pending;
  const r = h(ds);
  render();
  if (r && r.then) pending = r.then(() => render());
  return pending;
}

// ---------- Lagring ----------
let lastSave = null;
function save() {
  if (HEADLESS) return;
  lastSave = JSON.stringify({ S, rng: rngState });
  try { localStorage.setItem(SAVE_KEY, lastSave); } catch (e) { /* lagring er valgfri */ }
}
function load() {
  try {
    const raw = localStorage.getItem(SAVE_KEY); if (!raw) return false;
    const o = JSON.parse(raw); if (!o || !o.S || o.S.v !== 1) return false;
    S = o.S; rngState = (o.rng >>> 0) || 1; return true;
  } catch (e) { return false; }
}
function resume() {
  const B = S.run && S.run.battle; if (!B) return;
  UI.busy = false;
  if (B.over) { finishBattle(); render(); return; }
  if (B.phase === 'enemy') enemyPhase(B).then(() => { if (B.over) finishBattle(); else autoSelect(); render(); });
  else autoSelect();
}

// ---------- Oppstart ----------
document.addEventListener('click', e => {
  const el = e.target.closest('[data-act]');
  if (!el || el.disabled || e.detail > 1) return; // andre klikk i et dobbeltklikk skal ikke treffe neste hunds knapp
  dispatch(el.dataset.act, { ...el.dataset });
});
document.addEventListener('mouseover', e => {
  const el = e.target.closest('.tile'); const B = S && S.run && S.run.battle;
  if (!el || !B || !UI.mode.startsWith('act:')) return;
  UI.hover = { x: +el.dataset.x, y: +el.dataset.y }; refreshTiles(B);
});
document.addEventListener('keydown', e => {
  if (e.key !== 'Escape') return;
  if (UI.confirm) UI.confirm = null; else if (UI.pairing) UI.pairing = null; else if (UI.mode !== 'move') UI.mode = 'move'; else return;
  render();
});
function start(data) {
  if (data && data.S && data.S.v === 1) { S = data.S; rngState = (data.rng >>> 0) || 1; }
  else if (!load()) newGame();
  render();
  try { if (window.claude && window.claude.hot && window.claude.hot.snapshot) window.claude.hot.snapshot(() => (lastSave ? JSON.parse(lastSave) : { S, rng: rngState })); } catch (e) { /* ikke i en visning */ }
  resume();
  render();
}

// Test-API: lar Playwright kjøre de samme funksjonene som knappene bruker.
window.VOFF = {
  get S() { return S; }, set S(v) { S = v; }, UI,
  seed, rnd, newGame, makePuppy, makeStray, addDog, relation, derive, eff, dogById,
  makeBattle, simBattle, battleProblems, autoRun, startRun, chooseNode, finishBattle, continueAfterBattle,
  nightFall, addPair, dispatch, render, MUTS, STATS, LEARNED,
  idle: () => pending,
  headless(v) { HEADLESS = !!v; },
  speed(v) { SPEED = v; },
};

const hot = window.claude && window.claude.hot;
if (hot && hot.ready) hot.ready(start); else start((hot && hot.data) || {});
