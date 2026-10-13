// ---------- Kampmotor ----------
const DIRS = [[1, 0], [-1, 0], [0, 1], [0, -1]];
const inB = (B, x, y) => x >= 0 && y >= 0 && x < B.w && y < B.h;
const tileAt = (B, x, y) => B.tiles[y * B.w + x];
const unitAt = (B, x, y) => B.units.find(u => !u.dead && u.x === x && u.y === y);
const foesOf = (B, u) => B.units.filter(o => !o.dead && !o.down && o.side !== u.side);
const isFree = (B, x, y) => inB(B, x, y) && tileAt(B, x, y) === 0 && !unitAt(B, x, y);
function say(B, txt) { B.log.push(txt); if (B.log.length > 40) B.log.shift(); }
function fx(B, t, u, v) { if (!HEADLESS) B.fx.push({ t, id: u.id, x: u.x, y: u.y, v }); }
function foesWithin(B, u, min, max) {
  return foesOf(B, u).filter(o => { const d = man(u.x, u.y, o.x, o.y); return d >= min && d <= max; }).map(o => ({ x: o.x, y: o.y }));
}
const self = u => [{ x: u.x, y: u.y }];

const ACTIONS = {
  bitt: { name: 'Bitt', cd: 0, desc: 'Biter en fiende inntil seg.', val: u => `${u.melee} skade`,
    targets: (B, u) => foesWithin(B, u, 1, u.reach),
    exec(B, u, x, y) { strike(B, u, unitAt(B, x, y), u.melee, { melee: true }); } },
  nafs: { name: 'Nafs', cd: 0, desc: 'Et lite bitt i en fiende inntil seg.', val: u => `${Math.max(1, u.melee - 1)} skade`,
    targets: (B, u) => foesWithin(B, u, 1, u.reach),
    exec(B, u, x, y) { strike(B, u, unitAt(B, x, y), Math.max(1, u.melee - 1), { melee: true }); } },
  pinne: { name: 'Kast pinne', cd: 0, desc: 'Treffer en fiende 1-4 ruter unna.', val: u => `${u.ranged} skade`,
    targets: (B, u) => foesWithin(B, u, 1, 4),
    exec(B, u, x, y) { strike(B, u, unitAt(B, x, y), u.ranged, {}); } },
  gnist: { name: 'Gnistsnute', cd: 0, desc: 'Magi 1-3 ruter unna. Kan ikke unnvikes.', val: u => `${u.magic} skade`,
    targets: (B, u) => foesWithin(B, u, 1, 3),
    exec(B, u, x, y) { strike(B, u, unitAt(B, x, y), u.magic, { magic: true }); } },
  storm: { name: 'Stormløp', cd: 2, desc: 'Løper i rett linje mot en fiende 2-5 ruter unna og biter.', val: u => `${u.melee + 2} skade`,
    targets(B, u) {
      const out = [];
      for (const o of foesOf(B, u)) {
        if (o.x !== u.x && o.y !== u.y) continue;
        const d = man(u.x, u.y, o.x, o.y); if (d < 2 || d > 5) continue;
        const sx = Math.sign(o.x - u.x), sy = Math.sign(o.y - u.y); let ok = true;
        for (let i = 1; i < d; i++) if (!isFree(B, u.x + sx * i, u.y + sy * i)) { ok = false; break; }
        if (ok) out.push({ x: o.x, y: o.y });
      }
      return out;
    },
    exec(B, u, x, y) { const sx = Math.sign(x - u.x), sy = Math.sign(y - u.y); u.x = x - sx; u.y = y - sy; say(B, `${u.name} stormer fram!`); strike(B, u, unitAt(B, x, y), u.melee + 2, { melee: true }); } },
  vakt: { name: 'Vaktbjeff', cd: 2, self: true, desc: 'Får 4 skjold. Fiender i nærheten går etter vokteren.', val: () => '4 skjold',
    targets: (B, u) => self(u),
    exec(B, u) { u.shield += 4; u.taunt = true; say(B, `${u.name} bjeffer: VOFF! Kom igjen!`); fx(B, 'shield', u, 4); } },
  apport: { name: 'Apport!', cd: 1, desc: 'Treffer 1-4 ruter unna og dytter målet ett hakk bakover.', val: u => `${u.ranged + 1} skade`,
    targets: (B, u) => foesWithin(B, u, 1, 4),
    exec(B, u, x, y) { const t = unitAt(B, x, y); strike(B, u, t, u.ranged + 1, {}); if (t && !t.dead) push(B, u, t); } },
  maane: { name: 'Månehyl', cd: 2, area: true, desc: 'Treffer alle i et 3x3-område opptil 3 ruter unna, også egne hunder.', val: u => `${u.magic} skade`,
    targets(B, u) {
      const out = [];
      for (let y = 0; y < B.h; y++) for (let x = 0; x < B.w; x++) if (man(u.x, u.y, x, y) <= 3) out.push({ x, y });
      return out;
    },
    exec(B, u, x, y) {
      say(B, `${u.name} hyler mot månen!`);
      for (const o of B.units.slice()) if (o !== u && !o.dead && !o.down && Math.abs(o.x - x) <= 1 && Math.abs(o.y - y) <= 1) strike(B, u, o, u.magic, { magic: true });
    } },
  slikk: { name: 'Slikk sår', cd: 1, ally: true, desc: 'Helbreder seg selv eller en hund inntil seg. Vekker hunder som ligger nede.', val: u => `+${u.heal} helse`,
    targets: (B, u) => B.units.filter(o => o.side === 'dog' && !o.dead && man(u.x, u.y, o.x, o.y) <= 1 && o.hp < o.maxHp).map(o => ({ x: o.x, y: o.y })),
    exec(B, u, x, y) { const t = unitAt(B, x, y); if (t) { say(B, `${u.name} slikker ${t === u ? 'sine egne' : t.name + ' sine'} sår.`); healUnit(B, t, u.heal); } } },
  halespinn: { name: 'Halespinn', cd: 2, self: true, desc: 'Treffer alle fiender rundt seg, også på skrå.', val: u => `${Math.max(1, u.melee - 1)} skade`,
    targets: (B, u) => foesOf(B, u).some(o => Math.max(Math.abs(o.x - u.x), Math.abs(o.y - u.y)) <= 1) ? self(u) : [],
    exec(B, u) { say(B, `${u.name} jager halen sin i full fart!`); for (const o of foesOf(B, u)) if (Math.max(Math.abs(o.x - u.x), Math.abs(o.y - u.y)) <= 1) strike(B, u, o, Math.max(1, u.melee - 1), { melee: true }); } },
  grav: { name: 'Grav tunnel', cd: 2, desc: 'Graver seg til en ledig rute opptil 5 ruter unna.', val: () => 'flytt',
    targets(B, u) { const out = []; for (let y = 0; y < B.h; y++) for (let x = 0; x < B.w; x++) { const d = man(u.x, u.y, x, y); if (d >= 1 && d <= 5 && isFree(B, x, y)) out.push({ x, y }); } return out; },
    exec(B, u, x, y) { u.x = x; u.y = y; say(B, `${u.name} graver seg under bakken og dukker opp et annet sted.`); } },
  baesj: { name: 'Legg bæsj', cd: 2, desc: 'Lager en hindring ved siden av seg. Fiender inntil den tar 1 skade hver runde.', val: () => 'hindring',
    targets: (B, u) => DIRS.map(([dx, dy]) => ({ x: u.x + dx, y: u.y + dy })).filter(t => isFree(B, t.x, t.y)),
    exec(B, u, x, y) { B.tiles[y * B.w + x] = 2; say(B, `${u.name} legger en bæsj. Det lukter fryktelig.`); } },
  rull: { name: 'Rull i gresset', cd: 3, self: true, desc: 'Helbreder seg selv.', val: u => `+${u.selfHeal} helse`,
    targets: (B, u) => u.hp < u.maxHp ? self(u) : [],
    exec(B, u) { say(B, `${u.name} ruller seg i gresset.`); healUnit(B, u, u.selfHeal); } },
  skremme: { name: 'Skremmebjeff', cd: 1, self: true, desc: 'Fiender inntil hunden tar 1 skade og dyttes ett hakk unna.', val: () => '1 skade',
    targets: (B, u) => foesWithin(B, u, 1, 1).length ? self(u) : [],
    exec(B, u) { say(B, `${u.name} bjeffer så det runger!`); for (const o of foesOf(B, u)) if (man(u.x, u.y, o.x, o.y) === 1) { hurt(B, o, 1, false); if (!o.dead) push(B, u, o); } } },
  loppe: { name: 'Loppeskyss', cd: 1, desc: 'Gir en fiende 1-2 ruter unna lopper: 1 skade per runde i 3 runder.', val: () => '3 skade over tid',
    targets: (B, u) => foesWithin(B, u, 1, 2),
    exec(B, u, x, y) { const t = unitAt(B, x, y); if (t) { t.poison = 3; say(B, `${u.name} rister lopper over på ${t.name}.`); } } },
  glefs: { name: 'Dobbeltglefs', cd: 1, desc: 'Biter samme fiende to ganger.', val: u => `2 x ${Math.max(1, u.melee - 1)} skade`,
    targets: (B, u) => foesWithin(B, u, 1, u.reach),
    exec(B, u, x, y) { const t = unitAt(B, x, y); strike(B, u, t, Math.max(1, u.melee - 1), { melee: true }); if (t && !t.dead && !u.down) strike(B, u, t, Math.max(1, u.melee - 1), { melee: true }); } },
};
const abil = id => ACTIONS[id] || PASSIVES[id];

