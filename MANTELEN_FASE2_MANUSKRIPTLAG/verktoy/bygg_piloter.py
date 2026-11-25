#!/usr/bin/env python3
"""Trinn 0, steg 3: bygger registre/vitneregister.json og piloter/trinn0-10-piloter.json.

Bruk: bygg_piloter.py <prosjektmappe> <R10-mappe>
R10-mappen er en skrivebeskyttet kopi av den låste utgaven (assets/data/gt/books/*.json og
assets/data/bibelen/*.json). Skriptet leser R10 og skriver bare i prosjektmappen.

Regel null (plan 7.1): ingen lesning, datering eller siglum i utdataene kommer fra en språkmodell.
Hver vitneopplysning prøves her mot et belegg i kilder/belegg/. Det som ikke kan prøves, får
status IKKE_AVLEST og en henvisning til hvor det skal leses.
"""
import json, os, re, sys, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from monster import attest, edge_certainty, gnorm, hnorm, pattern, computed_kind

PROJ, R10 = sys.argv[1], sys.argv[2]
B = lambda f: json.load(open(os.path.join(PROJ, 'kilder', 'belegg', f), encoding='utf-8'))
LISTE, TRANS, DSS, LL, SW, NTU, MAM, VG, CL, FA = (B('intf-liste.json'), B('intf-transkripsjoner.json'), B('etcbc-dss-utdrag.json'), B('leon-levy-utdrag.json'),
    B('swete-utdrag.json'), B('nt-utgaver-utdrag.json'), B('mam-utdrag.json'), B('vulgata-clementina-utdrag.json'), B('clavis-utdrag.json'), B('fedre-oversettelse-utdrag.json'))
LOCK = json.load(open(os.path.join(PROJ, 'registre', 'r10-laas.json'), encoding='utf-8'))
TR = {(r['siglum'], r['ref']): r for r in TRANS['records']}
HAND = {'firsthand': '*', 'corrector': 'C', 'corrector1': 'C1', 'corrector2': 'C2', 'corrector3': 'C3'}
used = set()


def book(book_id):
    sub = 'gt/books' if book_id.startswith('gt-') else 'bibelen'
    p = os.path.join(R10, 'assets', 'data', sub, book_id + '.json')
    raw = open(p, 'rb').read(); h = hashlib.sha256(raw).hexdigest()
    assert h == LOCK['books'][book_id]['sha256'], 'R10-filen %s stemmer ikke med låsen' % book_id
    return json.loads(raw.decode('utf-8')), h


def verse(d, ch, vn):
    return [v for v in [c for c in d['chapters'] if c['n'] == ch][0]['v'] if v['n'] == vn][0]


def gt_anchor(book_id, ch, vn, first, last, relation):
    d, h = book(book_id); v = verse(d, ch, vn)
    ids = [w['id'] for w in v['w']]; i, j = ids.index(first), ids.index(last)
    words = [{'id': w['id'], 'position': w['position'], 'g': w['g']} for w in v['w'][i:j + 1]]
    return ({'testament': 'GT', 'bookId': book_id, 'bookSha256': h, 'mtRef': v['mtRef'], 'stepPublicationRef': v['stepPublicationRef'],
             'firstWordId': first, 'lastWordId': last, 'relation': relation, 'words': words}, v)


def nt_anchor(book_id, ch, vn, i, j, relation, note=None):
    d, h = book(book_id); v = verse(d, ch, vn)
    a = {'testament': 'NT', 'bookId': book_id, 'bookSha256': h, 'r11LayerSha256': LOCK['books'][book_id]['r11LayerSha256'], 'chapter': ch, 'verse': vn,
         'firstWordIndex': i, 'lastWordIndex': j, 'relation': relation, 'words': [{'wordIndex': k, 'g': v['w'][k - 1]['g']} for k in range(i, j + 1)]}
    if note: a['r111Note'] = note
    return a, v


def loc(r):
    f = r.get('folio')
    if f in (None, ''): return None
    return ('fol. %s' % f) if re.search(r'[rv]$', str(f)) else ('INTF-side/blad %s' % f)


def ms(sig, ref, pat, hand='firsthand', note=None):
    """Gresk håndskrift, prøvd mot INTF-transkripsjonen."""
    r = TR[(sig, ref)]; seg = r['segments'][0]
    found, cert = attest(seg['hands'][hand], 'grc', pat)
    assert found, 'Lesningen ble ikke funnet: %s %s %s %r i %r' % (sig, ref, hand, pat, seg['hands'][hand])
    used.add(sig)
    w = {'siglum': sig, 'hand': HAND[hand] if (hand != 'firsthand' or len(seg['hands']) > 1) else None, 'locator': loc(r), 'reading': seg['hands'][hand],
         'attested': found, 'certainty': cert, 'verification': {'status': 'BEKREFTET_TRANSKRIPSJON', 'evidence': 'kilder/belegg/intf-transkripsjoner.json#%s@%s' % (sig, ref), 'sha256': r['rawSha256']}}
    if note: w['note'] = note
    return w


def ms_omit(sig, ref, before, after):
    """Verset står ikke i håndskriftets tekst. Prøves mot transkripsjonen av versene før og etter."""
    r = TR[(sig, ref)]
    assert r['transcribed'] and r['segments'] and all(not t for s in r['segments'] for t in s['hands'].values()), (sig, ref)
    b, a = TR[(sig, before)]['segments'][0]['hands']['firsthand'], TR[(sig, after)]['segments'][0]['hands']['firsthand']
    assert b and a, (sig, 'kontekst mangler')
    cb, ca = edge_certainty(b, 'grc', tail=True), edge_certainty(a, 'grc', tail=False)
    weak = [c for c in (cb, ca) if c != 'lest']
    used.add(sig)
    w = {'siglum': sig, 'hand': None, 'locator': loc(r), 'reading': '', 'certainty': 'utelatt' if not weak else ('rekonstruert' if 'rekonstruert' in weak else 'delvis rekonstruert'),
         'verification': {'status': 'BEKREFTET_TRANSKRIPSJON', 'evidence': 'kilder/belegg/intf-transkripsjoner.json#%s@%s' % (sig, ref), 'sha256': r['rawSha256']},
         'note': 'Versene før og etter følger rett på hverandre i transkripsjonen.' + (' Overgangen er delvis rekonstruert, så utelatelsen bygger på utgiverens linjeberegning.' if weak else '')}
    return w


def ms_unread(sig, hand, must, note):
    used.add(sig)
    return {'siglum': sig, 'hand': hand, 'locator': None, 'certainty': 'ikke avlest', 'note': note, 'verification': {'status': 'IKKE_AVLEST', 'mustReadIn': must}}


DREC = {(r['scroll'], r['ref']): r for r in DSS['records']}
SCROLL = {'1QIsaa': '1Qisaa', '1QIsab': '1Q8', '4QIsad': '4Q58', '4QDeutj': '4Q37', '4QDeutq': '4Q44', '5/6HevPs': '5/6hev1b', '4QPsf': '4Q88', '11QPsa': '11Q5'}


def dss(sig, ref, pat, note=None):
    r = DREC[(SCROLL[sig], ref)]
    found, cert = attest(r['text'], 'he', pat)
    assert found, (sig, ref, pat, r['text'])
    used.add(sig)
    w = {'siglum': sig, 'hand': None, 'locator': 'ETCBC-sted %s, linje %s' % (r['fragmentOrColumn'], '–'.join([r['lines'][0], r['lines'][-1]]) if len(r['lines']) > 1 else r['lines'][0]),
         'reading': r['text'], 'attested': found, 'certainty': cert,
         'verification': {'status': 'BEKREFTET_TRANSKRIPSJON', 'evidence': 'kilder/belegg/etcbc-dss-utdrag.json#%s@%s' % (SCROLL[sig], ref), 'sha256': DSS['fileSha256']['glyph.tf']}}
    if note: w['note'] = note
    return w


def b19a(text, note=None):
    used.add('B19A')
    w = {'siglum': 'B19A', 'hand': None, 'locator': None, 'reading': text, 'certainty': 'lest',
         'verification': {'status': 'BEKREFTET_TRANSKRIPSJON', 'basis': 'WLC/OSHB er en transkripsjon av dette håndskriftet. Lesningen er ordene i låst R10.'}}
    if note: w['note'] = note
    return w


def ed_r10():
    return {'edition': 'R10', 'verification': {'status': 'BEKREFTET_ANKER', 'basis': 'Lesningen er ankerordene i låst R10.'}}


def ed_text(eid, vref, key, pat=None, form=None):
    t = gnorm(NTU['records'][vref][key])
    assert (t == '') if pat is None else re.search(pat, t), (eid, vref, pat, t)
    e = {'edition': eid, 'verification': {'status': 'BEKREFTET_UTGAVETEKST', 'evidence': 'kilder/belegg/nt-utgaver-utdrag.json#%s/%s' % (vref, key),
                                          'basis': 'Utgavens digitale tekst.' if pat else 'Verset står ikke i utgavens digitale tekst.'}}
    if form: e['form'] = form
    return e


