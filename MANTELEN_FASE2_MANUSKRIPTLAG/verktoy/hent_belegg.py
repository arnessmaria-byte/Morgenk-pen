#!/usr/bin/env python3
"""Trinn 0, steg 1: lager beleggfilene i kilder/belegg/ fra nedlastede kildedatasett.

Kjoeres der raadataene ligger (se kilder/belegg/proveniens.json for URL, revisjon og SHA-256).
Skriptet er dokumentasjon av hvordan beleggene ble hentet. Bygg og validering trenger bare
beleggfilene, ikke raadataene.  Bruk: hent_belegg.py <raadata-mappe> <prosjektmappe>
"""
import sys, os, re, json, glob, csv, hashlib, time, html, urllib.request, urllib.parse
import xml.etree.ElementTree as ET
SRC, PROJ = sys.argv[1], sys.argv[2]
OUT = os.path.join(PROJ, 'kilder', 'belegg'); os.makedirs(OUT, exist_ok=True)
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
def dump(name, obj):
    with open(os.path.join(OUT, name), 'w', encoding='utf-8', newline='\n') as f:
        json.dump(obj, f, ensure_ascii=False, indent=1); f.write('\n')
def gitrev(repo):
    return os.popen(f'git -C "{SRC}/git/{repo}" rev-parse HEAD 2>/dev/null').read().strip()
prov = []

# ---------- INTF: Liste og transkripsjoner ----------
T = '{http://www.tei-c.org/ns/1.0}'
def flat(el, hand):
    out = []
    def walk(e):
        tag = e.tag.replace(T, '')
        if tag == 'app':
            rd = e.findall(T + 'rdg'); ch = None
            for r in rd:
                if r.get('hand') == hand: ch = r
            if ch is None:
                for r in rd:
                    if r.get('type') == 'orig': ch = r
            if ch is not None:
                if ch.text: out.append(ch.text)
                for c in ch: walk(c)
            if e.tail: out.append(e.tail)
            return
        if tag in ('note', 'fw', 'pc'):
            if e.tail: out.append(e.tail)
            return
        if tag in ('lb', 'cb', 'pb'):
            if e.get('break') != 'no': out.append(' ')
            if e.tail: out.append(e.tail)
            return
        if tag == 'gap':
            out.append('[…]')
            if e.tail: out.append(e.tail)
            return
        pre = post = ''
        if tag == 'supplied': pre, post = '[', ']'
        if tag == 'unclear': pre, post = '(', ')'
        if tag == 'abbr' and e.get('type') == 'nomSac': pre = '‾'
        out.append(pre)
        if e.text: out.append(e.text)
        for c in e: walk(c)
        out.append(post)
        if tag == 'w': out.append(' ')
        if e.tail: out.append(e.tail)
    walk(el)
    return re.sub(r'\s+', ' ', ''.join(out)).strip()
def sig(docid):
    d = int(docid)
    if d < 20000: return 'P%d' % (d - 10000)
    if d < 30000: return '%02d' % (d - 20000) if d - 20000 < 10 else '0%d' % (d - 20000)
    return str(d - 30000)
log = {(l['kind'], l['docID'], l.get('ref')): l for l in json.load(open(f'{SRC}/ntvmr/fetchlog.json'))}
liste = {}
for f in glob.glob(f'{SRC}/ntvmr/liste/*.json'):
    docid = int(os.path.basename(f)[:-5])
    m = json.load(open(f))['data']['manuscripts'].get('manuscript')
    if not m: continue
    si = m.get('shelfInstances', {}).get('shelfInstance'); si = si if isinstance(si, list) else ([si] if si else [])
    l = log[('liste', docid, None)]
    liste[sig(docid)] = {'docID': docid, 'primaryName': str(m.get('primaryName')), 'orig': str(m.get('orig')),
        'origEarly': m.get('origEarly'), 'origLate': m.get('origLate'), 'lang': m.get('lang'),
        'shelfInstances': [{'institution': s['institution'].get('name'), 'place': s['institution'].get('place'),
                            'country': s['institution'].get('country'), 'shelfNumber': s.get('shelfNumber'),
                            'contentOverview': s.get('contentOverview')} for s in si],
        'url': l['url'], 'rawSha256': sha(f)}
