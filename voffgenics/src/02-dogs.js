// ---------- Tilstand ----------
const SAVE_KEY = 'voffgenics-save-v1';
let S = null;
let HEADLESS = false; // brukes av testene: ingen tegning, ingen lagring
let SPEED = 1;        // animasjonsfart; 0 i tester
const UI = { pairing: null, confirm: null, setup: [], sel: null, mode: 'move', hover: null, busy: false, info: null, toastTimer: 0 };

function newGame(seedVal) {
  seed(seedVal ?? (Date.now() % 2147483647));
  S = { v: 1, day: 1, bones: 20, wins: 0, heat: 0, nextId: 1, dogs: [], reg: {}, grave: [], pairs: [], news: [], screen: 'kennel', run: null, intro: true, bcount: 0 };
  for (const sx of ['M', 'M', 'M', 'F', 'F', 'F']) addDog(makeStray(sx));
  S.news = ['Seks gatehunder har flyttet inn i kennelen. Par dem, eller send dem på tur.'];
  UI.pairing = null; UI.setup = []; UI.sel = null; UI.mode = 'move'; UI.confirm = null;
}
function addDog(d) { S.dogs.push(d); S.reg[d.id] = { name: d.name, mom: d.mom, dad: d.dad, sex: d.sex }; return d; }
function newId() { return 'd' + (S.nextId++); }
function regNo(n, day) { return `VK ${String(n).padStart(4, '0')}/${String(day).padStart(2, '0')}`; }
const dogById = id => S.dogs.find(d => d.id === id);
const roman = i => ['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X'][i] || String(i);
function freshName(sex) {
  const list = sex === 'F' ? NAMES_F : NAMES_M;
  const used = new Set(S.dogs.map(d => d.name));
  const free = list.filter(n => !used.has(n));
  if (free.length) return pick(free);
  const base = pick(list); let i = 2;
  while (used.has(`${base} ${roman(i)}`)) i++;
  return `${base} ${roman(i)}`;
}
function randomLook() {
  const fur = ri(0, FURS.length - 1);
  let patc = ri(0, FURS.length - 1); if (patc === fur) patc = (patc + 3) % FURS.length;
  return { fur, patc, pat: pick(PATTERNS), ears: pick(EARS), snout: pick(SNOUTS), eye: ri(0, EYES.length - 1) };
}
function randomMut(pGood, exclude = []) {
  const pool = (chance(pGood) ? GOOD_MUTS : BAD_MUTS).filter(m => !exclude.includes(m));
  return pool.length ? pick(pool) : null;
}
function makeStray(sex) {
  const id = newId(); const n = S.nextId - 1;
  sex = sex || (chance(0.5) ? 'M' : 'F');
  const stats = {}; for (const k of STATS) stats[k] = ri(2, 6);
  const muts = []; if (chance(0.25)) muts.push(randomMut(0.7));
  const learned = []; if (chance(0.2)) learned.push(pick(LEARNED));
  return {
    id, reg: regNo(n, S.day), name: freshName(sex), sex, stats, look: randomLook(), muts, learned,
    level: 1, xp: 0, status: 'voksen', bornDay: S.day, mom: null, dad: null, gen: 0, kurs: false, scars: 0, runs: 0, wins: 0,
  };
}