function strike(B, src, tgt, base, o = {}) {
  if (!tgt || tgt.dead || tgt.down) return;
  if (!o.magic && chance(tgt.dodge || 0)) { say(B, `${tgt.name} unnviker ${src.name}.`); fx(B, 'miss', tgt, 0); return; }
  let dmg = base, crit = false;
  if (chance(src.crit || 0)) { dmg *= 2; crit = true; }
  say(B, `${src.name} treffer ${tgt.name} for ${dmg}${crit ? ' (kritisk!)' : ''}.`);
  hurt(B, tgt, dmg, crit);
  if (o.melee && tgt.thorns && !src.dead && !src.down) { say(B, `Au! ${src.name} stikker seg på pigghåret.`); hurt(B, src, tgt.thorns, false); }
  if (o.poison && !tgt.dead && !tgt.down) tgt.poison = 3;
}
function hurt(B, tgt, dmg, crit) {
  if (tgt.dead || tgt.down) return;
  if (tgt.shield > 0) { const a = Math.min(tgt.shield, dmg); tgt.shield -= a; dmg -= a; }
  tgt.hp = Math.max(0, tgt.hp - dmg);
  fx(B, crit ? 'crit' : 'dmg', tgt, dmg);
  if (tgt.hp <= 0) {
    if (tgt.side === 'dog') { tgt.down = true; tgt.poison = 0; tgt.taunt = false; tgt.shield = 0; tgt.acted = true; say(B, `${tgt.name} ligger nede!`); }
    else { tgt.dead = true; say(B, `${tgt.name} er beseiret.`); }
  }
  checkOver(B);
}
function healUnit(B, t, amt) {
  const before = t.hp;
  t.hp = Math.min(t.maxHp, t.hp + amt);
  if (t.down && t.hp > 0) { t.down = false; t.moved = true; t.acted = true; say(B, `${t.name} reiser seg igjen!`); }
  fx(B, 'heal', t, t.hp - before);
}
function push(B, src, tgt) {
  if (tgt.dead || tgt.down) return;
  if (tgt.boss) { say(B, `${tgt.name} rikker seg ikke.`); return; }
  let dx = Math.sign(tgt.x - src.x), dy = Math.sign(tgt.y - src.y);
  if (dx && dy) { if (Math.abs(tgt.x - src.x) >= Math.abs(tgt.y - src.y)) dy = 0; else dx = 0; }
  if (!dx && !dy) return;
  const nx = tgt.x + dx, ny = tgt.y + dy;
  if (isFree(B, nx, ny)) { tgt.x = nx; tgt.y = ny; }
  else { say(B, `${tgt.name} smeller inn i noe.`); hurt(B, tgt, 1, false); }
}
function checkOver(B) {
  if (B.over) return;
  if (!B.units.some(u => u.side === 'enemy' && !u.dead)) B.over = 'win';
  else if (!B.units.some(u => u.side === 'dog' && !u.down && !u.dead)) B.over = 'loss';
}

