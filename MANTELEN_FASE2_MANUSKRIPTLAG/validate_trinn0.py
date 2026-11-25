#!/usr/bin/env python3
"""Validator for Trinn 0 i MANTELEN fase 2 (manuskriptlaget).

Bruk:
  python validate_trinn0.py --r10-dir <mappe med låst R10>      (leser assets/data/gt/books og assets/data/bibelen)
  python validate_trinn0.py --fetch                              (henter de ni bokfilene fra www.mantelen.no, bare lesing)

Avslutter med 0 bare når alle kontrollene består:
  1. Hvert pilotsted består JSON Schema-valideringen.
  2. Hvert ordanker treffer riktig ord og riktig SHA-256 i de låste R10/R11.1-filene.
  3. Hvert siglum og hver patristisk referanse finnes i vitneregisteret, og hver utgave i kilderegisteret.
  4. Ingen datering er skrevet inn for hånd.
  5. Hvert belegg som en bekreftelse viser til, finnes og har riktig SHA-256.
  6. Vitnemønsteret (akse 1) kan regnes ut på nytt og er likt det som er lagret.
Krever Python 3.9+ og pakken jsonschema. Validatoren skriver ingenting i R10.
"""
import argparse, hashlib, json, os, re, sys, tempfile, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'verktoy'))
try:
    import jsonschema
except ImportError:
    print('FEIL: pakken jsonschema mangler (pip install jsonschema).'); sys.exit(2)
from monster import pattern, computed_kind

J = lambda *p: json.load(open(os.path.join(HERE, *p), encoding='utf-8'))
ok_all = True
lines = []


def say(s=''):
    lines.append(s); print(s)


def result(name, good, total, detail=None):
    global ok_all
    passed = good == total
    ok_all = ok_all and passed
    say('%s  %s: %d / %d' % ('BESTÅTT' if passed else 'FEIL   ', name, good, total))
    for d in (detail or [])[:20]:
        say('         - ' + d)
    return passed