// ---------- Egenskaper ----------
function eff(d, k) { let v = d.stats[k]; for (const m of d.muts) v += (MUTS[m].mods[k] || 0); return clamp(v, 1, 12); }
function derive(d, cls) {
  const st = k => eff(d, k), has = a => d.learned.includes(a), mut = m => d.muts.includes(m);
  return {
    maxHp: 6 + st('uth') * 2 + (cls ? CLASSES[cls].hp : 0) + (has('tykkpels') ? 4 : 0),
    melee: 1 + Math.ceil(st('sty') / 2) + (has('klor') ? 1 : 0) + (mut('tenner') ? 1 : 0),
    ranged: 1 + Math.floor(st('smi') / 2),
    magic: 1 + Math.floor(st('int') / 2),
    heal: 2 + Math.floor(st('int') / 2),
    selfHeal: 3 + Math.floor(st('int') / 3),
    move: 2 + Math.floor(st('hur') / 3) + (has('poter') ? 1 : 0),
    dodge: Math.min(0.4, st('smi') * 0.03),
    crit: Math.min(0.6, 0.03 + st('fla') * 0.04 + (has('snute') ? 0.1 : 0)),
    save: Math.min(0.95, 0.45 + st('fla') * 0.05 + (has('seig') ? 0.25 : 0)),
    reach: mut('kjempetunge') ? 2 : 1,
    thorns: mut('pigg') ? 1 : 0,
  };
}
function bump(d, k, n) { d.stats[k] = clamp(d.stats[k] + n, 1, 10); }
function addMut(d, m) { if (m && !d.muts.includes(m) && d.muts.length < 3) { d.muts.push(m); return true; } return false; }
function scar(d) {
  const ks = STATS.filter(k => d.stats[k] > 1);
  if (!ks.length) return 'uth';
  const k = pick(ks); d.stats[k]--; d.scars++; return k;
}
function killDog(d, cause) {
  S.dogs = S.dogs.filter(x => x.id !== d.id);
  S.pairs = S.pairs.filter(p => !p.includes(d.id));
  S.grave.unshift({ name: d.name, reg: d.reg, day: S.day, cause, level: d.level, gen: d.gen });
}

// ---------- Slekt og avl ----------
function parentsOf(id) { const r = S.reg[id]; return r ? [r.mom, r.dad].filter(Boolean) : []; }
function relation(a, b) {
  const pa = parentsOf(a), pb = parentsOf(b);
  if (pa.includes(b) || pb.includes(a)) return 'naer';
  if (pa.some(x => pb.includes(x))) return 'naer';
  const ga = pa.flatMap(parentsOf), gb = pb.flatMap(parentsOf);
  if (ga.includes(b) || gb.includes(a)) return 'fjern';
  if (ga.some(x => gb.includes(x))) return 'fjern';
  if (pa.some(x => gb.includes(x)) || pb.some(x => ga.includes(x))) return 'fjern';
  return 'ingen';
}
const REL_TXT = { naer: 'Nær slekt: stor risiko for defekter', fjern: 'Fjern slekt: litt risiko for defekter', ingen: 'Ikke i slekt' };

function makePuppy(mom, dad) {
  const rel = relation(mom.id, dad.id);
  const risk = rel === 'naer' ? 0.55 : rel === 'fjern' ? 0.2 : 0;
  const id = newId(); const n = S.nextId - 1;
  const sex = chance(0.5) ? 'M' : 'F';
  const stats = {};
  for (const k of STATS) {
    const hi = Math.max(mom.stats[k], dad.stats[k]), lo = Math.min(mom.stats[k], dad.stats[k]);
    const v = chance(0.6) ? hi : lo;
    let drift = 0;
    if (chance(0.15)) drift = chance(0.5) ? 1 : -1;
    if (risk && chance(risk * 0.5)) drift = -1;
    stats[k] = clamp(v + drift, 1, 10);
  }
  const pool = [...new Set([...mom.learned, ...dad.learned])];
  const learned = [];
  if (pool.length && chance(0.7)) {
    learned.push(pool.splice(Math.floor(rnd() * pool.length), 1)[0]);
    if (pool.length && chance(0.25)) learned.push(pool.splice(Math.floor(rnd() * pool.length), 1)[0]);
  }
  let muts = [];
  for (const m of new Set([...mom.muts, ...dad.muts])) if (chance(0.5)) muts.push(m);
  let defect = null;
  if (risk && chance(risk)) { defect = randomMut(0, muts); if (defect) muts.push(defect); }
  if (chance(0.10)) { const m = randomMut(0.65, muts); if (m) muts.push(m); }
  if (muts.length > 3) muts = (defect ? [defect, ...shuffle(muts.filter(m => m !== defect))] : shuffle(muts)).slice(0, 3);
  const look = {};
  for (const g of ['fur', 'patc', 'pat', 'ears', 'snout', 'eye']) look[g] = chance(0.5) ? mom.look[g] : dad.look[g];
  if (chance(0.08)) look.fur = ri(0, FURS.length - 1);
  if (chance(0.08)) look.pat = pick(PATTERNS);
  if (chance(0.06)) look.ears = pick(EARS);
  return {
    id, reg: regNo(n, S.day + 1), name: freshName(sex), sex, stats, look, muts, learned,
    level: 1, xp: 0, status: 'valp', bornDay: S.day + 1, mom: mom.id, dad: dad.id,
    gen: Math.max(mom.gen, dad.gen) + 1, kurs: false, scars: 0, runs: 0, wins: 0, rel, defect,
  };
}
function litterSize() { const r = rnd(); return r < 0.45 ? 1 : r < 0.85 ? 2 : 3; }
const canBreed = d => d && (d.status === 'voksen' || d.status === 'veteran');
function pairedWith(id) { const p = S.pairs.find(p => p.includes(id)); return p ? (p[0] === id ? p[1] : p[0]) : null; }
function pairProblem(a, b) {
  if (!a || !b) return 'Finnes ikke';
  if (a.id === b.id) return 'Samme hund';
  if (!canBreed(b)) return b.status === 'valp' ? 'Er valp til i morgen' : 'Kan ikke pare seg';
  if (a.sex === b.sex) return 'Samme kjønn';
  if (pairedWith(b.id)) return 'Allerede paret';
  return null;
}