// Bevegelse: bredde-først-søk. Egne enheter kan passeres, fiender ikke. Flygere går over alt.
function reach(B, u) {
  const map = new Map(), ends = new Map();
  map.set(u.x + ',' + u.y, { d: 0, prev: null });
  const q = [[u.x, u.y]];
  while (q.length) {
    const [x, y] = q.shift(); const d = map.get(x + ',' + y).d;
    if (d >= u.move) continue;
    for (const [dx, dy] of DIRS) {
      const nx = x + dx, ny = y + dy; if (!inB(B, nx, ny)) continue;
      const k = nx + ',' + ny; if (map.has(k)) continue;
      const t = tileAt(B, nx, ny), o = unitAt(B, nx, ny);
      if (!u.fly && t !== 0) continue;
      if (!u.fly && o && o.side !== u.side && !o.down) continue; // nede hunder kan man gå over, men ikke stå på
      map.set(k, { d: d + 1, prev: x + ',' + y }); q.push([nx, ny]);
      if (t === 0 && !o) ends.set(k, d + 1);
    }
  }
  return { map, ends };
}
function pathTo(map, x, y) {
  const out = []; let k = x + ',' + y;
  while (k) { const n = map.get(k); if (!n || n.prev === null) break; out.push(k.split(',').map(Number)); k = n.prev; }
  return out.reverse();
}
// Avstandskart fra målene, uten å ta hensyn til enheter (de flytter seg uansett).
function distField(B, targets, fly) {
  const f = new Array(B.w * B.h).fill(-1); const q = [];
  for (const t of targets) { f[t.y * B.w + t.x] = 0; q.push([t.x, t.y]); }
  while (q.length) {
    const [x, y] = q.shift(); const d = f[y * B.w + x];
    for (const [dx, dy] of DIRS) {
      const nx = x + dx, ny = y + dy; if (!inB(B, nx, ny)) continue;
      const i = ny * B.w + nx; if (f[i] >= 0) continue;
      if (!fly && B.tiles[i] !== 0) continue;
      f[i] = d + 1; q.push([nx, ny]);
    }
  }
  return f;
}