def tagnt_text(vref, tag):
    out = []
    for row in NTU['records'][vref]['TAGNT']:
        if tag in row['editions'].split('+'):
            out.append(row['greek'])
        else:
            for var in row['meaningVariants'].split(';'):
                m = re.match(r'\s*(\S+) \(.*? in: ([\w+]+)', var)
                if m and tag in m.group(2).split('+'): out.append(m.group(1))
    return gnorm(' '.join(out))


def ed_tagnt(eid, tag, vref, pat=None, form=None):
    t = tagnt_text(vref, tag)
    assert (t == '') if pat is None else re.search(pat, t), (eid, vref, pat, t)
    e = {'edition': eid, 'verification': {'status': 'BEKREFTET_SEKUNDAERT', 'evidence': 'kilder/belegg/nt-utgaver-utdrag.json#%s/TAGNT' % vref,
                                          'basis': 'STEPBible TAGNT, utgavefeltet «%s». Utgaven selv er ikke avlest.' % tag}}
    if form: e['form'] = form
    return e


def ed_na_rp(vref, needle, form=None):
    assert needle in NTU['records'][vref]['RP2018_variantnoter'], (vref, needle)
    e = {'edition': 'NA28', 'verification': {'status': 'BEKREFTET_SEKUNDAERT', 'evidence': 'kilder/belegg/nt-utgaver-utdrag.json#%s/RP2018_variantnoter' % vref,
                                             'basis': 'Robinson–Pierponts variantnote «%s». NA28 selv er ikke avlest.' % needle}}
    if form: e['form'] = form
    return e


def ed_mam(key, pat, basis='Utgavens tekst hentet via Sefaria.'):
    assert re.search(pat, hnorm(MAM['records'][key]['text'])), (key, pat, hnorm(MAM['records'][key]['text']))
    return {'edition': 'MAM', 'verification': {'status': 'BEKREFTET_UTGAVETEKST', 'evidence': 'kilder/belegg/mam-utdrag.json#' + key, 'sha256': MAM['records'][key]['rawSha256'], 'basis': basis}}


def lxx(key, pat, text, nor, vorlage, sig='LXX', limit=None, note=None, loc_=None):
    assert re.search(pat, gnorm(SW['records'][key])), (key, pat, gnorm(SW['records'][key]))
    used.add(sig)
    w = {'siglum': sig, 'text': text, 'lang': 'grc', 'norwegian': nor, 'readIn': 'SWETE', 'locator': loc_ or key, 'vorlage': vorlage,
         'verification': {'status': 'BEKREFTET_UTGAVETEKST', 'evidence': 'kilder/belegg/swete-utdrag.json#' + key, 'basis': 'Swetes tekst i digital form.'}}
    if limit: w['witnessLimit'] = limit
    if note: w['note'] = note
    return w


def vg(key, pat, text, nor, limit, compatible=None):
    assert re.search(pat, VG['records'][key].lower()), (key, pat)
    used.add('Vg-Clem')
    w = {'siglum': 'Vg-Clem', 'text': text, 'lang': 'la', 'norwegian': nor, 'readIn': 'VG-CLEM', 'locator': key, 'vorlage': 'kan ikke avgjøres', 'witnessLimit': limit,
         'verification': {'status': 'BEKREFTET_UTGAVETEKST', 'evidence': 'kilder/belegg/vulgata-clementina-utdrag.json#' + key, 'sha256': VG['fileSha256'], 'basis': 'Clementinas digitale tekst. Vulgata-håndskriftene er ikke avlest.'}}
    if compatible: w['compatibleWith'] = compatible
    return w


EDN = {'Iren-AH': 'Rousseau–Doutreleau, Sources Chrétiennes (bok III: SC 211; bok IV: SC 100)', 'Cypr-Quir': 'Weber, CCSL 3', 'Orig-Cels': 'Borret, Sources Chrétiennes 132 flg.; Koetschau, GCS',
       'Orig-CommJo': 'Blanc, Sources Chrétiennes 120 flg.; Preuschen, GCS', 'Clem-Strom': 'Stählin–Früchtel, GCS', 'Tert-Prax': 'Kroymann–Evans, CCSL 2',
       'Hipp-Noet': 'Butterworth (1977); Schwartz', 'Chrys-Hom1Tim': 'Field; Migne PG 62', 'GregNyss-Eun': 'Jaeger, GNO I–II'}


def father(sig, locator, key, lang, quote_type, wording, limit=None, compatible=None, note=None):
    f = FA['records'][key]; assert f['found'], key
    used.add(sig)
    w = {'siglum': sig, 'locator': locator, 'lang': lang, 'quoteType': quote_type, 'wording': wording,
         'verification': {'status': 'BEKREFTET_I_OVERSETTELSE', 'evidence': 'kilder/belegg/fedre-oversettelse-utdrag.json#' + key, 'sha256': FA['volumeSha256'][f['volume']],
                          'basis': 'Stedet og ordlyden er funnet i den engelske oversettelsen (%s). Grunnspråksteksten er ikke avlest.' % f['volume'].upper(), 'mustReadIn': EDN[sig]}}
    if limit: w['witnessLimit'] = limit
    if compatible: w['compatibleWith'] = compatible
    if note: w['note'] = note
    return w


def rd(rid, label, text, lang, morph, nor, eds=(), mss=(), vers=(), pats=(), **kw):
    d = {'readingId': rid, 'label': label, 'text': text, 'lang': lang, 'morphology': morph, 'norwegian': nor,
         'editionSupport': list(eds), 'manuscriptWitnesses': list(mss), 'versionWitnesses': list(vers), 'patristicWitnesses': list(pats)}
    d.update(kw)
    return d


N = lambda text, kind='ordrett', note=None: ({'text': text, 'kind': kind, 'note': note} if note else {'text': text, 'kind': kind})
NO_EVAL = {'class': 'ikke vurdert', 'by': None, 'date': None, 'arguments': [], 'literature': [], 'dissent': []}
LAT_ART = 'Latin har ingen artikkel og kan ikke skille mellom greske lesninger som bare avviker i artikkelen.'
units = []


def unit(vid, nr, ref, anchor_v, readings, assigned, signif, note, **kw):
    anchor, v = anchor_v
    u = {'variantId': vid, 'pilotNr': nr, 'status': 'UTKAST', 'ref': ref, 'anchor': anchor, 'r10Verse': v['t'], 'readings': readings,
         'witnessPattern': None, 'variantKind': {'computed': None, 'assigned': assigned, 'assignedBy': 'Fable (fagledelsen), utkast 2026-11-25'},
         'significance': signif, 'evaluation': dict(NO_EVAL), 'philologicalNote': note}
    u.update(kw)
    u['provenance'] = [{'built': '2026-11-25', 'builder': 'verktoy/bygg_piloter.py', 'enteredBy': 'Fable (fagledelsen), første registrering', 'secondReader': None}]
    u['checks'] = {'sigla': 'KJØRES AV validate_trinn0.py', 'anchor': 'KJØRES AV validate_trinn0.py', 'unicode': 'NFC ved bygg', 'doubleEntry': 'IKKE KJØRT'}
    units.append(u)


# ===================== 1. Jes 53,11 =====================
units_src = True
unit('GT-ISA-053-011-01', 1, {'r10': 'Jes 53,11', 'mtRef': 'Isa.53.11', 'stepPublicationRef': 'Isa.53.11', 'lxxRef': 'Isa 53:11'},
     gt_anchor('gt-isa', 53, 11, '23EFM', '23EFM', 'etter'),
     [rd('a', 'MT: uten objekt', 'יִרְאֶה', 'he', 'Verb, Qal, yiqtol, 3. person maskulinum entall. Verbet står uten objekt.', [N('skal han se', 'r10')],
         eds=[ed_r10(), ed_mam('Isaiah.53.11', r'יראה ישבע')], mss=[b19a('יראה ישבע')], isR10=True),
      rd('b', '«lys»', 'יראה אור', 'he', 'Samme verb med objektet אוֹר: substantiv, maskulinum entall, absolutt form.', [N('skal han se lys')],
         mss=[dss('1QIsaa', 'Is 53:11', r'יראהאור'), dss('1QIsab', 'Is 53:11', r'יראהאור'), dss('4QIsad', 'Is 53:11', r'יראהאור')],
         vers=[lxx('Isa 53:11', r'δειξαι αυτω φωσ', 'δεῖξαι αὐτῷ φῶς', [N('å vise ham lys')], 'sannsynlig',
                   limit='Gresk har en annen setningsbygning (infinitiv). Ordet φῶς svarer til אור og kan ikke avledes av MT-ordlyden.')])],
     'pluss', 'betydning',
     'Etter יִרְאֶה har tre Jesaja-ruller ordet אור, «lys», og Septuaginta har φῶς på samme sted. Den masoretiske teksten har verbet uten objekt, og R10 følger den: «skal han se». '
     'I 1QIsaᵃ og 4QIsaᵈ står det dessuten «og» foran det neste verbet, mens 1QIsaᵇ og MT ikke har det. I 4QIsaᵈ er siste bokstav i אור rekonstruert i transkripsjonen. '
     '4QIsaᵇ (4Q56) har bare slutten av verset og er ikke vitne på dette stedet. Om «lys» er falt ut i MT eller lagt til i de andre vitnene, er en vurdering og er ikke gjort her.',
     leads=['Dateringen av de tre rullene hentes fra DJD XV og DJD XXXII av navngitt leser. Leon Levy oppgir bare periode.'])