# sideindeks (folio) for dokumenter med transkripsjon, og for 025/046 (lakunekontroll)
os.makedirs(f'{SRC}/ntvmr/page', exist_ok=True)
def pages(docid):
    p = f'{SRC}/ntvmr/page/{docid}.json'
    url = 'https://ntvmr.uni-muenster.de/community/vmr/api/metadata/liste/search/?' + urllib.parse.urlencode({'docID': docid, 'detail': 'page', 'format': 'json'})
    if not (os.path.exists(p) and os.path.getsize(p) > 0):
        req = urllib.request.Request(url, headers={'User-Agent': 'research-client/1.0'})
        open(p, 'wb').write(urllib.request.urlopen(req, timeout=120).read()); time.sleep(0.4)
    m = json.load(open(p))['data']['manuscripts'].get('manuscript') or {}
    pg = (m.get('pages') or {}).get('page') or []
    return (pg if isinstance(pg, list) else [pg]), url, sha(p)
trans = []
for f in sorted(glob.glob(f'{SRC}/ntvmr/tei/*.xml')):
    docid, ref = os.path.basename(f)[:-4].split('_', 1); docid = int(docid)
    root = ET.parse(f).getroot()
    lic = ''.join(root.find('.//' + T + 'availability').itertext()) if root.find('.//' + T + 'availability') is not None else ''
    abs_ = list(root.iter(T + 'ab'))
    l = log[('tei', docid, ref)]
    rec = {'siglum': sig(docid), 'docID': docid, 'ref': ref, 'transcribed': bool(abs_), 'url': l['url'], 'rawSha256': sha(f),
           'license': 'CC BY 4.0 (INTF)' if 'creativecommons.org/licenses/by/4.0' in lic else None, 'segments': []}
    pid = None
    for ab in abs_:
        hands = sorted({r.get('hand') for r in ab.iter(T + 'rdg') if r.get('hand')})
        hs = ['firsthand'] + [h for h in hands if h != 'firsthand']
        rec['segments'].append({'n': ab.get('n'), 'part': ab.get('part'), 'hands': {h: flat(ab, h) for h in hs}})
        m = re.search(r'\.P(\d+)\.', ab.get('{http://www.w3.org/XML/1998/namespace}id') or '')
        if m and pid is None: pid = int(m.group(1))
    rec['pageID'] = pid
    trans.append(rec)
need = sorted({r['docID'] for r in trans if r['transcribed']} | {20025, 20046, 20004})
pindex = {}
for d in need:
    try:
        pg, url, h = pages(d)
    except Exception as e:
        continue
    pindex[d] = {str(p.get('pageID')): {'folio': p.get('folio'), 'indexContent': p.get('indexContent')} for p in pg}
    pindex[d]['_meta'] = {'url': url, 'rawSha256': h}
for r in trans:
    pi = pindex.get(r['docID'], {})
    r['folio'] = (pi.get(str(r['pageID'])) or {}).get('folio') if r['pageID'] else None
def last_page(docid, book):
    pi = pindex.get(docid, {}); pgs = [(int(k), v) for k, v in pi.items() if k != '_meta' and v.get('indexContent') and book in v['indexContent']]
    pgs.sort(); return ({'pageID': pgs[-1][0], **pgs[-1][1]} if pgs else None)
lacuna = {'025@Rev.22.19': {'siglum': '025', 'docID': 20025, 'ref': 'Rev.22.19', 'lastIndexedPageOfBook': last_page(20025, 'Rev'),
          'conclusion': 'Siste indekserte side med Åpenbaringen slutter før Åp 22,19; stedet er ikke bevart i håndskriftet.',
          **pindex.get(20025, {}).get('_meta', {})},
          '046@Rev.22.19': {'siglum': '046', 'docID': 20046, 'ref': 'Rev.22.19', 'lastIndexedPageOfBook': last_page(20046, 'Rev'), **pindex.get(20046, {}).get('_meta', {})},
          '04@Rev.22.19': {'siglum': '04', 'docID': 20004, 'ref': 'Rev.22.19', 'lastIndexedPageOfBook': last_page(20004, 'Rev'), **pindex.get(20004, {}).get('_meta', {})}}
dump('intf-liste.json', {'source': 'INTF, Kurzgefasste Liste, via NTVMR API (metadata/liste/search, detail=shelfInstance)',
     'retrieved': '2026-11-25', 'note': 'Faktaopplysninger fra registeret med henvisning. Selve registeret er ikke kopiert.', 'records': liste})
