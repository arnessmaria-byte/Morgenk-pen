// ---------- Tilfeldighet (seedet, så tester kan gjentas) ----------
let rngState = 1;
function seed(n) { rngState = (n >>> 0) || 1; }
function rnd() {
  rngState = (rngState + 0x6D2B79F5) >>> 0;
  let t = rngState;
  t = Math.imul(t ^ (t >>> 15), t | 1);
  t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
  return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
}
const ri = (a, b) => a + Math.floor(rnd() * (b - a + 1));
const pick = arr => arr[Math.floor(rnd() * arr.length)];
const chance = p => rnd() < p;
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
function shuffle(arr) {
  for (let i = arr.length - 1; i > 0; i--) { const j = Math.floor(rnd() * (i + 1)); [arr[i], arr[j]] = [arr[j], arr[i]]; }
  return arr;
}
const $ = s => document.querySelector(s);
const esc = s => String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const pct = p => Math.round(p * 100) + ' %';
const man = (ax, ay, bx, by) => Math.abs(ax - bx) + Math.abs(ay - by);

// ---------- Regler og data ----------
const CAP = 12;          // plasser i kennelen
const STEPS = 6;         // 5 steg + Kattekongen
const ADOPT_COST = 12;
const KURS_COST = 8;
const GIVE_BONES = 3;

const STATS = ['sty', 'smi', 'uth', 'int', 'hur', 'fla'];
const STAT_NAME = { sty: 'Styrke', smi: 'Smidighet', uth: 'Utholdenhet', int: 'Intelligens', hur: 'Hurtighet', fla: 'Flaks' };
const STAT_ABBR = { sty: 'STY', smi: 'SMI', uth: 'UTH', int: 'INT', hur: 'HUR', fla: 'FLA' };
const STAT_HELP = {
  sty: 'Skade med bitt', smi: 'Unnvikelse og kast', uth: 'Helse', int: 'Magi og helbredelse',
  hur: 'Hvor langt hunden går', fla: 'Kritiske treff og å overleve fall',
};

const NAMES_M = ['Bamse', 'Rufus', 'Tassen', 'Pølse', 'Kuling', 'Snurre', 'Pjokk', 'Fido', 'Brutus', 'Laban', 'Trofast', 'Kasper', 'Tuppen', 'Gubben', 'Bjeffe', 'Odin', 'Rambo', 'Knøttet', 'Sjefen', 'Pluto', 'Krølle', 'Grim', 'Bølle', 'Doffen', 'Fant', 'Smulen', 'Klumpen', 'Tjukken', 'Vaffel', 'Ruskus'];
const NAMES_F = ['Molly', 'Luna', 'Tiril', 'Bella', 'Frøya', 'Trine', 'Saga', 'Nala', 'Mira', 'Ronja', 'Dott', 'Lady', 'Tøffa', 'Snuppa', 'Bikkja', 'Perle', 'Lykke', 'Gullet', 'Mynta', 'Kanel', 'Vimsa', 'Fia', 'Tulla', 'Hera', 'Rosa', 'Sussi', 'Bitte', 'Snella', 'Polly', 'Lefse'];

const FURS = [
  { name: 'Gylden', c: '#d9a441' }, { name: 'Sjokolade', c: '#6e4225' }, { name: 'Svart', c: '#342c27' },
  { name: 'Hvit', c: '#f4efe6' }, { name: 'Grå', c: '#9b958c' }, { name: 'Rødbrun', c: '#a8532c' },
  { name: 'Krem', c: '#ead1a2' }, { name: 'Blåmerle', c: '#7e8ca3' },
];
const PATTERNS = ['ingen', 'flekker', 'maske', 'lapp', 'blis'];
const EARS = ['heng', 'spiss', 'rund', 'lange'];
const SNOUTS = ['kort', 'lang'];
const EYES = ['#5a3415', '#3b6fb5', '#c98a1b'];

const MUTS = {
  treoye: { name: 'Tredje øye', desc: '+2 Intelligens', mods: { int: 2 } },
  horn: { name: 'Horn', desc: '+2 Styrke, -1 Smidighet', mods: { sty: 2, smi: -1 } },
  kjempetunge: { name: 'Kjempetunge', desc: 'Bitt rekker 2 ruter', mods: {} },
  hjertenese: { name: 'Hjertenese', desc: '+2 Flaks', mods: { fla: 2 } },
  pigg: { name: 'Pigghår', desc: 'Den som biter hunden, tar 1 skade', mods: {} },
  kjempehode: { name: 'Kjempehode', desc: '+3 Intelligens, -2 Hurtighet', mods: { int: 3, hur: -2 } },
  glod: { name: 'Glødeøyne', desc: '+2 Smidighet', mods: { smi: 2 } },
  tenner: { name: 'Sabeltenner', desc: '+1 skade med bitt', mods: {} },
  flaksorer: { name: 'Flaksører', desc: 'Ører som vinger. +2 Hurtighet', mods: { hur: 2 } },
  kyklop: { name: 'Kyklop', desc: '+1 Styrke, -2 Smidighet', mods: { sty: 1, smi: -2 }, bad: true },
  skjeloyd: { name: 'Skjeløyd', desc: '-2 Smidighet', mods: { smi: -2 }, bad: true },
  harlos: { name: 'Hårløs', desc: '-2 Utholdenhet', mods: { uth: -2 }, bad: true },
  ettore: { name: 'Ett øre', desc: '-1 Flaks, -1 Hurtighet', mods: { fla: -1, hur: -1 }, bad: true },
  lopper: { name: 'Lopper', desc: '-1 Utholdenhet, -1 Flaks', mods: { uth: -1, fla: -1 }, bad: true },
  skjevkjeve: { name: 'Skjev kjeve', desc: '-2 Styrke', mods: { sty: -2 }, bad: true },
};
const GOOD_MUTS = Object.keys(MUTS).filter(k => !MUTS[k].bad);
const BAD_MUTS = Object.keys(MUTS).filter(k => MUTS[k].bad);

