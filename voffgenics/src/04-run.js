// ---------- Turen ----------
const alive = () => S.run ? S.run.party.filter(p => !p.dead) : [];
const pmOf = id => S.run && S.run.party.find(p => p.dogId === id);
const maxHpOf = pm => derive(dogById(pm.dogId), pm.cls).maxHp;
const healPm = (pm, n) => { pm.hp = clamp(pm.hp + n, 1, maxHpOf(pm)); };

function rollNode(step, avoid) {
  const w = [['kamp', 40], ['hendelse', 25], ['hvil', step >= 2 ? 15 : 8], ['elite', step >= 2 ? 20 : 0]];
  for (let tries = 0; tries < 20; tries++) {
    let r = rnd() * w.reduce((s, x) => s + x[1], 0), t = 'kamp';
    for (const [k, v] of w) { if (r < v) { t = k; break; } r -= v; }
    if (!avoid || t !== avoid.t || t === 'kamp') return { t, place: pick(PLACES[t]) };
  }
  return { t: 'kamp', place: pick(PLACES.kamp) };
}
function genNodes() {
  const steps = [];
  const a = pick(PLACES.kamp); let b = pick(PLACES.kamp); if (b === a) b = PLACES.kamp[(PLACES.kamp.indexOf(a) + 1) % PLACES.kamp.length];
  steps.push([{ t: 'kamp', place: a }, { t: 'kamp', place: b }]);
  for (let s = 1; s < STEPS - 1; s++) { const x = rollNode(s); steps.push([x, rollNode(s, x)]); }
  steps.push([{ t: 'boss', place: PLACES.boss[0] }]);
  return steps;
}
function suggestClass(d, used) {
  const st = k => eff(d, k);
  const score = { slass: st('sty') * 1.2 + st('uth') * 0.3, vokt: st('uth') * 1.2 + st('sty') * 0.3, jakt: st('smi') * 1.2 + st('hur') * 0.3, myst: st('int') * 1.2, pleie: st('int') * 0.9 + st('uth') * 0.3 };
  const order = CLS_ORDER.slice().sort((a, b) => score[b] - score[a]);
  return order.find(c => !used.includes(c)) || order[0];
}
function startRun(team) {
  team = team.filter(t => { const d = dogById(t.dogId); return d && d.status === 'voksen'; }).slice(0, 4);
  if (!team.length) return false;
  const used = [];
  for (const t of team) { if (!t.cls) t.cls = suggestClass(dogById(t.dogId), used); used.push(t.cls); }
  const party = team.map(t => { const d = dogById(t.dogId); return { dogId: d.id, cls: t.cls, hp: derive(d, t.cls).maxHp, dead: false, name: d.name }; });
  S.pairs = S.pairs.filter(p => !p.some(id => team.some(t => t.dogId === id)));
  S.run = { party, step: 0, nodes: genNodes(), choice: [], bones: 0, screen: 'map', battle: null, battleResult: null, event: null, levelQueue: [], used: [], note: null, current: null, next: 'map', result: null };
  S.screen = 'run';
  UI.pairing = null;
  return true;
}
function chooseNode(i) {
  const run = S.run; if (!run || run.screen !== 'map') return;
  const node = (run.nodes[run.step] || [])[i]; if (!node) return;
  run.choice[run.step] = i; run.current = node; run.note = null;
  if (node.t === 'kamp' || node.t === 'elite' || node.t === 'boss') {
    run.battle = makeBattle(node, run.step); run.battleResult = null; run.screen = 'battle';
    UI.info = null; autoSelect();
  } else if (node.t === 'hendelse') {
    const fresh = EVENTS.filter(e => !run.used.includes(e.id));
    const ev = fresh.length ? pick(fresh) : pick(EVENTS);
    run.used.push(ev.id); run.event = { id: ev.id, result: null }; run.screen = 'event';
  } else if (node.t === 'hvil') {
    for (const pm of alive()) healPm(pm, Math.ceil(maxHpOf(pm) * 0.6));
    run.note = `Dere hvilte ${node.place}. Alle fikk tilbake helse.`;
    run.step++; run.screen = 'map';
  }
}
function finishBattle() {
  const run = S.run, B = run && run.battle;
  if (!B || !B.over || run.battleResult) return;
  const win = B.over === 'win', node = run.current, lines = [];
  for (const u of B.units.filter(o => o.side === 'dog')) {
    const pm = pmOf(u.dogId), d = dogById(u.dogId);
    if (!pm || !d) continue;
    if (u.down) {
      if (chance(win ? u.save : u.save - 0.15)) {
        const k = scar(d); pm.hp = 1;
        lines.push({ who: d.name, txt: `kom seg på beina igjen, men fikk et arr (-1 ${STAT_NAME[k]}).`, kind: 'scar' });
      } else {
        pm.dead = true; killDog(d, `falt i ${B.place}`);
        lines.push({ who: d.name, txt: 'døde. Den blir husket i minnelunden.', kind: 'dead' });
      }
    } else {
      pm.hp = clamp(u.hp + (win ? 2 : 0), 1, maxHpOf(pm));
      if (win) {
        d.xp += node.t === 'elite' ? 2 : 1;
        if (d.xp >= 2) { d.xp -= 2; d.level++; const offers = makeOffers(d); if (offers.length) run.levelQueue.push({ dogId: d.id, level: d.level, offers }); }
      }
    }
  }
  let bones = 0;
  if (win) {
    bones = node.t === 'boss' ? 25 + S.heat * 5 : node.t === 'elite' ? 10 + run.step * 2 : 4 + run.step * 2;
    S.bones += bones; run.bones += bones;
  }
  run.battleResult = { win, lines, bones, boss: node.t === 'boss' };
}
function makeOffers(d) {
  const offers = [];
  if (d.learned.length < 2) for (const id of shuffle(LEARNED.filter(a => !d.learned.includes(a))).slice(0, 2)) offers.push({ kind: 'learn', id });
  const ks = shuffle(STATS.filter(k => d.stats[k] < 10));
  while (offers.length < 3 && ks.length) offers.push({ kind: 'stat', k: ks.pop() });
  return offers;
}
function continueAfterBattle() {
  const run = S.run; if (!run || !run.battleResult) return;
  const res = run.battleResult;
  run.battle = null; run.battleResult = null; UI.sel = null; UI.mode = 'move'; UI.info = null;
  if (!res.win) return endRun('tap');
  run.next = res.boss ? 'seier' : 'map';
  if (!res.boss) run.step++;
  proceed();
}
function proceed() {
  const run = S.run;
  if (!alive().length) return endRun('tap');
  run.levelQueue = run.levelQueue.filter(q => dogById(q.dogId));
  if (run.levelQueue.length) { run.screen = 'levelup'; return; }
  if (run.next === 'seier') return endRun('seier');
  run.screen = 'map';
}
function chooseOffer(i) {
  const run = S.run, q = run && run.levelQueue[0]; if (!q) return;
  const o = q.offers[i], d = dogById(q.dogId); if (!o || !d) return;
  const pm = pmOf(d.id), before = pm ? maxHpOf(pm) : 0;
  if (o.kind === 'learn' && d.learned.length < 2 && !d.learned.includes(o.id)) d.learned.push(o.id);
  if (o.kind === 'stat') d.stats[o.k] = Math.min(10, d.stats[o.k] + 1);
  if (pm) pm.hp = clamp(pm.hp + Math.max(0, maxHpOf(pm) - before), 1, maxHpOf(pm));
  run.levelQueue.shift();
  proceed();
}
function chooseEvent(i) {
  const run = S.run; if (!run || !run.event || run.event.result) return;
  const ev = EVENTS.find(e => e.id === run.event.id), o = ev && ev.opts[i];
  if (!o || (o.need && !o.need())) return;
  run.event.result = o.go();
}
function continueEvent() {
  const run = S.run; if (!run || !run.event || !run.event.result) return;
  run.event = null; run.step++; run.next = 'map'; proceed();
}
function endRun(kind) {
  const run = S.run, lines = [];
  for (const pm of run.party) {
    if (pm.dead) { lines.push({ who: pm.name, txt: 'døde på turen.', kind: 'dead' }); continue; }
    const d = dogById(pm.dogId); if (!d) continue;
    d.status = 'veteran'; d.runs++; if (kind === 'seier') d.wins++;
    lines.push({ who: d.name, txt: `kom hjem som veteran (nivå ${d.level}).`, kind: 'ok' });
  }
  if (kind === 'seier') { S.wins++; S.heat++; }
  run.battle = null; run.battleResult = null; run.event = null; run.levelQueue = [];
  run.result = { kind, lines, bones: run.bones };
  run.screen = 'end';
  nightFall();
}
function closeRun() { S.run = null; S.screen = 'kennel'; UI.sel = null; UI.mode = 'move'; }