dump('intf-transkripsjoner.json', {'source': 'INTF/NTVMR API (transcript/get, format=teiraw), publiserte transkripsjoner',
     'license': 'Creative Commons Attribution 4.0 (oppgitt i TEI-hodet til hver transkripsjon)', 'retrieved': '2026-11-25',
     'conventions': 'Parentes = usikre bokstaver, hakeparentes = rekonstruert tekst, ‾ = nomen sacrum, […] = lakune. Tom tekst i et transkribert verselement = verset står ikke i håndskriftets tekst.',
     'records': trans, 'lacunaChecks': lacuna})
prov.append({'id': 'INTF-NTVMR', 'what': 'Liste-poster (%d) og verstranskripsjoner (%d)' % (len(liste), len(trans)),
             'url': 'https://ntvmr.uni-muenster.de/community/vmr/api/', 'retrieved': '2026-11-25', 'sha256': 'per post (rawSha256)'})

# ---------- ETCBC/dss ----------
dss = json.load(open(f'{SRC}/../dss_words.json')) if os.path.exists(f'{SRC}/../dss_words.json') else []
grp = {}
for w in dss: grp.setdefault((w['ref'], w['scroll']), []).append(w)
drec = []
for (ref, sc), ws in grp.items():
    locs = sorted({(str(w['fragment']), str(w['line'])) for w in ws}, key=lambda x: (x[0], int(x[1]) if x[1].isdigit() else 0))
    drec.append({'ref': ref, 'scroll': sc, 'fragmentOrColumn': locs[0][0], 'lines': [l for _, l in locs],
                 'text': ' '.join(w['word'] for w in ws), 'words': [w['word'] for w in ws]})
tfdir = f'{SRC}/git/dss/tf/1.9'
dump('etcbc-dss-utdrag.json', {'source': 'ETCBC/dss (Text-Fabric), Martin Abeggs transkripsjoner av rullene', 'version': 'tf/1.9',
     'commit': gitrev('dss'), 'license': 'CC BY-NC 4.0', 'fileSha256': {f: sha(f'{tfdir}/{f}') for f in ('glyph.tf', 'scroll.tf', 'verse.tf', 'rec.tf', 'unc.tf', 'oslots.tf')},
     'conventions': 'Hakeparentes = rekonstruert, ? = usikker bokstav, ׳ skiller suffiks, ε = utfylt/tom plass i transkripsjonen.',
     'useNote': 'Utdrag for forskningskontroll av fem vers. Ikke for innfelling i kommersielt produkt uten avtale (NC).', 'records': drec})
prov.append({'id': 'ETCBC-DSS', 'url': 'https://github.com/ETCBC/dss', 'revision': gitrev('dss'), 'retrieved': '2026-11-25', 'sha256': {'tf/1.9/glyph.tf': sha(f'{tfdir}/glyph.tf')}})

# ---------- Leon Levy ----------
ll = {}
for f in glob.glob(f'{SRC}/llevy/*.html'):
    s = open(f, encoding='utf-8', errors='replace').read(); q = os.path.basename(f)[:-5]
    def fld(k):
        m = re.search(r'"%s":\s*("([^"\\]|\\.)*"|\[[^\]]*\])' % k, s)
        return json.loads(m.group(1)) if m else None
    if fld('manuscript_id') is None: continue
    ll[q] = {'manuscript_id': fld('manuscript_id'), 'name': fld('name'), 'short_name': fld('short_name'), 'site': fld('site'), 'material': fld('material'),
             'script_type': fld('script_type'), 'period': fld('period'), 'official_publications': fld('official_publications'),
             'url': f'https://www.deadseascrolls.org.il/explore-the-archive/manuscript/{q}-1', 'rawSha256': sha(f)}
dump('leon-levy-utdrag.json', {'source': 'Leon Levy Dead Sea Scrolls Digital Library (Israel Antiquities Authority), manuskriptsider', 'retrieved': '2026-11-25',
     'note': 'Katalogopplysninger med henvisning og lenke. Bilder er ikke lagret.', 'records': ll})
prov.append({'id': 'LEON-LEVY', 'url': 'https://www.deadseascrolls.org.il/', 'retrieved': '2026-11-25', 'sha256': 'per side (rawSha256)'})

# ---------- Swete (digital) ----------
def swete(fn, c, v):
    return ' '.join(l.split(' ', 1)[1].strip() for l in open(f'{SRC}/git/lxx-swete/data/{fn}', encoding='utf-8') if re.match(r'\d+\.%d\.%d ' % (c, v), l))