# ===================== 2. 5 Mos 32,8 =====================
unit('GT-DEU-032-008-01', 2, {'r10': '5 Mos 32,8', 'mtRef': 'Deut.32.8', 'stepPublicationRef': 'Deu.32.8', 'lxxRef': 'Deut 32:8'},
     gt_anchor('gt-deut', 32, 8, '05K67', '05hVg', 'erstatter'),
     [rd('a', 'MT: «Israels sønner»', 'בְּנֵי יִשְׂרָאֵל', 'he', 'Substantiv, maskulinum flertall, konstruktus + egennavn.', [N('Israels sønner', 'r10')],
         eds=[ed_r10(), ed_mam('Deuteronomy.32.8', r'למספר בני ישראל')], mss=[b19a('בני ישראל')], isR10=True),
      rd('b', '«Guds sønner»', 'בני אלוהים', 'he', 'Substantiv, maskulinum flertall, konstruktus + אלוהים (plene skrivemåte).', [N('Guds sønner')],
         mss=[dss('4QDeutj', 'Deut 32:8', r'בניאלוהים', note='De to ordene er lest. Resten av verset er rekonstruert i transkripsjonen.')],
         vers=[lxx('Deut 32:8', r'κατα αριθμον αγγελων θεου', 'ἀγγέλων θεοῦ', [N('Guds engler')], 'sannsynlig',
                   limit='Gresk har «engler», ikke «sønner». Ordlyden forutsetter et gudsnavn i forelegget og kan ikke avledes av «Israels sønner».')])],
     'leksikalsk', 'betydning',
     'Forskjellen gjelder hvem tallet viser til. MT har «Israels sønner», og R10 følger den. 4QDeutʲ har בני אלוהים, «Guds sønner». Swetes greske tekst har ἀγγέλων θεοῦ, «Guds engler». '
     'R10-noten til verset viser til Tovs drøfting av stedet. 4QpaleoDeutʳ (4Q45) har deler av verset, men ordene det gjelder, er rekonstruert der, så rullen er ikke vitne. '
     '4QDeutᑫ har ikke bevart verset. Vurderingen av hvilken lesning som er eldst, hører til akse 3 og er ikke gjort.',
     leads=['Greske håndskrifter med υἱῶν θεοῦ, «Guds sønner», oppgis i Wevers’ Göttingen-utgave. Sigla og datering må leses der og i Rahlfs–Fraenkel før de registreres.',
            'Den samaritanske Pentateuk oppgis å lese som MT. Stedet må leses i von Gall.'])

# ===================== 3. 5 Mos 32,43 =====================
d_heb, h_heb = book('heb'); v_heb = verse(d_heb, 1, 6)
heb_words = ' '.join(w['g'] for w in v_heb['w'][10:16])
odae = gnorm(SW['records']['Odae 2:43'])
assert gnorm(heb_words).replace('παντεσ αγγελοι', 'παντεσ οι αγγελοι') in odae
frag = ['ευφρανθητε ουρανοι αμα αυτω', 'και προσκυνησατωσαν αυτω υιοι', 'ευφρανθητε εθνη μετα του λαου αυτου', 'το αιμα των υιων αυτου', 'και τοισ μισουσιν ανταποδωσει', 'εκκαθαριει κυριοσ την γην του λαου αυτου']
assert all(f in gnorm(SW['records']['Deut 32:43']) for f in frag)
used.add('LXX'); a43, v43 = gt_anchor('gt-deut', 32, 43, '05w7w', '05CFi', 'hele_verset')
unit('GT-DEU-032-043-01', 3, {'r10': '5 Mos 32,43', 'mtRef': 'Deut.32.43', 'stepPublicationRef': 'Deu.32.43', 'lxxRef': 'Deut 32:43; Odae 2:43'}, (a43, v43),
     [rd('a', 'MT: kortere tekst', v43['mtText'], 'he', 'Fire ledd: oppfordring til folkeslagene, hevn for tjenernes blod, gjengjeldelse, soning for land og folk.',
         [N(v43['t'], 'r10')], eds=[ed_r10(), ed_mam('Deuteronomy.32.43', r'^הרנינו גוים עמו כי דם עבדיו יקום ונקם ישיב לצריו וכפר אדמתו עמו( [פס])?$')],
         mss=[b19a(hnorm(v43['mtText']))], isR10=True),
      rd('b', '4QDeutᑫ: lengre tekst', 'הרנינו שמים עמו והשתחוו לו כל אלהים כי דם בניו יקום ונקם ישיב לצריו ולמשנאיו ישלם ויכפר אדמת עמו', 'he',
         'Seks ledd. Oppfordringen går til himlene, ikke folkeslagene. Leddet om tilbedelse og leddet om dem som hater ham, står ikke i MT. «Sønner» der MT har «tjenere».',
         [N('Juble, himler, med ham, og tilbe ham, alle guder! For sine sønners blod skal han hevne, og hevn skal han vende tilbake over sine motstandere; dem som hater ham, skal han gjengjelde, og han skal gjøre soning for sitt folks land.'),
          N('Juble, himler, over hans folk …', 'tolkende', 'עמו er uvokalisert og kan leses «med ham» (slik gresk har) eller «hans folk» (slik MT vokaliserer ordet).')],
         mss=[dss('4QDeutq', 'Deut 32:43', r'הרנינושמיםעמווהשתחוולוכלאלהיםכידםבניויקוםונקםישיבלצריוולמשנאיוישלםויכפראדמתעמו')]),
      rd('c', 'LXX: lengre tekst', 'εὐφράνθητε, οὐρανοί, ἅμα αὐτῷ, καὶ προσκυνησάτωσαν αὐτῷ πάντες οἱ ἄγγελοι θεοῦ· εὐφράνθητε, ἔθνη, μετὰ τοῦ λαοῦ αὐτοῦ, καὶ ἐνισχυσάτωσαν αὐτῷ πάντες υἱοὶ θεοῦ· ὅτι τὸ αἷμα τῶν υἱῶν αὐτοῦ ἐκδικεῖται, καὶ ἐκδικήσει, καὶ ἀνταποδώσει δίκην τοῖς ἐχθροῖς· καὶ τοῖς μισοῦσιν ἀνταποδώσει δίκην, καὶ ἐκκαθαριεῖ Κύριος τὴν γῆν τοῦ λαοῦ αὐτοῦ.',
         'grc', 'Åtte ledd. Teksten er gjengitt etter Odae 2:43 hos Swete, der den er hel. Imperativ 3. person flertall i προσκυνησάτωσαν og ἐνισχυσάτωσαν.',
         [N('Gled dere, himler, sammen med ham, og alle Guds engler skal tilbe ham. Gled dere, folkeslag, sammen med hans folk, og alle Guds sønner skal styrke seg i ham. For hans sønners blod blir hevnet, og han skal hevne og gjengjelde fiendene med dom; dem som hater, skal han gjengjelde med dom, og Herren skal rense sitt folks land.')],
         vers=[{'siglum': 'LXX-Od', 'text': 'καὶ προσκυνησάτωσαν αὐτῷ πάντες οἱ ἄγγελοι θεοῦ', 'lang': 'grc', 'readIn': 'SWETE', 'locator': 'Odae 2:43', 'vorlage': 'kan ikke avgjøres',
                'norwegian': [N('og alle Guds engler skal tilbe ham')],
                'verification': {'status': 'BEKREFTET_UTGAVETEKST', 'evidence': 'kilder/belegg/swete-utdrag.json#Odae 2:43', 'basis': 'Swetes tekst i digital form. Verset er helt i datasettet.'}},
               {'siglum': 'LXX', 'text': 'καὶ προσκυνησάτωσαν αὐτῷ ⟨…⟩ υἱοὶ ⟨…⟩', 'lang': 'grc', 'readIn': 'SWETE', 'locator': 'Deut 32:43', 'vorlage': 'sannsynlig',
                'witnessLimit': 'Den digitale Swete-teksten har OCR-tap i dette verset. ⟨…⟩ markerer tapene. Seks ledd er funnet i teksten, resten må leses i trykt utgave.',
                'verification': {'status': 'DELVIS_BEKREFTET', 'evidence': 'kilder/belegg/swete-utdrag.json#Deut 32:43', 'basis': 'Leddene som er funnet: ' + '; '.join(frag) + '.',
                                 'mustReadIn': 'Swete, The Old Testament in Greek, bind I, 5 Mos 32:43'}}])],
     'pluss', 'betydning',
     'Verset finnes i tre former. MT har fire ledd, og R10 følger MT. 4QDeutᑫ har seks ledd, og den greske teksten har åtte. De to lange formene er ikke like: rullen har «alle guder» der gresk har «Guds engler» og «Guds sønner». '
     'Den greske teksten er her gjengitt etter Odae 2:43 hos Swete, fordi den digitale Swete-teksten til 5 Mos 32:43 har tap. I 5 Mos-formen står «sønner» i tilbedelsesleddet, i Odae-formen «engler». '
     'Hebr 1,6 i R10 har ordlyden «Καὶ προσκυνησάτωσαν αὐτῷ πάντες ἄγγελοι Θεοῦ». Den er lik Odae 2:43 bortsett fra artikkelen οἱ. Etter planens regel er et NT-sitat som kan avledes av kjent gresk tekst, ikke et uavhengig vitne.',
     crossReferences=[{'ref': 'Hebr 1,6', 'relation': 'NT-sitat', 'independentWitness': False, 'computed': True,
                       'anchor': {'testament': 'NT', 'bookId': 'heb', 'bookSha256': h_heb, 'r11LayerSha256': LOCK['books']['heb']['r11LayerSha256'], 'chapter': 1, 'verse': 6, 'firstWordIndex': 11, 'lastWordIndex': 16,
                                  'relation': 'erstatter', 'words': [{'wordIndex': k, 'g': v_heb['w'][k - 1]['g']} for k in range(11, 17)]},
                       'comparison': {'hebr': gnorm(heb_words), 'odae': 'και προσκυνησατωσαν αυτω παντεσ οι αγγελοι θεου', 'differsOnlyBy': ['οι']},
                       'basis': 'Plan 2.3 og punkt 3 i planens innledning: sitatet avviker ikke fra kjent gresk tekst utover artikkelen.'}],
     leads=['Sal 96:7 LXX er en annen mulig kilde for ordlyden i Hebr 1,6. Stedet er ikke hentet i Trinn 0.',
            'Swete-teksten til 5 Mos 32:43 må leses i trykt utgave før LXX-lesningen kan låses.'])