// Natten: valper vokser opp, parede hunder får valper, dagen går.
function nightFall() {
  const news = [];
  for (const d of S.dogs) if (d.status === 'valp') { d.status = 'voksen'; news.push(`${d.name} er blitt voksen og klar for tur.`); }
  for (const [a, b] of S.pairs) {
    const A = dogById(a), Bd = dogById(b);
    if (!A || !Bd) continue;
    const mom = A.sex === 'F' ? A : Bd, dad = A.sex === 'F' ? Bd : A;
    const free = CAP - S.dogs.length;
    if (free <= 0) { news.push(`Det var ikke plass til valpene til ${mom.name} og ${dad.name}.`); continue; }
    const n = Math.min(free, litterSize());
    const pups = [];
    for (let i = 0; i < n; i++) pups.push(addDog(makePuppy(mom, dad)));
    let line = `${mom.name} og ${dad.name} fikk ${n === 1 ? 'én valp' : n + ' valper'}: ${pups.map(p => p.name).join(', ')}.`;
    const def = pups.filter(p => p.defect);
    if (def.length) line += ` Innavl: ${def.map(p => `${p.name} fikk ${MUTS[p.defect].name.toLowerCase()}`).join(', ')}.`;
    news.push(line);
  }
  S.pairs = [];
  S.day++;
  if (!S.dogs.some(d => d.status === 'voksen' || d.status === 'valp') && S.dogs.length < CAP) {
    const s = addDog(makeStray());
    news.push(`En gatehund, ${s.name}, sto og ventet ved porten i morges.`);
  }
  S.news = news.length ? news : ['En rolig natt. Ingen nye valper.'];
}