def fetch_r10(books):
    tmp = tempfile.mkdtemp(prefix='r10-les-')
    page = urllib.request.urlopen(urllib.request.Request('https://www.mantelen.no/bibelen/', headers={'User-Agent': 'validate-trinn0'}), timeout=60).read().decode('utf-8')
    nt = re.search(r'data-bibel-index="([^"]+)"', page).group(1); gt = re.search(r'data-gt-index="([^"]+)"', page).group(1)
    for b, meta in books.items():
        base = gt if b.startswith('gt-') else nt
        url = base.replace('index.json', ('books/%s.json' if b.startswith('gt-') else '%s.json') % b)
        dst = os.path.join(tmp, meta['publishedPath']); os.makedirs(os.path.dirname(dst), exist_ok=True)
        open(dst, 'wb').write(urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'validate-trinn0'}), timeout=180).read())
        if meta.get('r11LayerPath'):
            u2 = base.replace('bibelen/index.json', 'r11-nt/%s.json' % b).split('?')[0] + '?v=' + meta['r11LayerSha256']
            d2 = os.path.join(tmp, meta['r11LayerPath']); os.makedirs(os.path.dirname(d2), exist_ok=True)
            open(d2, 'wb').write(urllib.request.urlopen(urllib.request.Request(u2, headers={'User-Agent': 'validate-trinn0'}), timeout=180).read())
    return tmp


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--r10-dir', default=os.environ.get('MANTELEN_R10_DIR'))
    ap.add_argument('--fetch', action='store_true')
    ap.add_argument('--report', help='skriv utskriften til denne filen')
    a = ap.parse_args()
    pil, reg, src, lock, schema = J('piloter', 'trinn0-10-piloter.json'), J('registre', 'vitneregister.json'), J('registre', 'kildelisenser.json'), J('registre', 'r10-laas.json'), J('registre', 'schema-manuscript-layer.json')
    units = pil['units']
    r10 = fetch_r10(lock['books']) if a.fetch else a.r10_dir
    if not r10:
        print('FEIL: oppgi --r10-dir eller --fetch.'); sys.exit(2)
    say('MANTELEN fase 2, Trinn 0: validering av %d pilotsteder' % len(units))
    say('R10-kilde: %s' % ('www.mantelen.no (hentet nå)' if a.fetch else r10)); say()

    # 1. skjema
    jsonschema.Draft202012Validator.check_schema(schema)
    uv = jsonschema.Draft202012Validator({'$schema': schema['$schema'], '$ref': '#/$defs/unit', '$defs': schema['$defs']})
    bad = []
    for u in units:
        errs = sorted(uv.iter_errors(u), key=lambda e: list(e.path))
        if errs: bad.append('%s: %s (%s)' % (u['variantId'], errs[0].message[:140], '/'.join(map(str, errs[0].path))))
    whole = list(jsonschema.Draft202012Validator(schema).iter_errors(pil))
    result('1. JSON Schema, pilotsteder', len(units) - len(bad), len(units), bad)
    result('   JSON Schema, hele filen', 0 if whole else 1, 1, [e.message[:140] for e in whole])

    # 2. ankre
    cache = {}

    def book(bid):
        if bid not in cache:
            p = os.path.join(r10, lock['books'][bid]['publishedPath'])
            raw = open(p, 'rb').read()
            cache[bid] = (json.loads(raw.decode('utf-8')), hashlib.sha256(raw).hexdigest())
        return cache[bid]

    def check_anchor(an, vid):
        errs = []
        d, h = book(an['bookId'])
        if h != an['bookSha256']: errs.append('%s: SHA-256 for %s stemmer ikke med ankeret' % (vid, an['bookId']))
        if h != lock['books'][an['bookId']]['sha256']: errs.append('%s: SHA-256 for %s stemmer ikke med R10-låsen' % (vid, an['bookId']))
        if an['testament'] == 'GT':
            vs = [v for c in d['chapters'] for v in c['v'] if v.get('mtRef') == an['mtRef']]
            if len(vs) != 1: return errs + ['%s: mtRef %s gir %d vers' % (vid, an['mtRef'], len(vs))]
            v = vs[0]; byid = {w['id']: w for w in v['w']}
            for w in an['words']:
                r = byid.get(w['id'])
                if not r or r['g'] != w['g'] or r['position'] != w['position']: errs.append('%s: ord %s treffer ikke' % (vid, w['id']))
            ids = [w['id'] for w in v['w']]
            if an['firstWordId'] not in ids or an['lastWordId'] not in ids or [w['id'] for w in an['words']] != ids[ids.index(an['firstWordId']):ids.index(an['lastWordId']) + 1]:
                errs.append('%s: ordspennet er ikke sammenhengende i R10' % vid)
            if v.get('stepPublicationRef') != an.get('stepPublicationRef'): errs.append('%s: stepPublicationRef avviker' % vid)
            back = [x['mtRef'] for c in d['chapters'] for x in c['v'] if x.get('stepPublicationRef') == an.get('stepPublicationRef')]
            if back != [an['mtRef']]: errs.append('%s: adressekoblingen stepPublicationRef → mtRef er ikke entydig (%s)' % (vid, back))
        else:
            v = [x for c in d['chapters'] if c['n'] == an['chapter'] for x in c['v'] if x['n'] == an['verse']]
            if len(v) != 1: return errs + ['%s: fant ikke verset' % vid]
            ws = v[0]['w']
            for w in an['words']:
                if w['wordIndex'] > len(ws) or ws[w['wordIndex'] - 1]['g'] != w['g']: errs.append('%s: ord %d treffer ikke (%s)' % (vid, w['wordIndex'], w['g']))
            if [w['wordIndex'] for w in an['words']] != list(range(an['firstWordIndex'], an['lastWordIndex'] + 1)): errs.append('%s: ordindeksene er ikke sammenhengende' % vid)
            meta = lock['books'][an['bookId']]
            if an.get('r11LayerSha256') != meta.get('r11LayerSha256'): errs.append('%s: SHA-256 for R11-ordlaget avviker fra låsen' % vid)
            lp = os.path.join(r10, meta.get('r11LayerPath', '-'))
            if os.path.exists(lp):
                raw = open(lp, 'rb').read(); side = json.loads(raw.decode('utf-8'))
                if hashlib.sha256(raw).hexdigest() != meta['r11LayerSha256'] or side.get('book_sha256') != h: errs.append('%s: R11-ordlaget er ikke bundet til bokfilen' % vid)
                row = side['verses'].get('%d:%d' % (an['chapter'], an['verse']))
                if not row or len(row) != len(ws): errs.append('%s: R11-ordlaget har ikke samme ordtall som verset' % vid)
        return errs

    bad = []; n_gt = n_nt = 0; twoway = 0
    for u in units:
        e = check_anchor(u['anchor'], u['variantId'])
        for x in u.get('crossReferences', []):
            if 'anchor' in x: e += check_anchor(x['anchor'], u['variantId'] + ' (kryssreferanse %s)' % x['ref'])
        if u['anchor']['testament'] == 'GT': n_gt += 1; twoway += 1
        else: n_nt += 1
        bad += e
    result('2. Ordankre mot låst R10/R11.1 (ord og SHA-256)', len(units) - len({b.split(':')[0] for b in bad}), len(units), bad)
    say('         GT: %d ankre med w[].id, toveis adresse mtRef ↔ stepPublicationRef prøvd for %d. NT: %d ankre med wordIndex + g + bookSha256.' % (n_gt, twoway, n_nt))
    t = [u for u in units if u['variantId'] == 'NT-1TI-003-016-01'][0]['anchor']
    w9 = [x for c in book('1ti')[0]['chapters'] if c['n'] == 3 for x in c['v'] if x['n'] == 16][0]['w'][8]
    result('   R11.1-ordet i 1 Tim 3,16 (ord 9, Θεὸς, G2316)', int(t['firstWordIndex'] == 9 and w9['g'] == 'Θεὸς' and w9['s'] == 2316), 1)

    # 3. sigla, patristiske referanser og utgaver
    W = reg['witnesses']; eds = {s['id'] for s in src['sources']} | {s['id'] for s in src['internalEditions']}
    sig_total = sig_ok = pat_total = pat_ok = ed_total = ed_ok = 0; miss = []
    for u in units:
        for r in u['readings']:
            for k in ('manuscriptWitnesses', 'versionWitnesses'):
                for w in r[k]:
                    sig_total += 1
                    if w['siglum'] in W: sig_ok += 1
                    else: miss.append('%s: siglum %s' % (u['variantId'], w['siglum']))
                    if w.get('readIn'):
                        ed_total += 1; ed_ok += w['readIn'] in eds
            for w in r['patristicWitnesses']:
                pat_total += 1
                e = W.get(w['siglum'])
                if e and e.get('type') == 'kirkefar_verk' and e.get('clavis', {}).get('number'): pat_ok += 1
                else: miss.append('%s: patristisk referanse %s' % (u['variantId'], w['siglum']))
            for e in r['editionSupport']:
                ed_total += 1
                if e['edition'] in eds: ed_ok += 1
                else: miss.append('%s: utgave %s' % (u['variantId'], e['edition']))
        for x in u.get('excludedWitnesses', []):
            sig_total += 1
            if x['siglum'] in W: sig_ok += 1
            else: miss.append('%s: utelukket vitne %s' % (u['variantId'], x['siglum']))
    result('3. Manuskriptsigla i vitneregister.json', sig_ok, sig_total, miss)
    result('   Patristiske referanser med Clavis-nummer i registeret', pat_ok, pat_total)
    result('   Utgaver i kildelisenser.json', ed_ok, ed_total)
    say('         Uregistrerte sigla: %d. Andel registrert: %.0f %%.' % (len(miss), 100.0 * (sig_ok + pat_ok) / max(1, sig_total + pat_total)))

    # 4. ingen datering for hånd
    dated = [k for k, v in W.items() if v.get('dateRange') or v.get('century')]
    hand = [k for k in dated if not (W[k].get('referenceSource', {}).get('sha256') and W[k]['referenceSource'].get('register'))]
    nodate = [k for k, v in W.items() if not v.get('dateRange') and not v.get('dateStatus')]
    in_units = len(re.findall(r'"(century|dateRange|date[A-Z]\w*|datering)"\s*:', json.dumps([{k: v for k, v in u.items() if k not in ('evaluation', 'provenance')} for u in units])))
    result('4. Dateringer hentet fra register med SHA-256 (av %d daterte oppslag)' % len(dated), len(dated) - len(hand), len(dated), hand)
    result('   Oppslag uten datering har merknad om hvor den skal hentes', len(W) - len(dated) - len(nodate), len(W) - len(dated), nodate)
    result('   Dateringsfelt i pilotenhetene (skal være 0)', 1 if in_units == 0 else 0, 1)

    # 5. belegg
    ev_cache = {}; ev_total = ev_ok = 0; evbad = []; status = {}
    for u in units:
        for r in u['readings']:
            for k in ('editionSupport', 'manuscriptWitnesses', 'versionWitnesses', 'patristicWitnesses'):
                for w in r[k]:
                    v = w['verification']; status[v['status']] = status.get(v['status'], 0) + 1
                    if 'evidence' not in v: continue
                    ev_total += 1
                    f, _, key = v['evidence'].partition('#')
                    try:
                        if f not in ev_cache: ev_cache[f] = json.load(open(os.path.join(HERE, f), encoding='utf-8'))
                        d = ev_cache[f]; good = True
                        if 'intf-transkripsjoner' in f:
                            s, ref = key.split('@'); rec = [x for x in d['records'] if x['siglum'] == s and x['ref'] == ref][0]
                            good = rec['rawSha256'] == v.get('sha256') and (w.get('reading') in [h for sg in rec['segments'] for h in sg['hands'].values()] or (w.get('reading') == '' and rec['transcribed']))
                        elif 'etcbc' in f:
                            sc, ref = key.split('@'); rec = [x for x in d['records'] if x['scroll'] == sc and x['ref'] == ref][0]
                            good = rec['text'] == w.get('reading')
                        elif 'fedre' in f:
                            good = d['records'][key]['found'] and d['volumeSha256'][d['records'][key]['volume']] == v.get('sha256')
                        elif 'nt-utgaver' in f:
                            vr, kk = key.split('/'); good = kk in d['records'][vr]
                        else:
                            good = key in d['records']
                        if good: ev_ok += 1
                        else: evbad.append('%s: belegg stemmer ikke: %s' % (u['variantId'], v['evidence']))
                    except Exception as ex:
                        evbad.append('%s: belegg mangler: %s (%s)' % (u['variantId'], v['evidence'], ex))
    result('5. Belegg bak bekreftede vitner og utgaver', ev_ok, ev_total, evbad)

    # 6. akse 1 og 2 kan regnes ut på nytt
    def recomputes(u):
        try:
            return pattern(u, reg) == u['witnessPattern'] and computed_kind(u) == u['variantKind']['computed']
        except KeyError:
            return False
    same = sum(1 for u in units if recomputes(u))
    result('6. Vitnemønster og mekanisk variantart regnet ut på nytt', same, len(units))
    ev = sum(1 for u in units if u['evaluation']['class'] == 'ikke vurdert')
    say(); say('Status for bekreftelsene (alle vitner og utgavefelt i de ti enhetene):')
    for k in sorted(status): say('  %-26s %3d' % (k, status[k]))
    open_ = status.get('IKKE_AVLEST', 0) + status.get('BEKREFTET_I_OVERSETTELSE', 0) + status.get('DELVIS_BEKREFTET', 0) + status.get('BEKREFTET_SEKUNDAERT', 0)
    say('Vurdering (akse 3): %d av %d enheter står som «ikke vurdert». Dobbel registrering: ikke kjørt.' % (ev, len(units)))
    say('Åpne punkter før låsing: %d opplysninger må leses i kilden av navngitt leser (ikke avlest, bare i oversettelse, delvis eller sekundært belagt).' % open_)
    say(); say('RESULTAT: ' + ('ALLE KONTROLLER BESTÅTT' if ok_all else 'FEIL FUNNET'))
    if a.report:
        open(a.report, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines) + '\n')
    sys.exit(0 if ok_all else 1)


if __name__ == '__main__':
    main()