// ---------- Hendelser ----------
const dogOf = pm => dogById(pm.dogId);
const EVENTS = [
  { id: 'soppel', title: 'Veltet søppelkasse', text: 'En søppelkasse har veltet bak en pizzarestaurant. Det lukter himmelsk.',
    opts: [
      { label: 'Rot gjennom den', go() {
        const pm = pick(alive()), d = dogOf(pm), r = rnd();
        if (r < 0.45) { bump(d, 'fla', 1); return `${d.name} fant et halvt kyllinglår og føler seg heldig. +1 Flaks.`; }
        if (r < 0.75) { S.bones += 8; S.run.bones += 8; return 'Dere fant 8 bein under en pizzaeske.'; }
        if (addMut(d, 'lopper')) return `${d.name} kom ut med lopper. Mutasjonen Lopper: ${MUTS.lopper.desc}.`;
        healPm(pm, -3); return `${d.name} fikk en boks i hodet. -3 helse.`;
      } },
      { label: 'Gå forbi', go: () => 'Dere går forbi. Det var nok lurt.' },
    ] },
  { id: 'kjottbein', title: 'Selvlysende kjøttbein', text: 'Bak et laboratorium ligger et grønt, selvlysende kjøttbein. Det summer svakt.',
    opts: [
      { label: 'La en hund spise det', go() {
        const d = dogOf(pick(alive())), m = randomMut(0.6, d.muts);
        if (!m || !addMut(d, m)) return `${d.name} spiste beinet. Ingenting skjedde, bortsett fra en lang rap.`;
        return `${d.name} spiste beinet og fikk mutasjonen ${MUTS[m].name}: ${MUTS[m].desc}.`;
      } },
      { label: 'La det ligge', go: () => 'Dere lar beinet ligge. Det fortsetter å summe.' },
    ] },
  { id: 'vet', title: 'Omreisende veterinær', text: 'En veterinær med campingvogn tilbyr helsesjekk. Hun tar betalt i bein.',
    opts: [
      { label: 'Betal 8 bein for full helse', need: () => S.bones >= 8, go() { S.bones -= 8; for (const pm of alive()) pm.hp = maxHpOf(pm); return 'Alle hundene er friske og raske igjen.'; } },
      { label: 'Nei takk', go: () => 'Veterinæren trekker på skuldrene og kjører videre.' },
    ] },
  { id: 'pinne', title: 'Den perfekte pinnen', text: 'Midt på stien ligger verdens beste pinne. Alle vil ha den.',
    opts: [
      { label: 'La dem slåss om den', go() {
        const p = shuffle(alive().slice());
        if (p.length < 2) { const d = dogOf(p[0]); bump(d, 'sty', 1); return `${d.name} vant pinnen uten kamp. +1 Styrke.`; }
        const w = dogOf(p[0]), l = dogOf(p[1]); bump(w, 'sty', 1); healPm(p[1], -3);
        return `${w.name} vant pinnen (+1 Styrke). ${l.name} fikk et bitt i øret (-3 helse).`;
      } },
      { label: 'Del den', go() { for (const pm of alive()) healPm(pm, 2); return 'Dere deler pinnen. Alle er glade. +2 helse til alle.'; } },
    ] },
  { id: 'postbud', title: 'Postbudet', text: 'Et postbud står helt stille ved en postkasse og stirrer på dere.',
    opts: [
      { label: 'Bjeff!', go() {
        if (chance(0.6)) { S.bones += 10; S.run.bones += 10; return 'Postbudet slipper matpakka og løper. Dere bytter den mot 10 bein.'; }
        const pm = pick(alive()); healPm(pm, -4); return `Postbudet hadde pepperspray. ${dogOf(pm).name} mister 4 helse.`;
      } },
      { label: 'Logre', go() { const d = dogOf(pick(alive())); bump(d, 'int', 1); return `Postbudet klør ${d.name} bak øret og lærer bort et triks. +1 Intelligens.`; } },
    ] },
  { id: 'dam', title: 'Gjørmete dam', text: 'En dam full av varm, deilig gjørme.',
    opts: [
      { label: 'Bad!', go() {
        for (const pm of alive()) healPm(pm, 3);
        if (chance(0.35)) { const d = dogOf(pick(alive())); bump(d, 'uth', 1); return `Alle får +3 helse. ${d.name} ble ekstra seig av gjørma. +1 Utholdenhet.`; }
        return 'Alle får +3 helse og lukter forferdelig.';
      } },
      { label: 'Hold dere tørre', go: () => 'Dere går rundt dammen. Kjedelig.' },
    ] },
  { id: 'katteluke', title: 'Ulåst katteluke', text: 'En katteluke står på gløtt. Innenfor hører dere snorking.',
    opts: [
      { label: 'Snik inn og stjel kattemat', go() {
        if (chance(0.5)) { S.bones += 12; S.run.bones += 12; return 'Dere stjeler en hel sekk kattemat og bytter den mot 12 bein.'; }
        for (const pm of alive()) healPm(pm, -3); return 'Katten våknet. Alle får klor over snuten (-3 helse).';
      } },
      { label: 'La katten sove', go: () => 'Dere lar katten sove. Den drømmer om dere.' },
    ] },
];