// ---------- Portretter (tegnes fra genene) ----------
let svgN = 0;
function shade(hex, amt) {
  const n = parseInt(hex.slice(1), 16);
  let r = n >> 16, g = (n >> 8) & 255, b = n & 255;
  const t = amt < 0 ? 0 : 255, p = Math.abs(amt);
  r = Math.round((t - r) * p + r); g = Math.round((t - g) * p + g); b = Math.round((t - b) * p + b);
  return '#' + ((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1);
}
const INK = '#24180d';
function eyeSVG(cx, cy, r, c, off) {
  return `<circle cx="${cx}" cy="${cy}" r="${r}" fill="#fff" stroke-width="2"/>` +
    `<circle cx="${cx + off}" cy="${cy + 0.6}" r="${(r * 0.62).toFixed(2)}" fill="${c}" stroke="none"/>` +
    `<circle cx="${cx + off}" cy="${cy + 0.6}" r="${(r * 0.3).toFixed(2)}" fill="${INK}" stroke="none"/>` +
    `<circle cx="${(cx + off - r * 0.22).toFixed(2)}" cy="${(cy - r * 0.15).toFixed(2)}" r="${(r * 0.15).toFixed(2)}" fill="#fff" stroke="none"/>`;
}
function dogSVG(d, o = {}) {
  const L = d.look, M = new Set(d.muts), id = 'vc' + (svgN++);
  const hairless = M.has('harlos');
  const fur = hairless ? '#ebb7a8' : FURS[L.fur].c;
  const fur2 = hairless ? '#d99a8a' : FURS[L.patc].c;
  const earC = shade(fur, -0.2), muz = shade(fur, 0.5);
  const pup = d.status === 'valp';
  const sc = (M.has('kjempehode') ? 1.1 : 1) * (pup ? 0.86 : 1);
  const one = M.has('ettore');
  const ears = M.has('flaksorer') ? 'vinge' : L.ears;
  let s = `<svg class="portrait" viewBox="0 0 100 100" aria-hidden="true"><defs><clipPath id="${id}"><ellipse cx="50" cy="54" rx="31" ry="28"/></clipPath></defs>`;
  s += `<g transform="translate(50 ${pup ? 58 : 54}) scale(${sc}) translate(-50 -54)" stroke="${INK}" stroke-width="3" stroke-linejoin="round" stroke-linecap="round">`;
  if (ears === 'spiss') {
    s += `<path d="M24 44 L25 12 L45 30 Z" fill="${earC}"/><path d="M29 36 L29.5 21 L39 30 Z" fill="#e7a3a0" stroke="none"/>`;
    if (!one) s += `<path d="M76 44 L75 12 L55 30 Z" fill="${earC}"/><path d="M71 36 L70.5 21 L61 30 Z" fill="#e7a3a0" stroke="none"/>`;
  }
  if (ears === 'rund') { s += `<circle cx="27" cy="30" r="12" fill="${earC}"/>`; if (!one) s += `<circle cx="73" cy="30" r="12" fill="${earC}"/>`; }
  if (ears === 'vinge') {
    s += `<path d="M27 42 Q4 34 5 12 Q13 22 20 20 Q13 28 22 30 Q16 36 31 38 Z" fill="#f6f2ea"/>`;
    if (!one) s += `<path d="M73 42 Q96 34 95 12 Q87 22 80 20 Q87 28 78 30 Q84 36 69 38 Z" fill="#f6f2ea"/>`;
  }
  if (M.has('horn')) s += `<path d="M37 30 Q30 14 38 7 Q37 19 45 27 Z" fill="#efe3c8"/><path d="M63 30 Q70 14 62 7 Q63 19 55 27 Z" fill="#efe3c8"/>`;
  if (M.has('pigg')) s += `<path d="M27 38 L29 21 L36 30 L41 14 L47 27 L53 12 L58 27 L65 16 L69 32 Z" fill="${shade(fur2, -0.1)}"/>`;
  s += `<ellipse cx="50" cy="54" rx="31" ry="28" fill="${fur}"/>`;
  const pats = {
    flekker: '<circle cx="34" cy="40" r="6"/><circle cx="66" cy="63" r="7"/><circle cx="60" cy="34" r="4"/><circle cx="27" cy="64" r="4.5"/>',
    maske: '<ellipse cx="50" cy="47" rx="27" ry="10"/>',
    lapp: '<circle cx="63" cy="46" r="11"/>',
    blis: '<path d="M45 24 h10 l-1.5 32 h-7 Z"/>',
  };
  if (pats[L.pat]) s += `<g clip-path="url(#${id})" fill="${L.pat === 'blis' ? muz : fur2}" stroke="none">${pats[L.pat]}</g>`;
  s += `<ellipse cx="50" cy="54" rx="31" ry="28" fill="none"/>`;
  if (hairless) s += `<path d="M38 32 q12 -5 24 0 M41 37 q9 -4 18 0" fill="none" stroke-width="1.6"/>`;
  if (ears === 'heng') {
    s += `<ellipse cx="22" cy="52" rx="9" ry="18" transform="rotate(16 22 52)" fill="${earC}"/>`;
    if (!one) s += `<ellipse cx="78" cy="52" rx="9" ry="18" transform="rotate(-16 78 52)" fill="${earC}"/>`;
  }
  if (ears === 'lange') {
    s += `<ellipse cx="21" cy="62" rx="9" ry="25" transform="rotate(10 21 62)" fill="${earC}"/>`;
    if (!one) s += `<ellipse cx="79" cy="62" rx="9" ry="25" transform="rotate(-10 79 62)" fill="${earC}"/>`;
  }
  const long = L.snout === 'lang';
  s += long ? `<ellipse cx="50" cy="69" rx="14" ry="14" fill="${muz}" stroke-width="2.2"/>` : `<ellipse cx="50" cy="66" rx="17" ry="11.5" fill="${muz}" stroke-width="2.2"/>`;
  const glow = M.has('glod');
  const ec = glow ? '#ffd23a' : EYES[L.eye];
  const er = pup ? 6.6 : 5.5;
  if (M.has('kyklop')) {
    if (glow) s += `<circle cx="50" cy="45" r="14" fill="#ffe46b" opacity=".5" stroke="none"/>`;
    s += eyeSVG(50, 45, 9.5, ec, 0);
  } else {
    if (glow) s += `<circle cx="38" cy="47" r="9.5" fill="#ffe46b" opacity=".5" stroke="none"/><circle cx="62" cy="47" r="9.5" fill="#ffe46b" opacity=".5" stroke="none"/>`;
    const off = M.has('skjeloyd') ? 1.9 : 0;
    s += eyeSVG(38, 47, er, ec, off) + eyeSVG(62, 47, er, ec, -off);
  }
  if (M.has('treoye')) s += `<ellipse cx="50" cy="31" rx="4.4" ry="5.6" fill="#fff" stroke-width="2"/><circle cx="50" cy="31.6" r="2.7" fill="${ec}" stroke="none"/><circle cx="50" cy="31.6" r="1.25" fill="${INK}" stroke="none"/>`;
  const ny = long ? 62 : 60;
  s += M.has('hjertenese')
    ? `<path d="M50 ${ny + 6} C40 ${ny - 1} 43 ${ny - 7} 50 ${ny - 2} C57 ${ny - 7} 60 ${ny - 1} 50 ${ny + 6} Z" fill="#d6456a" stroke-width="2"/>`
    : `<ellipse cx="50" cy="${ny}" rx="6.2" ry="4.4" fill="${INK}"/><ellipse cx="48" cy="${ny - 1.5}" rx="1.8" ry="1" fill="#fff" stroke="none"/>`;
  const my = ny + 4.5;
  if (M.has('kjempetunge')) s += `<path d="M45 ${my + 4} Q45 ${my + 24} 50 ${my + 24} Q55 ${my + 24} 55 ${my + 4} Z" fill="#e8657e" stroke-width="2"/><path d="M50 ${my + 6} v10" stroke-width="1.4"/>`;
  s += M.has('skjevkjeve')
    ? `<path d="M50 ${my} v3 q-5 6 -11 1 M50 ${my + 3} q6 1 10 6" fill="none" stroke-width="2.4"/>`
    : `<path d="M50 ${my} v3 q-5 5 -10 1 M50 ${my + 3} q5 5 10 1" fill="none" stroke-width="2.4"/>`;
  if (M.has('tenner')) s += `<path d="M43 ${my + 4} l2 7 l2.5 -6 Z M53.5 ${my + 4.5} l2.5 6.5 l2 -7 Z" fill="#fff" stroke-width="1.6"/>`;
  if (M.has('lopper')) s += `<g fill="${INK}" stroke="none"><circle cx="30" cy="40" r="1.4"/><circle cx="70" cy="38" r="1.3"/><circle cx="25" cy="58" r="1.2"/><circle cx="74" cy="64" r="1.4"/><circle cx="58" cy="78" r="1.2"/></g>`;
  s += `</g>`;
  if (o.cls) s += `<path d="M30 85 Q50 95 70 85 L70 92 Q50 102 30 92 Z" fill="${CLASSES[o.cls].hex}" stroke="${INK}" stroke-width="2.5"/><circle cx="50" cy="96" r="3.6" fill="#e2a524" stroke="${INK}" stroke-width="1.8"/>`;
  return s + `</svg>`;
}

function foeSVG(type) {
  const open = `<svg class="portrait" viewBox="0 0 100 100" aria-hidden="true"><g stroke="${INK}" stroke-width="3" stroke-linejoin="round" stroke-linecap="round">`;
  const close = '</g></svg>';
  if (type === 'rotte' || type === 'kloakk') {
    const c = type === 'kloakk' ? '#6a625a' : '#a39d96', inner = '#e9a2a8';
    let s = open + `<circle cx="27" cy="32" r="13" fill="${c}"/><circle cx="27" cy="32" r="7" fill="${inner}" stroke="none"/><circle cx="73" cy="32" r="13" fill="${c}"/><circle cx="73" cy="32" r="7" fill="${inner}" stroke="none"/>` +
      `<path d="M24 50 Q26 30 50 30 Q74 30 76 50 Q72 70 50 90 Q28 70 24 50 Z" fill="${c}"/>` +
      `<circle cx="40" cy="50" r="3.8" fill="#d23a2e"/><circle cx="60" cy="50" r="3.8" fill="#d23a2e"/><circle cx="50" cy="86" r="4.2" fill="#e78a95"/>` +
      `<path d="M43 72 L21 67 M43 76 L23 81 M57 72 L79 67 M57 76 L77 81" stroke-width="1.5" fill="none"/>`;
    if (type === 'kloakk') s += `<path d="M33 39 L47 57" stroke="#efe0c8" stroke-width="2.5"/><path d="M36 44 l5 -2 M39 49 l5 -2" stroke="#efe0c8" stroke-width="1.6"/><path d="M62 62 q2 8 0 12 q-2 -4 0 -12" fill="#8bc34a" stroke-width="1.5"/>`;
    return s + close;
  }
  if (type === 'maake') {
    return open + `<path d="M22 54 Q22 26 50 24 Q78 26 78 54 Q78 76 50 78 Q22 76 22 54 Z" fill="#f6f5ef"/>` +
      `<path d="M30 37 L46 44 M70 37 L54 44" stroke-width="3.5"/>` +
      `<circle cx="40" cy="49" r="4.2" fill="#f1d34a"/><circle cx="40" cy="49" r="1.8" fill="${INK}" stroke="none"/><circle cx="60" cy="49" r="4.2" fill="#f1d34a"/><circle cx="60" cy="49" r="1.8" fill="${INK}" stroke="none"/>` +
      `<path d="M37 58 L50 93 L63 58 Q50 54 37 58 Z" fill="#f2c12e"/><circle cx="52" cy="79" r="3" fill="#d2342b" stroke="none"/>` + close;
  }
  const c = type === 'konge' ? '#e08a3a' : type === 'hvese' ? '#3b3533' : '#8d8478';
  const eyeC = type === 'hvese' ? '#7fd14b' : '#d6e04a';
  let s = open + `<path d="M24 46 L24 12 L46 30 Z" fill="${c}"/><path d="M76 46 L76 12 L54 30 Z" fill="${c}"/>` +
    `<path d="M28 37 L28 22 L38 30 Z" fill="#e7a3a0" stroke="none"/><path d="M72 37 L72 22 L62 30 Z" fill="#e7a3a0" stroke="none"/>` +
    `<ellipse cx="50" cy="56" rx="30" ry="26" fill="${c}"/>`;
  if (type === 'katt') s += `<path d="M42 33 l2 8 M50 31 v9 M58 33 l-2 8" fill="none" stroke-width="2.5"/>`;
  if (type !== 'katt') s += `<path d="M29 43 L44 48 M71 43 L56 48" fill="none"/>`;
  s += `<ellipse cx="38" cy="54" rx="6.5" ry="5" fill="${eyeC}"/><ellipse cx="38" cy="54" rx="1.4" ry="4.2" fill="${INK}" stroke="none"/>` +
    `<ellipse cx="62" cy="54" rx="6.5" ry="5" fill="${eyeC}"/><ellipse cx="62" cy="54" rx="1.4" ry="4.2" fill="${INK}" stroke="none"/>` +
    `<path d="M46 63 L54 63 L50 68 Z" fill="#e78a95" stroke-width="2"/>`;
  s += type === 'hvese'
    ? `<path d="M40 71 Q50 85 60 71 Z" fill="#7a2230" stroke-width="2.4"/><path d="M43 72 l2 5 l2 -4.5 M53 72.5 l2 4.5 l2 -5" fill="#fff" stroke-width="1.4"/>`
    : `<path d="M50 68 v3 q-4 4 -8 1 M50 71 q4 4 8 1" fill="none" stroke-width="2.4"/>`;
  s += `<path d="M35 67 L15 63 M35 71 L17 75 M65 67 L85 63 M65 71 L83 75" fill="none" stroke-width="1.5"/>`;
  if (type === 'konge') s += `<path d="M30 31 L27 7 L40 20 L50 3 L60 20 L73 7 L70 31 Z" fill="#e2a524"/><circle cx="50" cy="21" r="3.2" fill="#c3362b" stroke-width="1.5"/>`;
  return s + close;
}