sw = {'Isa 53:11': swete('48.Isaias.txt', 53, 11), 'Deut 32:8': swete('05.Deuteronomium.txt', 32, 8), 'Deut 32:43': swete('05.Deuteronomium.txt', 32, 43),
      'Ps 21:17': swete('27.Psalmi.txt', 21, 17), 'Ps 144:13': swete('27.Psalmi.txt', 144, 13), 'Ps 144:14 (trykt 13a + 14)': swete('27.Psalmi.txt', 144, 14),
      'Odae 2:43': swete('28.Odae.txt', 2, 43)}
dump('swete-utdrag.json', {'source': 'H. B. Swete, The Old Testament in Greek (digital tekst: nathans/lxx-swete, avledet av First1KGreek)', 'commit': gitrev('lxx-swete'),
     'license': 'CC BY-SA 4.0 (digital tekst); trykt utgave er fri', 'fileSha256': {f: sha(f'{SRC}/git/lxx-swete/data/{f}') for f in ('48.Isaias.txt', '05.Deuteronomium.txt', '27.Psalmi.txt', '28.Odae.txt')},
     'qualityWarning': 'Den digitale teksten er OCR-avledet. 5 Mos 32:43 har tydelige tap (linjeslutt mangler). Lesninger fra dette verset er ikke bekreftet før de er lest mot trykt utgave.',
     'records': sw})
prov.append({'id': 'SWETE-DIGITAL', 'url': 'https://github.com/nathans/lxx-swete', 'revision': gitrev('lxx-swete'), 'retrieved': '2026-11-25'})

# ---------- NT-utgaver ----------
def rp(book, c, v, kind):
    for r in csv.reader(open(f'{SRC}/git/byzantine-majority-text/csv-unicode/ccat/{kind}/{book}.csv', encoding='utf-8')):
        if len(r) >= 3 and r[0] == str(c) and r[1] == str(v): return r[2]
    return None
def tisch(book, c, v):
    return ' '.join(l.split(' ')[4] for l in open(f'{SRC}/git/tischendorf-data/word-per-line/2.8/Unicode/{book}.txt', encoding='utf-8') if l.split(' ')[1].startswith(f'{c}:{v}.'))
def tagnt(fn, ref):
    out = []
    for ln in open(f'{SRC}/step/{fn}', encoding='utf-8-sig'):
        if ln.startswith(ref + '#'):
            p = ln.rstrip('\n').split('\t')
            out.append({'id': p[0], 'greek': p[1].split(' (')[0], 'editions': p[5], 'meaningVariants': p[6].strip(), 'spellingVariants': p[7].strip()})
    return out
V = [('Mark 1,1', 'MAR', 'MR', 'TAGNT_Mat-Jhn.txt', 'Mrk.1.1', 1, 1), ('Joh 1,18', 'JOH', 'JOH', 'TAGNT_Mat-Jhn.txt', 'Jhn.1.18', 1, 18),
     ('Apg 8,37', 'ACT', 'AC', 'TAGNT_Act-Rev.txt', 'Act.8.37', 8, 37), ('1 Tim 3,16', '1TI', '1TI', 'TAGNT_Act-Rev.txt', '1Ti.3.16', 3, 16),
     ('Åp 22,19', 'REV', 'RE', 'TAGNT_Act-Rev.txt', 'Rev.22.19', 22, 19)]
ed = {}
for name, rb, tb, tf_, tref, c, v in V:
    ed[name] = {'RP2018': rp(rb, c, v, 'no-variants'), 'RP2018_variantnoter': rp(rb, c, v, 'with-variants'), 'TISCH8': tisch(tb, c, v), 'TAGNT': tagnt(tf_, tref)}
dump('nt-utgaver-utdrag.json', {'sources': {
      'RP2018': {'name': 'Robinson–Pierpont, bysantinsk tekstform (byztxt/byzantine-majority-text, csv-unicode/ccat)', 'commit': gitrev('byzantine-majority-text'), 'license': 'Public domain (LICENSE i repoet)'},
      'TISCH8': {'name': 'Tischendorf, Editio octava (morphgnt/tischendorf-data, word-per-line 2.8)', 'commit': gitrev('tischendorf-data'), 'license': 'Public domain (README i datasettet)'},
      'TAGNT': {'name': 'STEPBible TAGNT, utgavefelt per ord (NA28, NA27, Tyn=THGNT, SBL, WH, Treg, TR, Byz)', 'revision': 'efe428a0047bf7b9c3ce2624f60c252c6e435945', 'license': 'CC BY 4.0 (Tyndale House, STEPBible)',
                'fileSha256': {f: sha(f'{SRC}/step/{f}') for f in ('TAGNT_Mat-Jhn.txt', 'TAGNT_Act-Rev.txt')}}},
     'note': 'Tom RP2018/TISCH8-verdi betyr at verset ikke står i utgavens tekst. RP2018_variantnoter gjengir utgivernes egne merknader om NA-tekstens lesning.',
     'records': ed})