function makeDogUnit(B, pm, x, y) {
  const d = dogById(pm.dogId), D = derive(d, pm.cls), C = CLASSES[pm.cls];
  const actions = [C.attack, C.skill, ...d.learned.filter(a => ACTIONS[a])];
  return Object.assign({
    id: 'u' + (B.uid++), side: 'dog', dogId: d.id, name: d.name, cls: pm.cls, x, y,
    hp: clamp(pm.hp, 1, D.maxHp), actions, cds: {}, shield: 0, taunt: false, poison: 0,
    down: false, dead: false, moved: false, acted: false, from: null,
  }, D);
}
function makeEnemy(B, type, x, y, scale) {
  const T = ENEMIES[type], hp = Math.round(T.hp * scale.hp);
  return {
    id: 'e' + (B.uid++), side: 'enemy', type, name: T.name, x, y, hp, maxHp: hp, dmg: T.dmg + scale.dmg,
    move: T.move, range: T.range, dodge: T.dodge, crit: 0.05, fly: !!T.fly, boss: !!T.boss, poisonAtk: !!T.poison,
    poison: 0, shield: 0, dead: false, acted: false, thorns: 0,
  };
}
function connected(tiles, W, H) {
  const start = tiles.indexOf(0); if (start < 0) return false;
  const seen = new Set([start]); const q = [start];
  while (q.length) {
    const i = q.shift(); const x = i % W, y = (i / W) | 0;
    for (const [dx, dy] of DIRS) {
      const nx = x + dx, ny = y + dy; if (nx < 0 || ny < 0 || nx >= W || ny >= H) continue;
      const j = ny * W + nx; if (tiles[j] !== 0 || seen.has(j)) continue;
      seen.add(j); q.push(j);
    }
  }
  return seen.size === tiles.filter(t => t === 0).length;
}
function encounter(node, step) {
  if (node.t === 'boss') return S.heat > 0 ? ['katt', 'katt', 'hvese'] : ['katt', 'katt'];
  const list = []; let budget = 5 + step * 3;
  if (node.t === 'elite') { list.push('kloakk'); budget = Math.max(3, budget - 6); }
  const pool = step === 0 ? ['rotte', 'rotte', 'maake'] : step === 1 ? ['rotte', 'maake', 'hvese', 'katt'] : ['rotte', 'maake', 'hvese', 'katt', 'katt'];
  let guard = 0;
  while (budget >= 2 && list.length < 6 && guard++ < 60) { const t = pick(pool); if (ENEMIES[t].cost <= budget) { list.push(t); budget -= ENEMIES[t].cost; } }
  return list;
}
function makeBattle(node, step) {
  S.bcount = (S.bcount || 0) + 1;
  const W = 8, H = 6;
  let tiles, deco;
  for (let tries = 0; tries < 40; tries++) {
    tiles = new Array(W * H).fill(0); deco = new Array(W * H).fill(0);
    const n = ri(4, 7);
    for (let i = 0; i < n; i++) { const x = ri(2, 5), y = ri(0, H - 1); tiles[y * W + x] = 1; deco[y * W + x] = ri(0, 2); }
    if (connected(tiles, W, H)) break;
    tiles.fill(0);
  }
  const scale = { hp: 1 + 0.06 * step + 0.2 * S.heat, dmg: Math.floor(S.heat / 2) + (step >= 4 ? 1 : 0) };
  const B = { id: 'b' + S.bcount, w: W, h: H, tiles, deco, units: [], uid: 1, round: 0, phase: 'player', log: [], fx: [], over: null, kind: node.t, place: node.place, scale, ticked: false };
  const dogSpots = []; for (let y = 0; y < H; y++) for (let x = 0; x <= 1; x++) dogSpots.push([x, y]);
  shuffle(dogSpots);
  alive().forEach((pm, i) => { const [x, y] = dogSpots[i]; B.units.push(makeDogUnit(B, pm, x, y)); });
  let foeSpots = []; for (let y = 0; y < H; y++) for (let x = 6; x <= 7; x++) foeSpots.push([x, y]);
  if (node.t === 'boss') {
    const by = ri(2, 3); B.units.push(makeEnemy(B, 'konge', 7, by, scale));
    foeSpots = foeSpots.filter(([x, y]) => !(x === 7 && y === by));
  }
  shuffle(foeSpots);
  for (const t of encounter(node, step)) { const sp = foeSpots.pop(); if (sp) B.units.push(makeEnemy(B, t, sp[0], sp[1], scale)); }
  say(B, `${B.place}: ${B.units.filter(u => u.side === 'enemy').map(u => u.name).join(', ')}.`);
  startPlayerPhase(B);
  return B;
}