# ===================== 4. Sal 22,17 =====================
a22, v22 = gt_anchor('gt-ps', 22, 17, '19dCM', '19dCM', 'erstatter')
unit('GT-PSA-022-017-01', 4, {'r10': 'Sal 22,17', 'mtRef': 'Ps.22.17', 'stepPublicationRef': 'Psa.22.16', 'western': 'Sal 22,16', 'lxxRef': 'Ps 21:17'}, (a22, v22),
     [rd('a', 'MT: «som en løve»', 'כָּאֲרִי', 'he', 'Preposisjon כְּ med artikkel + substantiv, maskulinum entall, absolutt form.', [N('som en løve', 'r10')],
         eds=[ed_r10(), ed_mam('Psalms.22.17', r'כארי ידי ורגלי')], mss=[b19a('כארי ידי ורגלי')], isR10=True),
      rd('b', 'verbform med waw', 'כארו', 'he', 'Sluttbokstaven er waw, ikke jod. Formen leses som verb, 3. person flertall, qatal. Rot og betydning er omstridt.',
         [N('de har gravd', 'ordrett', 'Hvis formen hører til en rot for «grave». BDB drøfter rot og betydning med forbehold.'),
          N('de har gjennomboret', 'tolkende', 'Den tradisjonelle gjengivelsen i KJV og Bibelen 1930. Den tar stilling til hva gravingen betyr.')],
         mss=[dss('5/6HevPs', 'Ps 22:17', r'כארו(?=ידי)')],
         vers=[lxx('Ps 21:17', r'ωρυξαν χειρασ μου και ποδασ', 'ὤρυξαν', [N('de gravde')], 'sannsynlig', limit='Gresk har et verb i 3. person flertall. Det forutsetter en verbform i forelegget, ikke «som en løve».')]),
      rd('b2', 'verbform uten alef (usikker)', 'כר[ו]', 'he', 'Tre bokstaver, de to første usikre og den siste rekonstruert i transkripsjonen.', [N('de har gravd')],
         mss=[dss('4QPsf', 'Ps 22:17', r'כרו(?=ידי)', note='Lesningen er usikker. Bare en ny avlesing av fragmentet kan avgjøre om rullen støtter verbformen.')], agreesWith='b')],
     'leksikalsk', 'betydning',
     'Lesningen og tolkningen holdes adskilt. MT har כָּאֲרִי, «som en løve», og R10 følger MT: «som en løve er de over mine hender og mine føtter». Verbet i R10-setningen er en norsk utfylling. '
     'Salmerullen fra Nahal Hever har כארו med waw, og Swetes greske tekst har ὤρυξαν, «de gravde». Derfor har lesning b to gjengivelser: den ordrette og den tradisjonelle. '
     '4QPsᶠ har bare usikre bokstaver på stedet. Adressen er Sal 22,17 i MT og 22,16 i vestlig nummerering. I gresk er det Sal 21,17.')

# ===================== 5. Sal 145,13 =====================
a145, v145 = gt_anchor('gt-ps', 145, 13, '19tHU', '19tHU', 'etter')
unit('GT-PSA-145-013-01', 5, {'r10': 'Sal 145,13', 'mtRef': 'Ps.145.13', 'stepPublicationRef': 'Psa.145.13', 'lxxRef': 'Ps 144:13a'}, (a145, v145),
     [rd('a', 'MT: uten nun-linjen', '', 'he', 'Akrostikonet går fra mem-linjen (v. 13) rett til samek-linjen (v. 14).', [N('(linjen står ikke i teksten)', 'r10')],
         eds=[ed_r10(), ed_mam('Psalms.145.13', r'בכל דור ודר$', 'Vers 13 slutter med ודר. Nun-linjen står ikke i verset.')],
         mss=[b19a('', 'Ingen linje mellom v. 13 og v. 14.')], isR10=True, textNote='Tom lesning: linjen mangler.'),
      rd('b', 'nun-linjen', 'נאמן אלוהים בדבריו וחסיד בכול מעשיו', 'he', 'Nominalsetning i to ledd. Første ord begynner på nun. Gudsnavnet er אלוהים.',
         [N('Trofast er Gud i sine ord og god i alle sine gjerninger.')],
         mss=[dss('11QPsa', 'Ps 145:13', r'נאמןאלוהיםבדבריווחסידבכולמעשיו', note='Rullen har også et omkved etter hvert vers: «Velsignet være HERREN, og velsignet være hans navn for evig og alltid.»')],
         vers=[lxx('Ps 144:14 (trykt 13a + 14)', r'πιστοσ κυριοσ εν τοισ λογοισ αυτου και οσιοσ εν πασι τοισ εργοισ αυτου', 'πιστὸς Κύριος ἐν τοῖς λόγοις αὐτοῦ, καὶ ὅσιος ἐν πᾶσι τοῖς ἔργοις αὐτοῦ',
                   [N('Trofast er Herren i sine ord, og hellig i alle sine gjerninger.')], 'sannsynlig', loc_='Ps 144:13a',
                   limit='Gresk har Κύριος der rullen har אלוהים. Det digitale datasettet fører linjen under v. 14.')])],
     'pluss', 'betydning',
     'Salmen følger alfabetet, og mellom mem-linjen og samek-linjen mangler nun-linjen i MT. R10 følger MT. 11QPsᵃ har en nun-linje, og Swetes greske tekst har linjen som 144:13a. '
     'De to er ikke like i gudsnavnet: rullen har «Gud», gresk «Herren». חסיד er gjengitt «god», slik R10 gjengir ordet i vers 17. R10-noten til verset omtaler de samme vitnene.',
     leads=['Et middelaldersk hebraisk håndskrift (Kennicott) og den syriske oversettelsen oppgis også å ha linjen. De er ikke avlest.'])