prov += [{'id': 'RP2018', 'url': 'https://github.com/byztxt/byzantine-majority-text', 'revision': gitrev('byzantine-majority-text'), 'retrieved': '2026-11-25'},
         {'id': 'TISCH8', 'url': 'https://github.com/morphgnt/tischendorf-data', 'revision': gitrev('tischendorf-data'), 'retrieved': '2026-11-25'},
         {'id': 'TAGNT', 'url': 'https://github.com/STEPBible/STEPBible-Data', 'revision': 'efe428a0047bf7b9c3ce2624f60c252c6e435945', 'retrieved': '2026-11-25',
          'sha256': {f: sha(f'{SRC}/step/{f}') for f in ('TAGNT_Mat-Jhn.txt', 'TAGNT_Act-Rev.txt')}}]

# ---------- MAM (via Sefaria) og Vulgata Clementina ----------
mam = {}
for f in glob.glob(f'{SRC}/sefaria/*.json'):
    d = json.load(open(f))
    for v in d.get('versions', []):
        t = v.get('text'); t = t if isinstance(t, str) else ' '.join(t)
        mam[os.path.basename(f)[:-5]] = {'text': re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', t))).strip(), 'versionTitle': v.get('versionTitle'),
                                         'license': v.get('license'), 'versionSource': v.get('versionSource'), 'rawSha256': sha(f)}
dump('mam-utdrag.json', {'source': 'Miqra according to the Masorah (MAM), hentet via Sefaria API v3', 'retrieved': '2026-11-25', 'records': mam})
prov.append({'id': 'MAM-SEFARIA', 'url': 'https://www.sefaria.org/api/v3/texts/', 'retrieved': '2026-11-25', 'sha256': 'per vers (rawSha256)'})
vg = json.load(open(f'{SRC}/vulg/VulgClementine.json')); vrec = {}
for b in vg['books']:
    for c in b['chapters']:
        for v in c['verses']:
            k = (b['name'], c['chapter'], v['verse'])
            if k in (('Mark', 1, 1), ('John', 1, 18), ('Acts', 8, 37), ('I Timothy', 3, 16), ('Revelation of John', 22, 19)):
                vrec['%s %d:%d' % k] = v['text']
dump('vulgata-clementina-utdrag.json', {'source': 'Vulgata Clementina (digital tekst: scrollmapper/bible_databases, formats/json/VulgClementine.json)', 'retrieved': '2026-11-25',
     'license': 'Teksten er fri (1592-tradisjonen); repoet er MIT-lisensiert', 'fileSha256': sha(f'{SRC}/vulg/VulgClementine.json'), 'records': vrec})
prov.append({'id': 'VG-CLEM', 'url': 'https://github.com/scrollmapper/bible_databases', 'retrieved': '2026-11-25', 'sha256': sha(f'{SRC}/vulg/VulgClementine.json')})

# ---------- Clavis og fedre i oversettelse ----------
cl = {}
for f in glob.glob(f'{SRC}/clavis/*.txt'):
    series, num = os.path.basename(f)[:-4].split('-')
    t = re.sub(r'\s+', ' ', open(f, encoding='utf-8').read())
    m = re.search(r'Full parent tree\(s\)\s*(.*?)\s*%s-%s' % (series, num), t)
    head = m.group(1) if m else ''
    parts = [p.strip() for p in head.split(' > ')]
    cl[f'{series} {num}'] = {'series': series, 'number': num, 'treeAndTitle': head, 'title': parts[-1] if parts else None,
                             'anteNicene': 'Antenicaeni' in head, 'url': f'https://clavis.brepols.net/clacla/OA/Link.aspx?clavis={series}&number={num}', 'rawSha256': sha(f)}
dump('clavis-utdrag.json', {'source': 'Clavis Clavium (Brepols, åpen tilgang): Clavis Patrum Graecorum / Latinorum', 'retrieved': '2026-11-25',
     'note': 'Nummer, plassering og tittel slik basen oppgir dem. Tittelfeltet er siste ledd i basens plassering og kan inneholde krysshenvisning.', 'records': cl})