function startPlayerPhase(B) {
  B.round++; B.phase = 'player'; B.ticked = false;
  B.units = B.units.filter(u => !u.dead);
  for (const u of B.units) {
    if (u.side !== 'dog') continue;
    u.shield = 0; u.taunt = false; u.from = null;
    for (const k in u.cds) if (u.cds[k] > 0) u.cds[k]--;
    if (u.poison > 0 && !u.down) { u.poison--; say(B, `${u.name} klør seg (lopper).`); hurt(B, u, 1, false); }
    u.moved = u.down; u.acted = u.down;
  }
  if (!B.over) say(B, `Runde ${B.round}. Din tur.`);
}
function execAction(B, u, id, x, y) {
  const A = ACTIONS[id];
  A.exec(B, u, x, y);
  if (A.cd) u.cds[id] = A.cd + 1;
  u.acted = true; u.moved = true;
  checkOver(B);
}

// ---------- Fiendenes hjerne ----------
function planEnemy(B, e) {
  const dogs = B.units.filter(u => u.side === 'dog' && !u.down && !u.dead);
  if (!dogs.length) return { path: [], target: null };
  const R = reach(B, e);
  const spots = [[e.x, e.y, 0], ...[...R.ends].map(([k, d]) => [...k.split(',').map(Number), d])];
  const taunters = dogs.filter(d => d.taunt && man(e.x, e.y, d.x, d.y) <= e.move + e.range[1] + 2);
  const pool = taunters.length ? taunters : dogs;
  let best = null;
  for (const [x, y, steps] of spots) {
    for (const d of pool) {
      const dist = man(x, y, d.x, d.y);
      if (dist < e.range[0] || dist > e.range[1]) continue;
      const score = -d.hp * 2 + (e.range[1] > 1 ? dist * 3 : 0) - steps * 0.1 + rnd() * 0.5;
      if (!best || score > best.score) best = { score, x, y, target: d };
    }
  }
  if (best) return { path: pathTo(R.map, best.x, best.y), target: best.target };
  const field = distField(B, pool, e.fly);
  let bt = null;
  for (const [x, y, steps] of spots) {
    const f = field[y * B.w + x]; const v = f < 0 ? 999 : f;
    if (!bt || v < bt.v || (v === bt.v && steps < bt.steps)) bt = { v, x, y, steps };
  }
  return { path: bt ? pathTo(R.map, bt.x, bt.y) : [], target: null };
}
function nearPoop(B, e) { return DIRS.some(([dx, dy]) => inB(B, e.x + dx, e.y + dy) && tileAt(B, e.x + dx, e.y + dy) === 2); }
function freeTiles(B) { const out = []; for (let y = 0; y < B.h; y++) for (let x = 0; x < B.w; x++) if (isFree(B, x, y)) out.push([x, y]); return out; }