const CLASSES = {
  slass: { name: 'Slåsshund', hex: '#c3362b', hp: 2, attack: 'bitt', skill: 'storm', desc: 'Biter hardt. Stormløp: løper i rett linje og biter for ekstra skade.' },
  vokt: { name: 'Vokter', hex: '#2a52be', hp: 6, attack: 'bitt', skill: 'vakt', desc: 'Tåler mye. Vaktbjeff: 4 skjold, og fiender i nærheten går etter vokteren.' },
  jakt: { name: 'Jakthund', hex: '#2e8745', hp: 0, attack: 'pinne', skill: 'apport', desc: 'Kaster pinner på avstand. Apport!: treffer og dytter fienden bakover.' },
  myst: { name: 'Mystiker', hex: '#7b3fb0', hp: 0, attack: 'gnist', skill: 'maane', desc: 'Magi som ikke kan unnvikes. Månehyl treffer et helt område, også egne.' },
  pleie: { name: 'Pleier', hex: '#e2a524', hp: 2, attack: 'nafs', skill: 'slikk', desc: 'Slikk sår: helbreder og vekker hunder som ligger nede.' },
};
const CLS_ORDER = ['slass', 'vokt', 'jakt', 'myst', 'pleie'];

const PASSIVES = {
  klor: { name: 'Skarpe klør', desc: 'Passiv: +1 skade med bitt.' },
  tykkpels: { name: 'Tykk pels', desc: 'Passiv: +4 maks helse.' },
  snute: { name: 'Supersnute', desc: 'Passiv: +10 % sjanse for kritisk treff.' },
  poter: { name: 'Lette poter', desc: 'Passiv: går 1 rute lenger.' },
  seig: { name: 'Seigpining', desc: 'Passiv: +25 % sjanse for å overleve når den faller.' },
};
const LEARNED = ['halespinn', 'grav', 'baesj', 'rull', 'skremme', 'loppe', 'glefs', 'klor', 'tykkpels', 'snute', 'poter', 'seig'];

const ENEMIES = {
  rotte: { name: 'Rotte', hp: 5, dmg: 2, move: 3, range: [1, 1], dodge: 0.10, cost: 2 },
  maake: { name: 'Måke', hp: 4, dmg: 2, move: 4, range: [1, 1], dodge: 0.20, cost: 2, fly: true },
  katt: { name: 'Gatekatt', hp: 9, dmg: 3, move: 3, range: [1, 1], dodge: 0.15, cost: 4 },
  hvese: { name: 'Hvesekatt', hp: 6, dmg: 2, move: 2, range: [2, 3], dodge: 0.10, cost: 3 },
  kloakk: { name: 'Kloakkrotta', hp: 18, dmg: 3, move: 3, range: [1, 1], dodge: 0.05, cost: 8, poison: true },
  konge: { name: 'Kattekongen', hp: 40, dmg: 4, move: 2, range: [1, 1], dodge: 0.05, boss: true },
};
const ENEMY_INFO = {
  rotte: 'Rask og svak.', maake: 'Flyr over hindringer.', katt: 'Tøff nærkjemper.',
  hvese: 'Hveser på avstand 2-3.', kloakk: 'Bittet gir lopper: 1 skade per runde.',
  konge: 'Tilkaller katter hver tredje runde. Kan ikke dyttes.',
};

const PLACES = {
  kamp: ['Bakgården', 'Parkeringsplassen', 'Lekeplassen', 'Skolegården', 'Havna', 'Søppelfyllinga', 'Kolonihagen'],
  elite: ['Kloakken'],
  boss: ['Kattekongens loft'],
  hvil: ['under et epletre', 'i en varm garasje', 'på en solrik trapp', 'bak bensinstasjonen'],
  hendelse: ['Et sted langs veien'],
};
const NODE_INFO = {
  kamp: { name: 'Kamp', desc: 'Rotter, måker og katter.' },
  elite: { name: 'Elitekamp', desc: 'Kloakkrotta. Dobbel erfaring og flere bein.' },
  hendelse: { name: 'Hendelse', desc: 'Noe rart skjer. Dere velger hva dere gjør.' },
  hvil: { name: 'Hvil', desc: 'Alle får tilbake 60 % helse.' },
  boss: { name: 'Kattekongen', desc: 'Sjefen selv. Han tilkaller hjelp hver tredje runde.' },
};