# ===================== 6. Mark 1,1 =====================
MK = 'Mark.1.1'
unit('NT-MRK-001-001-01', 6, {'r10': 'Mark 1,1', 'ntRef': 'Mark 1,1'}, nt_anchor('mrk', 1, 1, 6, 8, 'erstatter'),
     [rd('a', 'υἱοῦ τοῦ θεοῦ', 'υἱοῦ τοῦ θεοῦ', 'grc', 'Substantiv, genitiv entall maskulinum + artikkel + substantiv, genitiv entall maskulinum.', [N('Guds Sønn', 'r10')],
         eds=[ed_r10(), ed_text('RP2018', 'Mark 1,1', 'RP2018', r'υιου του θεου$')],
         mss=[ms(s, MK, r'χυ(υυ|υιου)τουθυ$') for s in ('02', '017', '037', '041', '33', '565', '892', '1424', '700', '1', '13')],
         vers=[vg('Mark 1:1', r'filii dei', 'Filii Dei', [N('Guds Sønn')], LAT_ART, ['a', 'b'])],
         pats=[father('Iren-AH', 'III.10.5', 'Iren-AH@III.10.5', 'la', 'sitat', 'The beginning of the Gospel of Jesus Christ, the Son of God', LAT_ART, ['a', 'b']),
               father('Iren-AH', 'III.16.3', 'Iren-AH@III.16.3', 'la', 'sitat', 'The beginning of the Gospel of Jesus Christ, the Son of God', LAT_ART, ['a', 'b'])], isR10=True),
      rd('b', 'υἱοῦ θεοῦ', 'υἱοῦ θεοῦ', 'grc', 'Samme ord uten artikkel.', [N('Guds Sønn', 'ordrett', 'Norsk gjengivelse er lik lesning a.')],
         eds=[ed_tagnt('THGNT', 'Tyn', 'Mark 1,1', r'χριστου υιου θεου$'), ed_tagnt('TREG', 'Treg', 'Mark 1,1', r'χριστου υιου θεου$'),
              ed_na_rp('Mark 1,1', '{NA υἱοῦ τοῦ θεοῦ > [υἱοῦ θεοῦ] }', 'i hakeparentes')],
         mss=[ms('01', MK, r'χυυυθυ$', 'corrector1'), ms('03', MK, r'χυυιουθυ$'), ms('05', MK, r'χρυυιουθυ$'), ms('019', MK, r'χυυυθυ$'), ms('032', MK, r'χυυιουθυ$')]),
      rd('c', 'uten «Guds Sønn»', '', 'grc', 'Verset slutter med Ἰησοῦ Χριστοῦ.', [N('(ordene står ikke)')],
         eds=[ed_text('TISCH8', 'Mark 1,1', 'TISCH8', r'ιησου χριστου$'), ed_tagnt('SBLGNT', 'SBL', 'Mark 1,1', r'ιησου χριστου$'), ed_tagnt('WH', 'WH', 'Mark 1,1', r'ιησου χριστου$')],
         mss=[ms('01', MK, r'ευαγγελιουιυχυ$'), ms('038', MK, r'ευαγγελιουιυχυ$'), ms('28', MK, r'ευαγγελιουιυχυ$', 'corrector', 'Første hånd i 28 har bare ιυ. Korrektoren har lagt til χυ.')],
         pats=[father('Iren-AH', 'III.11.8', 'Iren-AH@III.11.8', 'la', 'sitat', 'The beginning of the Gospel of Jesus Christ, as it is written in Esaias the prophet'),
               father('Orig-Cels', 'II.4', 'Orig-Cels@II.4', 'grc', 'sitat', 'The beginning of the Gospel of Jesus Christ, as it is written in the prophet Isaiah'),
               father('Orig-CommJo', 'I.14 (ANF-inndeling)', 'Orig-CommJo@I.14(ANF)', 'grc', 'sitat', 'The beginning of the Gospel of Jesus Christ.')], textNote='Tom lesning: ordene mangler.')],
     'minus', 'betydning',
     'R10 følger Scrivener: «Guds Sønn» med artikkel foran θεοῦ. Robinson–Pierpont har det samme. Lesning b har de samme ordene uten artikkel og gir samme norske tekst. Lesning c har ikke ordene. '
     'Første hånd i Sinaiticus har ikke ordene, og en korrektor har lagt dem til uten artikkel. Irenæus er delt i oversettelsen: to steder har «Guds Sønn», ett har det ikke. '
     'Minuskel 1241 har ifølge transkripsjonen υἱοῦ τοῦ κυρίου og er ikke ført under noen av lesningene.',
     dataConflicts=['TAGNT fører opp NA28 i utgavefeltet for artikkelen τοῦ, mens ordtypen i samme rad og Robinson–Pierponts variantnote sier at NA-teksten har [υἱοῦ θεοῦ] uten artikkel. NA28 er ført under lesning b etter variantnoten og må leses i utgaven.'])

# ===================== 7. Joh 1,18 =====================
J = 'John.1.18'
unit('NT-JOH-001-018-01', 7, {'r10': 'Joh 1,18', 'ntRef': 'Joh 1,18'}, nt_anchor('joh', 1, 18, 5, 7, 'erstatter'),
     [rd('a', 'ὁ μονογενὴς υἱός', 'ὁ μονογενὴς υἱός', 'grc', 'Artikkel + adjektiv + substantiv, alle nominativ entall maskulinum.', [N('Den eneste Sønnen', 'r10')],
         eds=[ed_r10(), ed_text('RP2018', 'Joh 1,18', 'RP2018', r'ο μονογενησ υιοσ'), ed_text('TISCH8', 'Joh 1,18', 'TISCH8', r'ο μονογενησ υιοσ'), ed_tagnt('THGNT', 'Tyn', 'Joh 1,18', r'ο μονογενησ υιοσ')],
         mss=[ms('02', J, r'ομονογενησυιοσ'), ms('04', J, r'ομονογενησυσ', 'corrector3'), ms('037', J, r'ομονογενησυσ'), ms('038', J, r'ομονογενησυιοσ')],
         vers=[vg('John 1:18', r'unigenitus filius', 'unigenitus Filius', [N('den enbårne Sønn')], 'Latin viser «Sønn» mot «Gud», men ikke artikkelen.')],
         pats=[father('Iren-AH', 'III.11.6', 'Iren-AH@III.11.6', 'la', 'sitat', 'the only-begotten Son of God, which is in the bosom of the Father', note='Oversettelsen har «Son of God».'),
               father('Iren-AH', 'IV.20.6', 'Iren-AH@IV.20.6', 'la', 'sitat', 'the only-begotten Son, who is in the bosom of the Father'),
               father('Tert-Prax', '15', 'Tert-Prax@15', 'la', 'sitat', 'the only begotten Son, who is in the bosom of the Father'),
               father('Hipp-Noet', '5', 'Hipp-Noet@5', 'grc', 'sitat', 'the only-begotten Son, which is in the bosom of the Father'),
               father('Orig-Cels', 'II.71', 'Orig-Cels@II.71', 'grc', 'omstridt', 'the only-begotten Son, who is in the bosom of the Father',
                      note='Oversettelsen bygger på en eldre utgave. Hva den kritiske utgaven har på stedet, må leses før sitatet teller for en lesning.')], isR10=True),
      rd('b', 'μονογενὴς θεός', 'μονογενὴς θεός', 'grc', 'Adjektiv + substantiv, nominativ entall maskulinum, uten artikkel.',
         [N('den eneste Gud', 'ordrett', 'Slik R10-noten gjengir lesningen formnært.'), N('den eneste, som er Gud', 'tolkende', 'Forklarende gjengivelse fra R10-noten.')],
         eds=[ed_na_rp('Joh 1,18', '{NA ὁ μονογενὴς υἱός > μονογενὴς θεός }'), ed_tagnt('SBLGNT', 'SBL', 'Joh 1,18', r'πωποτε μονογενησ θεοσ'), ed_tagnt('WH', 'WH', 'Joh 1,18', r'πωποτε μονογενησ θεοσ'),
              ed_tagnt('TREG', 'Treg', 'Joh 1,18', r'πωποτε μονογενησ θεοσ')],
         mss=[ms('P66', J, r'πωποταιμονογενησθσ'), ms('01', J, r'πωποτεμονογενησθσ'), ms('03', J, r'πωποτεμονογενησθσ'), ms('04', J, r'πωποτεμονογενησθσ')],
         pats=[father('Iren-AH', 'IV.20.11', 'Iren-AH@IV.20.11', 'la', 'sitat', 'The only-begotten God, which is in the bosom of the Father', LAT_ART, ['b', 'c']),
               father('Clem-Strom', 'V.12', 'Clem-Strom@V.12', 'grc', 'sitat', 'The only-begotten God, who is in the bosom of the Father', 'Oversettelsen viser ikke om gresk har artikkel.', ['b', 'c']),
               father('Orig-CommJo', 'II.29 (ANF-inndeling)', 'Orig-CommJo@II.29(ANF)', 'grc', 'sitat', 'the only-begotten God, who is in the bosom of the Father', 'Oversettelsen viser ikke om gresk har artikkel.', ['b', 'c'])]),
      rd('c', 'ὁ μονογενὴς θεός', 'ὁ μονογενὴς θεός', 'grc', 'Som b, med artikkel.', [N('den eneste Gud')],
         mss=[ms('P75', J, r'ομονογενησθσ'), ms('01', J, r'πωποτεομονογενησθσ', 'corrector2')])],
     'leksikalsk', 'betydning',
     'R10 følger Scrivener: «Den eneste Sønnen». Robinson–Pierpont og Tischendorf har samme lesning, og TAGNT fører THGNT under den. De to tidligste papyrusene og første hånd i Sinaiticus, Vaticanus og Ephraemi har θεός, med eller uten artikkel. '
     'Alexandrinus har υἱός. I Ephraemi har en korrektor endret til υἱός, og i Sinaiticus har en korrektor lagt til artikkelen. Fedrene er delt, også innenfor samme verk hos Irenæus. '
     'Sitatene er bare funnet i engelsk oversettelse, og et latinsk eller oversatt sitat viser ikke artikkelen. R10-noten til verset omtaler de samme hovedvitnene.',
     leads=['Tatians, Klemens’ (Excerpta ex Theodoto) og Origenes’ øvrige sitater av verset må leses i kritiske utgaver før de registreres.',
            'THGNT-valget er belagt med én kilde (TAGNT) og bør leses i utgaven.'])