prov.append({'id': 'CLAVIS', 'url': 'https://clavis.brepols.net/clacla/OA/', 'retrieved': '2026-11-25', 'sha256': 'per post (rawSha256)'})
FIND = [('Iren-AH@III.12.8', 'anf01', r'I believe Jesus Christ to be the Son of God'),
        ('Cypr-Quir@III.43', 'anf05', r'what is there which hinders me from being baptized\? Then said Philip, If thou believest with all thine heart, thou mayest'),
        ('Iren-AH@III.10.5', 'anf01', r'does thus commence his Gospel narrative: "The beginning of the Gospel of Jesus Christ, the Son of God'),
        ('Iren-AH@III.16.3', 'anf01', r'Wherefore Mark also says: "The beginning of the Gospel of Jesus Christ, the Son of God'),
        ('Iren-AH@III.11.8', 'anf01', r'"The beginning of the Gospel of Jesus Christ, as it is written in Esaias the prophet,"'),
        ('Orig-Cels@II.4', 'anf04', r'Mark--says: "The beginning of the Gospel of Jesus Christ, as it is written in the prophet Isaiah'),
        ('Orig-CommJo@I.14(ANF)', 'anf09', r'as Mark says, \[\d+\] "The beginning of the Gospel of Jesus Christ\."'),
        ('Iren-AH@III.11.6', 'anf01', r'"the only-begotten Son of God, which is in the bosom of the Father'),
        ('Iren-AH@IV.20.6', 'anf01', r'except the only-begotten Son, who is in the bosom of the Father'),
        ('Iren-AH@IV.20.11', 'anf01', r'"The only-begotten God, \[\d+\] which is in the bosom of the Father'),
        ('Clem-Strom@V.12', 'anf02', r'The only-begotten God, who is in the bosom of the Father, He hath declared Him'),
        ('Tert-Prax@15', 'anf03', r'the only begotten Son, who is in the bosom of the Father, and has Himself declared Him'),
        ('Hipp-Noet@5', 'anf05', r'the only-begotten Son, which is in the bosom of the Father'),
        ('Orig-Cels@II.71', 'anf04', r'the only-begotten Son, who is in the bosom of the Father, He hath declared Him'),
        ('Orig-CommJo@II.29(ANF)', 'anf09', r'the only-begotten God, who is in the bosom of the Father, He hath declared Him'),
        ('Chrys-Hom1Tim@XI', 'npnf113', r'"God was manifest in the flesh\." The Creator was seen incarnate'),
        ('GregNyss-Eun@XI(NPNF)', 'npnf205', r'to Timothy, proclaims in plain terms, "God was manifest in the flesh, justified in the spirit')]
fa = {}; vols = {}
for key, vol, pat in FIND:
    if vol not in vols: vols[vol] = re.sub(r'\s+', ' ', open(f'{SRC}/ccel/{vol}.txt', encoding='utf-8', errors='replace').read())
    m = re.search(pat, vols[vol])
    fa[key] = {'volume': vol, 'found': bool(m), 'excerpt': vols[vol][max(0, m.start() - 60):m.end() + 60] if m else None}
dump('fedre-oversettelse-utdrag.json', {'source': 'Ante-Nicene Fathers / Nicene and Post-Nicene Fathers (engelsk oversettelse, fri), tekstfiler fra CCEL', 'retrieved': '2026-11-25',
     'note': 'Bekrefter at stedet finnes og hvilken ordlyd oversettelsen har. Dette er ikke kritisk utgave: ordlyden på gresk eller latin må leses i utgaven som registeret viser til.',
     'volumeSha256': {v: sha(f'{SRC}/ccel/{v}.txt') for v in sorted(vols)}, 'records': fa})
prov.append({'id': 'ANF-NPNF', 'url': 'https://ccel.org/ccel/s/schaff/', 'retrieved': '2026-11-25', 'sha256': {v: sha(f'{SRC}/ccel/{v}.txt') for v in sorted(vols)}})
dump('proveniens.json', {'generated': '2026-11-25', 'datasets': prov})
print('belegg skrevet:', sorted(os.listdir(OUT)))
print('fedre uten treff:', [k for k, v in fa.items() if not v['found']])
print('lakune 025:', json.dumps(lacuna['025@Rev.22.19']['lastIndexedPageOfBook'], ensure_ascii=False), '| 046:', json.dumps(lacuna['046@Rev.22.19']['lastIndexedPageOfBook'], ensure_ascii=False), '| 04:', json.dumps(lacuna['04@Rev.22.19']['lastIndexedPageOfBook'], ensure_ascii=False))