const wait = ms => (SPEED <= 0 || HEADLESS) ? Promise.resolve() : new Promise(r => setTimeout(r, ms * SPEED));
async function animatePath(B, u, path) {
  for (const [x, y] of path) { u.x = x; u.y = y; render(); await wait(85); }
}
async function enemyAct(B, e) {
  if (e.boss && B.round % 3 === 0) {
    const n = B.units.filter(o => o.side === 'enemy' && !o.dead).length;
    if (n < 7) {
      const spots = shuffle(freeTiles(B).filter(([x]) => x >= 5)).slice(0, 2);
      for (const [x, y] of spots) { const c = makeEnemy(B, 'katt', x, y, B.scale); c.acted = true; B.units.push(c); }
      if (spots.length) { say(B, 'Kattekongen roper på hjelp! Nye katter dukker opp.'); render(); await wait(400); return; }
    }
  }
  const plan = planEnemy(B, e);
  if (plan.path.length) await animatePath(B, e, plan.path);
  if (plan.target && !plan.target.down && !e.dead) {
    await wait(120);
    strike(B, e, plan.target, e.dmg, { melee: e.range[1] === 1, poison: e.poisonAtk });
    render(); await wait(280);
  }
}
async function enemyPhase(B) {
  B.phase = 'enemy'; UI.busy = true; render();
  if (!B.ticked) {
    B.ticked = true;
    for (const e of B.units.filter(o => o.side === 'enemy' && !o.dead)) {
      if (e.poison > 0) { e.poison--; say(B, `${e.name} klør seg (lopper).`); hurt(B, e, 1, false); }
      if (!e.dead && nearPoop(B, e)) { say(B, `${e.name} kveles av bæsjestank.`); hurt(B, e, 1, false); }
    }
    render(); await wait(250);
  }
  for (const e of B.units.filter(o => o.side === 'enemy' && !o.dead && !o.acted)) {
    if (B.over) break;
    if (e.dead) continue;
    await enemyAct(B, e);
    e.acted = true;
    render(); await wait(120);
  }
  for (const e of B.units) if (e.side === 'enemy') e.acted = false;
  UI.busy = false;
  if (!B.over) startPlayerPhase(B);
  render();
}