# ===================== 8. Apg 8,37 =====================
A, A0, A1 = 'Acts.8.37', 'Acts.8.36', 'Acts.8.38'
a8, v8 = nt_anchor('act', 8, 37, 1, 23, 'hele_verset')
P8 = r'^ειπεν?δεαυτωι?ειπιστευεισεξολησ(τησ)?καρδιασ(σου)?εξεστιναποκριθεισδεειπεν?πιστευωτον(υν|υιον)τουθυειναιινχν$'
unit('NT-ACT-008-037-01', 8, {'r10': 'Apg 8,37', 'ntRef': 'Apg 8,37'}, (a8, v8),
     [rd('a', 'verset i Scriveners form', ' '.join(w['g'] for w in v8['w']), 'grc', 'Hele verset. Scrivener har ὁ Φίλιππος som subjekt og ikke σου etter καρδίας.', [N(v8['t'], 'r10')],
         eds=[ed_r10()],
         vers=[vg('Acts 8:37', r'credo filium dei esse jesum christum', 'Dixit autem Philippus: Si credis ex toto corde, licet. Et respondens ait: Credo Filium Dei esse Jesum Christum.',
                  [N('Og Filip sa: Hvis du tror av hele hjertet, er det tillatt. Og han svarte og sa: Jeg tror at Jesus Kristus er Guds Sønn.')],
                  'Clementina har «Philippus» og ikke «tuo», som Scrivener. Den viser at verset står i den trykte Vulgata, ikke hvilke håndskrifter som har det.'),
               {'siglum': 'VL', 'lang': 'la', 'vorlage': 'kan ikke avgjøres', 'note': 'Oppdraget nevner Vetus Latina som vitne. Ingen gammellatinsk tekst er hentet i Trinn 0.',
                'verification': {'status': 'IKKE_AVLEST', 'mustReadIn': 'Vetus Latina-utgaven (Beuron) for Apostlenes gjerninger; håndskriftene må navngis med Beuron-nummer før de registreres.'}}], isR10=True),
      rd('a2', 'verset i minuskelform', 'εἶπε δὲ αὐτῷ· εἰ πιστεύεις ἐξ ὅλης τῆς καρδίας σου, ἔξεστιν· ἀποκριθεὶς δὲ εἶπε· πιστεύω τὸν υἱὸν τοῦ θεοῦ εἶναι Ἰησοῦν Χριστόν', 'grc',
         'Som a, men med αὐτῷ og uten ὁ Φίλιππος. De fleste har σου. Tre av håndskriftene har ikke τῆς.',
         [N('Og han sa til ham: «Hvis du tror av hele ditt hjerte, er det tillatt.» Og han svarte og sa: «Jeg tror at Jesus Kristus er Guds Sønn.»')],
         mss=[ms(s, A, P8) for s in ('1739', '1891', '307', '945', '323', '2818', '453')],
         pats=[father('Iren-AH', 'III.12.8', 'Iren-AH@III.12.8', 'la', 'sitat', 'I believe Jesus Christ to be the Son of God', 'Irenæus gjengir bare hoffmannens bekjennelse, ikke Filips vilkår.', ['a', 'a2']),
               father('Cypr-Quir', 'III.43', 'Cypr-Quir@III.43', 'la', 'sitat', 'Then said Philip, If thou believest with all thine heart, thou mayest', 'Cyprian gjengir v. 36 og Filips vilkår, ikke bekjennelsen.', ['a', 'a2'])], agreesWith='a'),
      rd('a3', 'verset i Laudianus’ form', 'εἶπεν δὲ αὐτῷ ὁ Φίλιππος· ἐὰν πιστεύεις ἐξ ὅλης τῆς καρδίας σου, σωθήσει· ἀποκριθεὶς δὲ εἶπεν· πιστεύω εἰς τὸν Χριστὸν τὸν υἱὸν τοῦ θεοῦ', 'grc',
         'Annen ordlyd: ἐάν, σωθήσει (futurum passiv 2. person entall) og πιστεύω εἰς.',
         [N('Og Filip sa til ham: «Hvis du tror av hele ditt hjerte, skal du bli frelst.» Og han svarte og sa: «Jeg tror på Kristus, Guds Sønn.»')],
         mss=[ms('08', A, r'^ειπενδεαυτωοφιλιπποσεανπιστευεισεξολωστησκαρδιασσουσωθησειαποκριθεισδεειπενπιστευωειστονχντονυιοντουθυ$'.replace('ολωσ', 'ολησ'))], agreesWith='a'),
      rd('b', 'uten verset', '', 'grc', 'Teksten går fra v. 36 rett til v. 38.', [N('(verset står ikke)')],
         eds=[ed_text('RP2018', 'Apg 8,37', 'RP2018'), ed_text('TISCH8', 'Apg 8,37', 'TISCH8')] + [ed_tagnt(e, t, 'Apg 8,37') for e, t in (('NA28', 'NA28'), ('THGNT', 'Tyn'), ('SBLGNT', 'SBL'), ('WH', 'WH'), ('TREG', 'Treg'))],
         mss=[ms_omit(s, A, A0, A1) for s in ('P45', 'P74', '01', '02', '03', '04', '020', '044', '049', '33', '81', '1175', '614', '18', '35')], textNote='Tom lesning: verset mangler.')],
     'pluss', 'betydning',
     'R10 følger Scrivener og har hele verset. Robinson–Pierpont har det ikke, og de andre utgavene har det heller ikke. Blant de transkriberte greske håndskriftene står verset i tre former, og ingen av dem har nøyaktig Scriveners ordlyd. '
     'Codex Laudianus fra 500-tallet er det eldste greske vitnet og har en egen form («skal du bli frelst»). Minusklene 1739 og 1891 fra 900-tallet har formen som ligger nærmest Scrivener. '
     'Irenæus og Cyprian gjengir hver sin del av verset. Begge er bare funnet i engelsk oversettelse, og begge skrev eller er overlevert på latin. '
     'Papyrus 45 er svært fragmentarisk her, så utelatelsen der bygger på utgiverens linjeberegning. Bezae mangler denne delen av Apostlenes gjerninger.',
     leads=['Minuskel 2816, som Erasmus brukte, har ingen publisert transkripsjon hos INTF. Margen der bør leses, fordi Scriveners ordlyd går tilbake til Erasmus.',
            'Vetus Latina-håndskriftene og Vulgata-håndskriftene må leses i utgavene før de registreres.'])

# ===================== 9. 1 Tim 3,16 =====================
T = '1Tim.3.16'
unit('NT-1TI-003-016-01', 9, {'r10': '1 Tim 3,16', 'ntRef': '1 Tim 3,16'},
     nt_anchor('1ti', 3, 16, 9, 9, 'erstatter', 'R11.1 retter ordkortet for dette ordet til «Gud». Rettelsen ligger i leseren og er bundet til bokfilens SHA-256. Bokfilen er uendret.'),
     [rd('a', 'Θεός', 'Θεός', 'grc', 'Substantiv, nominativ entall maskulinum. I majuskelskrift ΘΣ med strek over.', [N('Gud', 'r10')],
         eds=[ed_r10(), ed_text('RP2018', '1 Tim 3,16', 'RP2018', r'μυστηριον θεοσ εφανερωθη')],
         mss=[ms('01', T, r'(?<=μυστηριον)θεοσ(?=εφανερω)', 'corrector3'), ms('02', T, r'(?<=μυστηριον)θσ(?=εφανερω)', 'corrector'), ms('04', T, r'(?<=μυστηριον)θσ(?=εφανερω)', 'corrector3'),
              ms('6', T, r'(?<=μυστηριον)θσ(?=εφανερω)'),
              ms_unread('06', 'C2', 'Tischendorfs utgave av Codex Claromontanus (1852) eller bildene hos BnF', 'Oppdraget fører D² under denne lesningen. INTF har ingen publisert transkripsjon av stedet.')],
         pats=[father('Chrys-Hom1Tim', 'Hom. XI', 'Chrys-Hom1Tim@XI', 'grc', 'sitat', 'God was manifest in the flesh'),
               father('GregNyss-Eun', 'bok XI (NPNF-inndeling)', 'GregNyss-Eun@XI(NPNF)', 'grc', 'sitat', 'God was manifest in the flesh, justified in the spirit')], isR10=True),
      rd('b', 'ὅς', 'ὅς', 'grc', 'Relativpronomen, nominativ entall maskulinum. I majuskelskrift ΟΣ.', [N('han som')],
         eds=[ed_text('TISCH8', '1 Tim 3,16', 'TISCH8', r'μυστηριον οσ εφανερωθη'), ed_na_rp('1 Tim 3,16', '{NA θεὸς > ὃς }')] + [ed_tagnt(e, t, '1 Tim 3,16', r'μυστηριον οσ εφανερωθη') for e, t in (('THGNT', 'Tyn'), ('SBLGNT', 'SBL'), ('WH', 'WH'), ('TREG', 'Treg'))],
         mss=[ms(s, T, r'(?<=μυστηριον)οσ(?=εφανερω)') for s in ('01', '02', '04')]),
      rd('c', 'ὅ', 'ὅ', 'grc', 'Relativpronomen, nominativ entall nøytrum, som viser til μυστήριον.', [N('det som')],
         mss=[ms_unread('06', '*', 'Tischendorfs utgave av Codex Claromontanus (1852) eller bildene hos BnF', 'Oppdraget fører D* under denne lesningen. INTF har ingen publisert transkripsjon av stedet.')],
         vers=[vg('I Timothy 3:16', r'quod manifestatum est in carne', 'quod manifestatum est', [N('det som ble åpenbart')], 'Latin har relativpronomen i nøytrum, som viser til sacramentum. Det utelukker «Gud», men viser ikke sikkert om forelegget hadde ὅ eller ὅς.', ['b', 'c'])])],
     'leksikalsk', 'betydning',
     'R10 følger Scrivener: «Gud ble åpenbart i kjød». Robinson–Pierpont har samme lesning. I Sinaiticus, Alexandrinus og Ephraemi har første hånd ὅς, «han som», og en korrektor har endret til θεός i alle tre. '
     'I majuskelskrift skiller ΘΣ med strek seg fra ΟΣ med to streker. Minuskel 6 fra 1200-tallet er det eneste transkriberte håndskriftet med θεός i første hånd. De bysantinske majusklene har ingen publisert transkripsjon hos INTF. '
     'De to fedrene som er funnet med «Gud», er fra 300-tallet og ligger utenfor hovedvinduet. Ingen før-nikensk far er funnet med et ordrett sitat av stedet.',
     leads=['Oppdraget bruker betegnelsene ℵᵉ, A², C² og D². INTF-transkripsjonene kaller hendene korrektor 3 (01), korrektor (02) og korrektor 3 (04). Samsvaret mellom Tischendorfs, NA28s og INTFs korrektorbetegnelser må leses i utgavene.',
            'De bysantinske majusklene K 018, L 020, P 025 og Ψ 044 har ingen publisert transkripsjon av verset hos INTF og er derfor ikke registrert.',
            'Fedre som oppgis for ὅς i håndbøkene, må leses i kritiske utgaver før de registreres.',
            'Papyrus 133 har verset, men stedet er rekonstruert i transkripsjonen.'])