// ---------- Kennel-handlinger ----------
function adopt() {
  if (S.bones < ADOPT_COST || S.dogs.length >= CAP) return null;
  S.bones -= ADOPT_COST; return addDog(makeStray());
}
function addPair(aId, bId) {
  const a = dogById(aId), b = dogById(bId);
  if (!a || !canBreed(a) || pairedWith(aId) || pairProblem(a, b)) return false;
  S.pairs.push([aId, bId]); return true;
}
function puppyCourse(id) {
  const d = dogById(id); if (!d || d.status !== 'valp' || d.kurs || S.bones < KURS_COST) return null;
  const ks = STATS.filter(k => d.stats[k] < 10); if (!ks.length) return null;
  S.bones -= KURS_COST; d.kurs = true; const k = pick(ks); d.stats[k]++; return k;
}
function giveAway(id) {
  const d = dogById(id); if (!d) return;
  S.dogs = S.dogs.filter(x => x.id !== id); S.pairs = S.pairs.filter(p => !p.includes(id)); S.bones += GIVE_BONES;
}

// ---------- Autospill av en hel tur (tester) ----------
function autoTeam() {
  return shuffle(S.dogs.filter(d => d.status === 'voksen')).slice(0, 4).map(d => ({ dogId: d.id, cls: null }));
}
async function autoRun(team) {
  if (!startRun(team || autoTeam())) return null;
  for (let guard = 0; guard < 300 && S.run; guard++) {
    const run = S.run;
    if (run.screen === 'map') {
      const opts = run.nodes[run.step];
      const hurtAvg = alive().reduce((s, pm) => s + pm.hp / maxHpOf(pm), 0) / Math.max(1, alive().length);
      let i = Math.floor(rnd() * opts.length);
      const rest = opts.findIndex(o => o.t === 'hvil'); if (rest >= 0 && hurtAvg < 0.6) i = rest;
      chooseNode(i);
    } else if (run.screen === 'battle') {
      if (!run.battle.over) await simBattle(run.battle);
      if (!run.battle.over) run.battle.over = 'loss';
      finishBattle(); continueAfterBattle();
    } else if (run.screen === 'event') {
      if (!run.event.result) { const ev = EVENTS.find(e => e.id === run.event.id); const ok = ev.opts.map((o, j) => j).filter(j => !ev.opts[j].need || ev.opts[j].need()); chooseEvent(pick(ok)); }
      else continueEvent();
    } else if (run.screen === 'levelup') chooseOffer(Math.floor(rnd() * run.levelQueue[0].offers.length));
    else if (run.screen === 'end') { const res = run.result; closeRun(); return res; }
  }
  return { kind: 'stuck' };
}