// ---------- Autospiller (brukes av testene og til balansering) ----------
function actionDamage(u, id) {
  return { bitt: u.melee, nafs: Math.max(1, u.melee - 1), pinne: u.ranged, gnist: u.magic, storm: u.melee + 2, apport: u.ranged + 1, glefs: 2 * Math.max(1, u.melee - 1) }[id] || 0;
}
function scoreAction(B, u, id, t) {
  const tu = unitAt(B, t.x, t.y);
  const adj8 = o => Math.max(Math.abs(o.x - u.x), Math.abs(o.y - u.y)) <= 1;
  switch (id) {
    case 'slikk': if (!tu) return 0; if (tu.down) return 30; return (tu.maxHp - tu.hp) >= 3 ? (tu.maxHp - tu.hp) * 1.5 : 0;
    case 'rull': return (u.maxHp - u.hp) >= 5 ? 6 : 0;
    case 'vakt': return foesOf(B, u).some(e => man(e.x, e.y, u.x, u.y) <= 4) ? 5 : 0;
    case 'grav': return 0;
    case 'baesj': return foesOf(B, u).some(e => man(e.x, e.y, t.x, t.y) <= 1) ? 2.5 : 0;
    case 'loppe': return tu && !tu.poison ? Math.min(3, tu.hp) : 0;
    case 'maane': {
      let s = 0;
      for (const o of B.units) if (!o.dead && !o.down && o !== u && Math.abs(o.x - t.x) <= 1 && Math.abs(o.y - t.y) <= 1)
        s += o.side === 'enemy' ? Math.min(o.hp, u.magic) + (o.hp <= u.magic ? 4 : 0) : -u.magic * 2;
      return s;
    }
    case 'halespinn': { let s = 0; for (const e of foesOf(B, u)) if (adj8(e)) s += Math.min(e.hp, Math.max(1, u.melee - 1)) + 0.5; return s > 3 ? s : 0; }
    case 'skremme': { let s = 0; for (const e of foesOf(B, u)) if (man(e.x, e.y, u.x, u.y) === 1) s += 1.5; return s; }
    default: {
      if (!tu || tu.side === u.side) return 0;
      const d = actionDamage(u, id);
      return Math.min(tu.hp, d) + (tu.hp <= d ? 5 : 0) + (ACTIONS[id].cd ? 0.5 : 0);
    }
  }
}
function autoDog(B, u) {
  const R = reach(B, u);
  const ox = u.x, oy = u.y;
  const spots = [[ox, oy], ...[...R.ends.keys()].map(k => k.split(',').map(Number))];
  let best = null;
  for (const [x, y] of spots) {
    u.x = x; u.y = y;
    for (const id of u.actions) {
      if ((u.cds[id] || 0) > 0) continue;
      for (const t of ACTIONS[id].targets(B, u)) {
        const sc = scoreAction(B, u, id, t) - man(ox, oy, x, y) * 0.01;
        if (sc > 0 && (!best || sc > best.sc)) best = { sc, x, y, id, t };
      }
    }
  }
  u.x = ox; u.y = oy;
  if (best) { u.x = best.x; u.y = best.y; execAction(B, u, best.id, best.t.x, best.t.y); return; }
  const foes = foesOf(B, u);
  if (foes.length) {
    const field = distField(B, foes, false); let bt = null;
    for (const [x, y] of spots) { const f = field[y * B.w + x]; const v = f < 0 ? 999 : f; if (!bt || v < bt.v) bt = { v, x, y }; }
    if (bt) { u.x = bt.x; u.y = bt.y; }
  }
  u.acted = true; u.moved = true;
}
function autoDogs(B) {
  for (const u of B.units.filter(o => o.side === 'dog' && !o.down && !o.acted)) { if (B.over) return; if (!u.down) autoDog(B, u); }
}
async function simBattle(B) {
  while (!B.over && B.round <= 60) {
    autoDogs(B);
    if (B.over) break;
    await enemyPhase(B);
  }
  return B;
}
function battleProblems(B) {
  const errs = [], seen = new Set();
  for (const u of B.units) {
    if (u.dead) continue;
    const k = u.x + ',' + u.y;
    if (seen.has(k)) errs.push(`to enheter på ${k}`); seen.add(k);
    if (!inB(B, u.x, u.y)) errs.push(`${u.name} utenfor brettet`);
    else if (tileAt(B, u.x, u.y) !== 0) errs.push(`${u.name} står på hindring ${k}`);
    if (!Number.isFinite(u.hp) || u.hp < 0 || u.hp > u.maxHp) errs.push(`${u.name} har ugyldig helse ${u.hp}/${u.maxHp}`);
  }
  return errs;
}