# ===================== 10. Åp 22,19 =====================
R = 'Rev.22.19'
LAC = TRANS['lacunaChecks']
for s in ('025', '04'): used.add(s)
unit('NT-REV-022-019-01', 10, {'r10': 'Åp 22,19', 'ntRef': 'Åp 22,19'}, nt_anchor('rev', 22, 19, 19, 21, 'erstatter'),
     [rd('a', 'βίβλου τῆς ζωῆς', 'βίβλου τῆς ζωῆς', 'grc', 'Substantiv, genitiv entall femininum + artikkel + substantiv, genitiv entall femininum.', [N('livets bok', 'r10')],
         eds=[ed_r10()],
         vers=[vg('Revelation of John 22:19', r'de libro vit', 'de libro vitæ', [N('fra livets bok')], 'Latin har liber, «bok». Det latinske ordet for «tre» er lignum, og de to ordene ligner hverandre i genitiv og ablativ (libro, ligno).')], isR10=True),
      rd('b', 'τοῦ ξύλου τῆς ζωῆς', 'τοῦ ξύλου τῆς ζωῆς', 'grc', 'Artikkel + substantiv, genitiv entall nøytrum + artikkel + substantiv, genitiv entall femininum.', [N('livets tre')],
         eds=[ed_text('RP2018', 'Åp 22,19', 'RP2018', r'απο του ξυλου τησ ζωησ'), ed_text('TISCH8', 'Åp 22,19', 'TISCH8', r'απο του ξυλου τησ ζωησ')] + [ed_tagnt(e, t, 'Åp 22,19', r'απο του ξυλου τησ ζωησ') for e, t in (('NA28', 'NA28'), ('THGNT', 'Tyn'), ('SBLGNT', 'SBL'), ('WH', 'WH'), ('TREG', 'Treg'))],
         mss=[ms(s, R, r'αποτουξυλουτησζωησ') for s in ('01', '02', '1006', '1854', '2050', '469', '35')] +
             [ms_unread('046', None, 'Bildene hos Biblioteca Apostolica Vaticana (Vat. gr. 2066, fol. 268r) eller ECM Apokalypse', 'Bladet med Åp 22,7–21 er bevart ifølge INTFs sideindeks, men stedet har ingen publisert transkripsjon.')])],
     'leksikalsk', 'betydning',
     'R10 følger Scrivener: «livets bok». Alle de transkriberte greske håndskriftene har «livets tre», også de to eldste, og Robinson–Pierpont har samme lesning. Scriveners lesning er her belagt i den latinske Clementina. '
     'Ingen gresk håndskrift med βίβλου er bekreftet i Trinn 0. Oppdraget nevner P (025) som vitne for «livets tre». INTFs sideindeks viser at håndskriftet slutter med Åp 22,2–6, så stedet er ikke bevart der. Ephraemi slutter i Åp 19,5.',
     excludedWitnesses=[{'siglum': '025', 'reason': 'Lakune: siste indekserte side med Åpenbaringen er fol. %s (%s).' % (LAC['025@Rev.22.19']['lastIndexedPageOfBook']['folio'], LAC['025@Rev.22.19']['lastIndexedPageOfBook']['indexContent']),
                         'evidence': 'kilder/belegg/intf-transkripsjoner.json#lacunaChecks/025@Rev.22.19', 'sha256': LAC['025@Rev.22.19']['rawSha256']},
                        {'siglum': '04', 'reason': 'Lakune: siste indekserte side med Åpenbaringen er fol. %s (%s).' % (LAC['04@Rev.22.19']['lastIndexedPageOfBook']['folio'], LAC['04@Rev.22.19']['lastIndexedPageOfBook']['indexContent']),
                         'evidence': 'kilder/belegg/intf-transkripsjoner.json#lacunaChecks/04@Rev.22.19', 'sha256': LAC['04@Rev.22.19']['rawSha256']}],
     leads=['Minusklene 296 og 2049 oppgis å ha βίβλου og å være avskrifter av trykte utgaver. Ingen av dem har publisert transkripsjon av stedet hos INTF.',
            'Latinske fedre som oppgis for «libro» (Ambrosius, De paradiso, CPL 124; Primasius, kommentaren til Åpenbaringen, CPL 873), er ikke avlest. Clavis-numrene er slått opp.',
            'Hvilke Vulgata-håndskrifter som har libro og hvilke som har ligno, leses i Stuttgart-utgavens apparat.'])

# ---------------- vitneregister ----------------
LET = {'01': 'ℵ', '02': 'A', '03': 'B', '04': 'C', '05': 'D', '06': 'D', '08': 'E', '017': 'K', '019': 'L', '020': 'L', '025': 'P', '032': 'W', '037': 'Δ', '038': 'Θ', '041': 'Π', '044': 'Ψ'}
NAME = {'01': 'Codex Sinaiticus', '02': 'Codex Alexandrinus', '03': 'Codex Vaticanus', '04': 'Codex Ephraemi Rescriptus', '05': 'Codex Bezae', '06': 'Codex Claromontanus', '08': 'Codex Laudianus', '025': 'Codex Porphyrianus'}
reg = {}
for s in sorted(used):
    if s in LISTE['records']:
        L = LISTE['records'][s]
        typ = 'papyrus' if s.startswith('P') else ('majuskel' if s.startswith('0') else 'minuskel')
        disp = ('𝔓' + s[1:]) if typ == 'papyrus' else ((LET[s] + ' ' + s) if s in LET else s)
        reg[s] = {'siglum': s, 'display': disp, 'type': typ, 'tradition': 'NT gresk', 'gaNumber': s, 'intfDocId': L['docID'], 'century': L['orig'],
                  'dateRange': {'notBefore': L['origEarly'], 'notAfter': L['origLate']},
                  'repository': [{'institution': x['institution'], 'place': x['place'], 'country': x['country'], 'shelfmark': x['shelfNumber']} for x in L['shelfInstances']],
                  'referenceSource': {'register': 'INTF-LISTE', 'url': L['url'], 'sha256': L['rawSha256'], 'retrieved': '2026-11-25'}, 'verification': 'IMPORTERT'}
        if s in NAME: reg[s]['commonName'] = NAME[s]
        if str(L['orig']) == 'XI' and L['origEarly'] == 900: reg[s]['registerNote'] = 'INTF-posten oppgir århundre XI og årstallene 900–999. Begge er gjengitt slik de står.'
