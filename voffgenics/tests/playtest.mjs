// Selvverifikasjon for Voffgenics. Kjør: node voffgenics/build.mjs && node voffgenics/tests/playtest.mjs
// Krever Playwright (globalt installert: NODE_PATH=$(npm root -g)).
import { createServer } from 'node:http';
import { readFileSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const { chromium } = require('playwright');
const here = dirname(fileURLToPath(import.meta.url));
const root = join(here, '..');
const shots = process.env.SHOTS || join(root, 'tests', 'shots');
mkdirSync(shots, { recursive: true });

const html = readFileSync(join(root, 'index.html'));
const server = createServer((req, res) => { res.writeHead(200, { 'content-type': 'text/html; charset=utf-8' }); res.end(html); });
await new Promise(r => server.listen(0, r));
const url = `http://127.0.0.1:${server.address().port}/`;

let failed = 0;
const results = [];
function check(name, ok, detail = '') {
  results.push(`${ok ? 'OK  ' : 'FEIL'} ${name}${detail ? ' :: ' + detail : ''}`);
  if (!ok) failed++;
  console.log(results.at(-1));
}

const browser = await chromium.launch();
async function openPage(viewport) {
  const ctx = await browser.newContext({ viewport });
  const page = await ctx.newPage();
  const errors = [];
  page.on('pageerror', e => errors.push('pageerror: ' + e.message));
  page.on('console', m => { if (m.type() === 'error') errors.push('console: ' + m.text()); });
  // Fonter hentes ikke i testmiljøet; svar tomt så de ikke gir støy.
  await page.route(/fonts\.(googleapis|gstatic)\.com/, r => r.fulfill({ status: 200, contentType: 'text/css', body: '' }));
  await page.goto(url);
  await page.waitForSelector('.dog');
  return { ctx, page, errors };
}
const noOverflow = page => page.evaluate(() => document.scrollingElement.scrollWidth <= window.innerWidth + 1);

// 1. Lasting, desktop og mobil
for (const [label, vp] of [['desktop', { width: 1280, height: 860 }], ['mobil', { width: 390, height: 844 }]]) {
  const { ctx, page, errors } = await openPage(vp);
  check(`${label}: laster uten feil`, errors.length === 0, errors.join(' | '));
  check(`${label}: seks hunder i kennelen`, (await page.locator('.dog').count()) === 6);
  check(`${label}: ingen horisontal rulling`, await noOverflow(page));
  await page.screenshot({ path: join(shots, `1-kennel-${label}.png`), fullPage: label === 'desktop' });
  await ctx.close();
}

const { ctx, page, errors } = await openPage({ width: 1280, height: 860 });

// 2 og 3. Genetikk og innavl
const gen = await page.evaluate(() => {
  const V = window.VOFF; V.headless(true); V.newGame(42);
  const S = V.S; const errs = []; let n = 0;
  const strays = S.dogs;
  for (let i = 0; i < 2000; i++) {
    const mom = strays.filter(d => d.sex === 'F')[i % 3], dad = strays.filter(d => d.sex === 'M')[(i * 7) % 3];
    mom.learned = ['klor', 'grav'].slice(0, i % 3); dad.learned = ['rull', 'snute'].slice(0, (i + 1) % 3);
    const p = V.makePuppy(mom, dad); n++;
    for (const k of V.STATS) {
      const v = p.stats[k];
      if (v < 1 || v > 10) errs.push(`stat ${k}=${v}`);
      if (Math.abs(v - mom.stats[k]) > 1 && Math.abs(v - dad.stats[k]) > 1) errs.push(`stat ${k}=${v} vs ${mom.stats[k]}/${dad.stats[k]}`);
    }
    if (p.learned.length > 2) errs.push('for mange evner');
    for (const a of p.learned) if (!mom.learned.includes(a) && !dad.learned.includes(a)) errs.push('evne ikke fra foreldre: ' + a);
    if (p.muts.length > 3) errs.push('for mange mutasjoner');
    if (new Set(p.muts).size !== p.muts.length) errs.push('dobbel mutasjon');
  }
  // Innavl: søsken mot ubeslektede
  V.newGame(7); const s2 = V.S;
  const F = s2.dogs.find(d => d.sex === 'F'), M = s2.dogs.find(d => d.sex === 'M');
  F.muts = []; M.muts = [];
  const sis = V.makePuppy(F, M); sis.sex = 'F'; sis.muts = []; V.addDog(sis);
  const bro = V.makePuppy(F, M); bro.sex = 'M'; bro.muts = []; V.addDog(bro);
  const strangerF = V.addDog(V.makeStray('F')); strangerF.muts = [];
  const strangerM = V.addDog(V.makeStray('M')); strangerM.muts = [];
  const bad = (a, b) => { let c = 0; for (let i = 0; i < 1500; i++) if (V.makePuppy(a, b).muts.some(m => V.MUTS[m].bad)) c++; return c / 1500; };
  return { n, errs: errs.slice(0, 5), errCount: errs.length, rel: V.relation(sis.id, bro.id), relStr: V.relation(strangerF.id, strangerM.id), inbred: bad(sis, bro), outbred: bad(strangerF, strangerM) };
});
check('genetikk: 2000 valper innenfor reglene', gen.errCount === 0, gen.errs.join('; '));
check('slekt: søsken er nær slekt, fremmede ikke', gen.rel === 'naer' && gen.relStr === 'ingen', `${gen.rel}/${gen.relStr}`);
check('innavl gir flere defekter', gen.inbred > gen.outbred + 0.25, `søsken ${(gen.inbred * 100).toFixed(0)} % mot ubeslektet ${(gen.outbred * 100).toFixed(0)} %`);

// 4. 300 autospilte kamper
const fights = await page.evaluate(async () => {
  const V = window.VOFF; V.headless(true);
  const problems = []; let maxRound = 0, wins = 0, total = 0;
  for (let i = 0; i < 300; i++) {
    V.newGame(1000 + i);
    const team = V.S.dogs.slice(0, 4).map((d, j) => ({ dogId: d.id, cls: ['slass', 'vokt', 'jakt', 'myst', 'pleie'][(i + j) % 5] }));
    V.startRun(team);
    const step = i % 6;
    V.S.run.step = step;
    const node = step === 5 ? { t: 'boss', place: 'Test' } : { t: i % 4 === 0 && step >= 2 ? 'elite' : 'kamp', place: 'Test' };
    V.S.run.current = node;
    const B = V.makeBattle(node, step);
    const origRound = B.round;
    let guard = 0;
    while (!B.over && B.round <= 60 && guard++ < 200) {
      await V.simBattle(Object.assign(B, {})); // simBattle stopper ved slutt eller runde 60
      const p = V.battleProblems(B); if (p.length) { problems.push(`kamp ${i}: ${p.join(', ')}`); break; }
    }
    const p = V.battleProblems(B); if (p.length) problems.push(`kamp ${i} slutt: ${p.join(', ')}`);
    maxRound = Math.max(maxRound, B.round); total++; if (B.over === 'win') wins++;
    if (!B.over) problems.push(`kamp ${i} ble ikke ferdig (runde ${B.round})`);
  }
  return { problems: problems.slice(0, 5), count: problems.length, maxRound, wins, total };
});
check('300 kamper: alle ferdige, ingen ulovlige tilstander', fights.count === 0, fights.problems.join(' | '));
check('300 kamper: ferdige innen 60 runder', fights.maxRound <= 60, `lengste: ${fights.maxRound} runder`);
console.log(`     (autospilleren vant ${fights.wins} av ${fights.total} enkeltkamper)`);

// 5 og 6. 100 hele turer + balanse
const runs = await page.evaluate(async () => {
  const V = window.VOFF; V.headless(true);
  const tally = { seier: 0, tap: 0, hjem: 0, stuck: 0 }, problems = [];
  let steps = 0;
  for (let i = 0; i < 100; i++) {
    V.newGame(5000 + i);
    const before = V.S.day, ids = V.S.dogs.slice(0, 4).map(d => d.id);
    const res = await V.autoRun(ids.map(id => ({ dogId: id, cls: null })));
    if (!res) { problems.push(`tur ${i}: startet ikke`); continue; }
    tally[res.kind] = (tally[res.kind] || 0) + 1;
    const S = V.S;
    if (S.run) problems.push(`tur ${i}: run ikke lukket`);
    if (S.day !== before + 1) problems.push(`tur ${i}: dagen gikk ikke fram`);
    for (const id of ids) {
      const d = V.dogById(id);
      if (d && d.status !== 'veteran') problems.push(`tur ${i}: ${d.name} ble ikke veteran`);
      if (!d && !S.grave.length) problems.push(`tur ${i}: hund forsvant uten grav`);
    }
    if (S.dogs.some(d => !Number.isFinite(d.stats.sty))) problems.push(`tur ${i}: ødelagte egenskaper`);
    steps += S.grave.length;
  }
  return { tally, problems: problems.slice(0, 6), count: problems.length, deaths: steps };
});
check('100 turer: alle avsluttes riktig', runs.count === 0 && !runs.tally.stuck, runs.problems.join(' | ') + ` ${JSON.stringify(runs.tally)}`);
const winRate = runs.tally.seier / 100;
check('balanse: autospilleren vinner 15-85 % av turene', winRate >= 0.15 && winRate <= 0.85, `seier ${runs.tally.seier}, tap ${runs.tally.tap}, døde hunder totalt ${runs.deaths}`);

// 7. Ekte klikk: parring, tur, kamp
await page.evaluate(() => { const V = window.VOFF; V.headless(false); V.newGame(99); V.S.intro = false; V.render(); });
await page.locator('.dog').first().waitFor();
const firstMale = page.locator('.dog', { has: page.locator('.sex', { hasText: '♂' }) }).first();
await firstMale.locator('[data-act="pair"]').click();
await page.locator('[data-act="pair-with"]').first().click();
check('klikk: parring registrert', (await page.evaluate(() => window.VOFF.S.pairs.length)) === 1);
await page.screenshot({ path: join(shots, '2-paret.png') });
await page.locator('[data-act="sleep"]').click();
const pups = await page.evaluate(() => window.VOFF.S.dogs.filter(d => d.status === 'valp').length);
check('klikk: natten gir valper', pups >= 1, `${pups} valper`);
await page.screenshot({ path: join(shots, '3-valper.png'), fullPage: true });

await page.locator('[data-act="setup"]').click();
const picks = page.locator('[data-act="toggle-dog"]');
for (let i = 0; i < 4; i++) await picks.nth(i).click();
await page.screenshot({ path: join(shots, '4-oppsett.png'), fullPage: true });
await page.locator('[data-act="start-run"]').click();
await page.screenshot({ path: join(shots, '5-turloype.png'), fullPage: true });
await page.locator('[data-act="choose-node"]').first().click();
await page.waitForSelector('#board .unit');
await page.evaluate(() => window.VOFF.speed(0.25));
await page.screenshot({ path: join(shots, '6-kamp-start.png') });

// Spill kampen med klikk: for hver hund, gå mot nærmeste fiende og angrip om mulig.
let clicks = 0, moved = false, attacked = false;
for (let round = 0; round < 40; round++) {
  const state = await page.evaluate(() => { const B = window.VOFF.S.run && window.VOFF.S.run.battle; return B ? { over: B.over, phase: B.phase } : { over: 'gone' }; });
  if (state.over) break;
  for (let dogTurn = 0; dogTurn < 5; dogTurn++) {
    const plan = await page.evaluate(() => {
      const V = window.VOFF, B = V.S.run.battle;
      if (B.over || B.phase !== 'player') return null;
      const u = B.units.find(o => o.id === V.UI.sel && !o.acted && !o.down);
      if (!u) return null;
      const foes = B.units.filter(o => o.side === 'enemy' && !o.dead);
      const tgt = foes.find(f => Math.abs(f.x - u.x) + Math.abs(f.y - u.y) <= (u.cls === 'jakt' ? 4 : u.cls === 'myst' ? 3 : u.reach));
      if (tgt) return { kind: 'attack', x: tgt.x, y: tgt.y };
      if (u.moved) return { kind: 'wait' };
      const tiles = [...document.querySelectorAll('#board .tile.hl-move')].map(t => ({ x: +t.dataset.x, y: +t.dataset.y }));
      if (!tiles.length) return { kind: 'wait' };
      const near = (t) => Math.min(...foes.map(f => Math.abs(f.x - t.x) + Math.abs(f.y - t.y)));
      tiles.sort((a, b) => near(a) - near(b));
      return { kind: 'move', x: tiles[0].x, y: tiles[0].y };
    });
    if (!plan) break;
    if (plan.kind === 'wait') await page.locator('[data-act="wait"]').click();
    else {
      await page.locator(`#board .tile[data-x="${plan.x}"][data-y="${plan.y}"]`).click();
      if (plan.kind === 'move') moved = true; else attacked = true;
    }
    clicks++;
    await page.evaluate(() => window.VOFF.idle());
    if (clicks === 3) await page.screenshot({ path: join(shots, '7-kamp-midt.png') });
  }
  const st = await page.evaluate(() => { const B = window.VOFF.S.run.battle; return B ? { over: B.over, phase: B.phase } : { over: 'gone' }; });
  if (st.over) break;
  if (st.phase === 'player') { await page.locator('[data-act="end-turn"]').click(); }
  await page.waitForFunction(() => { const B = window.VOFF.S.run.battle; return !B || B.over || (B.phase === 'player' && !window.VOFF.UI.busy); }, null, { timeout: 30000 });
}
check('klikk: hunder flyttet og angrep', moved && attacked, `${clicks} klikk`);
const over = await page.evaluate(() => { const r = window.VOFF.S.run; return r && r.battleResult ? (r.battleResult.win ? 'win' : 'loss') : null; });
check('klikk: kampen fikk et resultat', !!over, String(over));
await page.screenshot({ path: join(shots, '8-kamp-slutt.png') });
if (over) await page.locator('[data-act="battle-continue"]').click();
const after = await page.evaluate(() => window.VOFF.S.run ? window.VOFF.S.run.screen : window.VOFF.S.screen);
check('klikk: videre etter kamp', ['map', 'levelup', 'end'].includes(after), after);
await page.screenshot({ path: join(shots, '9-etter-kamp.png'), fullPage: true });

// 8. Lagring overlever omlasting
const dayBefore = await page.evaluate(() => JSON.stringify([window.VOFF.S.day, window.VOFF.S.dogs.length, window.VOFF.S.run && window.VOFF.S.run.screen]));
await page.reload(); await page.waitForSelector('#app > *');
const dayAfter = await page.evaluate(() => JSON.stringify([window.VOFF.S.day, window.VOFF.S.dogs.length, window.VOFF.S.run && window.VOFF.S.run.screen]));
check('lagring: samme tilstand etter omlasting', dayBefore === dayAfter, `${dayBefore} -> ${dayAfter}`);

// 9. Hendelse, nivåøkning og sluttskjerm tegnes og virker med klikk
await page.evaluate(() => {
  const V = window.VOFF; V.newGame(11); V.S.intro = false;
  V.startRun(V.S.dogs.slice(0, 4).map(d => ({ dogId: d.id, cls: null })));
  V.S.run.step = 1; V.S.run.screen = 'event'; V.S.run.event = { id: 'kjottbein', result: null }; V.render();
});
await page.locator('[data-act="event-opt"]').first().click();
check('klikk: hendelse gir et utfall', !!(await page.evaluate(() => window.VOFF.S.run.event.result)));
await page.screenshot({ path: join(shots, '11-hendelse.png'), fullPage: true });
await page.locator('[data-act="event-next"]').click();
check('klikk: videre etter hendelse', (await page.evaluate(() => [window.VOFF.S.run.screen, window.VOFF.S.run.step].join()) ) === 'map,2');
await page.evaluate(() => {
  const V = window.VOFF, d = V.S.dogs[0];
  V.S.run.levelQueue.push({ dogId: d.id, level: 2, offers: [{ kind: 'learn', id: 'halespinn' }, { kind: 'learn', id: 'tykkpels' }, { kind: 'stat', k: 'sty' }] });
  V.S.run.screen = 'levelup'; V.render();
});
await page.screenshot({ path: join(shots, '12-niva.png'), fullPage: true });
await page.locator('[data-act="offer"]').first().click();
check('klikk: ny evne lært', await page.evaluate(() => window.VOFF.S.dogs[0].learned.includes('halespinn') && window.VOFF.S.run.screen === 'map'));
await page.locator('[data-act="go-home"]').click();
await page.locator('[data-act="confirm-yes"]').click();
check('klikk: gå hjem gir sluttskjerm', (await page.evaluate(() => window.VOFF.S.run.screen)) === 'end');
await page.screenshot({ path: join(shots, '13-slutt.png'), fullPage: true });
await page.locator('[data-act="close-run"]').click();
const vets = await page.evaluate(() => window.VOFF.S.dogs.filter(d => d.status === 'veteran').length);
check('klikk: laget er veteraner i kennelen', vets === 4, `${vets} veteraner`);
await page.screenshot({ path: join(shots, '14-kennel-veteraner.png'), fullPage: true });

check('ingen konsollfeil under hele testen', errors.length === 0, errors.slice(0, 3).join(' | '));

// Mobil kamp-skjermbilde
const mob = await openPage({ width: 390, height: 844 });
await mob.page.evaluate(() => { const V = window.VOFF; V.newGame(3); V.S.intro = false; V.startRun(V.S.dogs.slice(0, 4).map(d => ({ dogId: d.id, cls: null }))); V.chooseNode(0); V.render(); });
await mob.page.waitForSelector('#board .unit');
check('mobil: kamp uten horisontal rulling', await noOverflow(mob.page));
await mob.page.screenshot({ path: join(shots, '10-kamp-mobil.png'), fullPage: true });
check('mobil: ingen feil', mob.errors.length === 0, mob.errors.join(' | '));
await mob.ctx.close();

await ctx.close();
await browser.close();
server.close();
console.log(`\n${results.length - failed}/${results.length} sjekker bestått.`);
process.exit(failed ? 1 : 0);