LLQ = {'1QIsab': '1Q8', '4QIsad': '4Q58', '4QDeutj': '4Q37', '4QDeutq': '4Q44', '4QPsf': '4Q88', '11QPsa': '11Q5'}
DISP = {'1QIsaa': '1QIsaᵃ', '1QIsab': '1QIsaᵇ', '4QIsad': '4QIsaᵈ', '4QDeutj': '4QDeutʲ', '4QDeutq': '4QDeutᑫ', '5/6HevPs': '5/6ḤevPs', '4QPsf': '4QPsᶠ', '11QPsa': '11QPsᵃ'}
for s in sorted(used & set(SCROLL)):
    e = {'siglum': s, 'display': DISP[s], 'type': 'rulle', 'tradition': 'Q', 'etcbcScrollCode': SCROLL[s], 'century': None, 'dateRange': None,
         'dateStatus': 'Ikke importert. Årstallsintervall hentes fra DJD eller Tov, Revised Lists, av navngitt leser.', 'repository': None,
         'referenceSource': {'register': 'ETCBC-DSS', 'note': 'Rullen finnes under denne koden i datasettet.', 'commit': DSS['commit']},
         'siglumNote': 'Bokstavindeksen følger vanlig nomenklatur og er ikke kontrollert mot Tov, Revised Lists.', 'verification': 'DELVIS'}
    if s in LLQ and LLQ[s] in LL['records']:
        l = LL['records'][LLQ[s]]
        e.update({'inventoryNumber': LLQ[s], 'period': l['period'], 'site': l['site'], 'material': l['material'], 'imageUrl': l['url'],
                  'officialPublications': l['official_publications'], 'catalogSource': {'register': 'LEON-LEVY', 'url': l['url'], 'sha256': l['rawSha256'], 'name': l['name']}})
        e['dateStatus'] = 'Leon Levy oppgir perioden «%s». Årstallsintervall er ikke importert og hentes fra DJD av navngitt leser.' % l['period']
    reg[s] = e
reg['B19A'] = {'siglum': 'B19A', 'display': 'B19ᴬ (Codex Leningradensis)', 'type': 'hebraisk_kodeks', 'tradition': 'M', 'century': None, 'dateRange': None,
               'dateStatus': 'Ikke importert. Kolofonåret hentes fra WLC/UXLC-dokumentasjonen av navngitt leser.', 'repository': None,
               'referenceSource': {'register': 'WLC-OSHB', 'note': 'WLC er en transkripsjon av håndskriftet, og R10 bygger på WLC/OSHB.'}, 'verification': 'DELVIS'}
reg['LXX'] = {'siglum': 'LXX', 'display': 'LXX', 'type': 'oversettelse', 'tradition': 'G', 'language': 'grc', 'century': None, 'dateRange': None,
              'dateStatus': 'Oversettelsen registreres uten årstall. Håndskriftene bak Swetes tekst registreres først når de er lest i Rahlfs–Fraenkel, Verzeichnis.',
              'referenceSource': {'register': 'SWETE', 'note': 'Lesningene er hentet fra Swetes utgave, som i hovedsak trykker Codex Vaticanus.'}, 'verification': 'DELVIS'}
reg['LXX-Od'] = {'siglum': 'LXX-Od', 'display': 'LXX Odae', 'type': 'oversettelse', 'tradition': 'G', 'language': 'grc', 'century': None, 'dateRange': None,
                 'dateStatus': 'Som LXX. Odene står etter Salmene i enkelte greske håndskrifter.', 'referenceSource': {'register': 'SWETE', 'note': 'Odae 2 hos Swete.'}, 'verification': 'DELVIS'}
reg['Vg-Clem'] = {'siglum': 'Vg-Clem', 'display': 'Vulgata Clementina', 'type': 'oversettelse', 'tradition': 'Vg', 'language': 'la', 'century': None, 'dateRange': None,
                  'dateStatus': 'Trykt utgave av den latinske oversettelsen. Vulgata-håndskriftene er ikke registrert.', 'referenceSource': {'register': 'VG-CLEM', 'sha256': VG['fileSha256']}, 'verification': 'DELVIS'}
reg['VL'] = {'siglum': 'VL', 'display': 'Vetus Latina', 'type': 'oversettelse', 'tradition': 'VL', 'language': 'la', 'century': None, 'dateRange': None,
             'dateStatus': 'Samlebetegnelse. Enkelthåndskrifter registreres med Beuron-nummer når de er lest.', 'referenceSource': {'register': 'PATR-UTG', 'note': 'Vetus Latina-utgaven (Beuron).'}, 'verification': 'IKKE_KONTROLLERT'}
FATH = {'Iren-AH': ('Irenæus av Lyon', 'Adversus haereses', 'CPG 1306', 'grc', 'Verket er skrevet på gresk og er i hovedsak bevart i latinsk oversettelse.'),
        'Cypr-Quir': ('Cyprian av Karthago', 'Ad Quirinum (Testimoniorum libri III)', 'CPL 39', 'la', None),
        'Orig-Cels': ('Origenes', 'Contra Celsum', 'CPG 1476', 'grc', None), 'Orig-CommJo': ('Origenes', 'Commentarii in Iohannem', 'CPG 1453', 'grc', None),
        'Clem-Strom': ('Klemens av Alexandria', 'Stromata', 'CPG 1377', 'grc', None), 'Tert-Prax': ('Tertullian', 'Adversus Praxean', 'CPL 26', 'la', None),
        'Hipp-Noet': ('Hippolyt av Roma', 'Contra Noetum', 'CPG 1902', 'grc', None), 'GregNyss-Eun': ('Gregor av Nyssa', 'Contra Eunomium', 'CPG 3135', 'grc', None),
        'Chrys-Hom1Tim': ('Johannes Krysostomos', 'In epistulam I ad Timotheum homiliae', 'CPG 4436', 'grc', None)}
for s in sorted(used & set(FATH)):
    au, work, cno, lang, tn = FATH[s]; c = CL['records'][cno]
    reg[s] = {'siglum': s, 'display': '%s, %s' % (au, work), 'type': 'kirkefar_verk', 'tradition': 'fedre', 'author': au, 'work': work, 'language': lang,
              'clavis': {'series': c['series'], 'number': c['number'], 'placementAndTitle': c['treeAndTitle'], 'url': c['url'], 'sha256': c['rawSha256'], 'checked': '2026-11-25'},
              'window': 'hovedvindu' if c['anteNicene'] else 'utenfor hovedvinduet', 'windowBasis': 'Clavis Clavium fører verket under «%s».' % c['treeAndTitle'].split(' > ')[0],
              'century': None, 'dateRange': None, 'dateStatus': 'Ikke importert. Clavis-basen gir plassering, ikke årstall.', 'criticalEdition': EDN[s],
              'referenceSource': {'register': 'CLAVIS', 'url': c['url']}, 'verification': 'IMPORTERT (Clavis-nummer og plassering)'}
    if tn: reg[s]['transmissionNote'] = tn
missing = used - set(reg)
assert not missing, missing
register = {'schemaVersion': 'vitneregister.v1-trinn0', 'generated': '2026-11-25',
            'rule': 'Datering, type og oppbevaringssted står bare her. Ingen datering er skrevet inn for hånd: feltene century og dateRange er enten importert fra et register med SHA-256, eller tomme med en merknad om hvor de skal hentes.',
            'counts': {}, 'witnesses': reg}
import collections
register['counts'] = dict(collections.Counter(v['type'] for v in reg.values()))
register['counts']['medImportertDatering'] = sum(1 for v in reg.values() if v.get('dateRange'))
register['counts']['utenDatering'] = sum(1 for v in reg.values() if not v.get('dateRange'))

# ---------------- akse 1 og 2, og skriving ----------------
import unicodedata
for u in units:
    u['witnessPattern'] = pattern(u, register)
    u['variantKind']['computed'] = computed_kind(u)


def nfc(o):
    if isinstance(o, str): return unicodedata.normalize('NFC', o)
    if isinstance(o, list): return [nfc(x) for x in o]
    if isinstance(o, dict): return {k: (v if k == 'anchor' else nfc(v)) for k, v in o.items()}
    return o


def dump(rel, obj):
    with open(os.path.join(PROJ, rel), 'w', encoding='utf-8', newline='\n') as f:
        json.dump(nfc(obj), f, ensure_ascii=False, indent=1); f.write('\n')


# Ankerordene skal staa byte for byte som i R10. NFC ville byttet greske aksenttegn (oxia mot tonos),
# saa nfc() hopper over alle felt som heter anchor. Egne felt normaliseres til NFC.
doc = nfc({'schemaVersion': 'mlag.schema.v1-trinn0', 'generated': '2026-11-25', 'r10ReleaseId': LOCK['r10ReleaseId'], 'status': 'UTKAST',
           'notice': 'Utkast fra første registrering. Enhetene kan ikke låses før hvert vitne merket IKKE_AVLEST eller BEKREFTET_I_OVERSETTELSE er lest i kilden av navngitt leser, og før dobbel registrering er kjørt (plan 7.4).',
           'registers': {'witnesses': 'registre/vitneregister.json', 'sources': 'registre/kildelisenser.json', 'schema': 'registre/schema-manuscript-layer.json', 'r10Lock': 'registre/r10-laas.json'},
           'units': units})
with open(os.path.join(PROJ, 'piloter', 'trinn0-10-piloter.json'), 'w', encoding='utf-8', newline='\n') as f:
    json.dump(doc, f, ensure_ascii=False, indent=1); f.write('\n')
dump('registre/vitneregister.json', register)
st = collections.Counter(w['verification']['status'] for u in units for r in u['readings'] for k in ('editionSupport', 'manuscriptWitnesses', 'versionWitnesses', 'patristicWitnesses') for w in r[k])
print('enheter:', len(units), '| vitner i registeret:', len(reg), '|', dict(st))
for u in units: print(' ', u['pilotNr'], u['ref']['r10'], '|', u['witnessPattern']['code'], '|', u['variantKind'])
