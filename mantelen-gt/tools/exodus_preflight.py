#!/usr/bin/env python3
"""Bygger kildedelen av 02_2mosebok_PREFLIGHT.md fra offentlige grunntekstkilder.

Kjøring (stier til lokalt nedlastede kilder):

  python3 exodus_preflight.py --src <kildemappe> --nt <mappe med MANTELEN NT-json> \
      --out-md ../02_2mosebok_PREFLIGHT.md --out-app ../02_2mosebok_PREFLIGHT_ORDDATA.md \
      --out-json ../data/exodus_preflight.json [--kommentar anker_kommentar.json]

<kildemappe> må inneholde:
  oshb/Exod.xml, oshb/VerseMap.xml                 (openscriptures/morphhb, wlc/)
  step/TAHOT Gen-Deu*.txt                          (STEPBible/STEPBible-Data)
  scrivener/textonly/*.SCV                         (byztxt/greektext-scrivener)
  swete/data/02.Exodus.txt                         (nathans/lxx-swete)

Skriptet leser bare. Det endrer ingen bibelfil og skriver bare de tre utfilene.
Låst GT-ordlyd inngår ikke her; den føres i egen paritetsfil utenfor offentlig repo.
"""
import argparse
import collections
import glob
import hashlib
import json
import os
import re

import gtkilder as g

BOK = {'mat': ('Matt', 'MT'), 'mrk': ('Mark', 'MR'), 'luk': ('Luk', 'LU'), 'joh': ('Joh', 'JOH'),
       'act': ('Apg', 'AC'), 'rom': ('Rom', 'RO'), '1co': ('1 Kor', '1CO'), '2co': ('2 Kor', '2CO'),
       'gal': ('Gal', 'GA'), 'eph': ('Ef', 'EPH'), 'heb': ('Heb', 'HEB'), 'jam': ('Jak', 'JAS'),
       '1pe': ('1 Pet', '1PE'), 'rev': ('Åp', 'RE')}

# (id, tittel, WLC-vers, NT-steder, Swete-adresse der den avviker fra WLC)
ANKRE = [
    ('SK-01', 'Tornebusken: fedrenes Gud', [(3, 6)],
     ['mat 22:32', 'mrk 12:26', 'luk 20:37', 'act 3:13', 'act 7:32'], {}),
    ('SK-02', 'Navnet: «Jeg er»', [(3, 14)], ['joh 8:58', 'rev 1:4', 'rev 1:8'], {}),
    ('SK-03', 'Farao reist opp', [(9, 16)], ['rom 9:17'], {}),
    ('SK-04', 'Påskelammets bein', [(12, 46)], ['joh 19:36'], {}),
    ('SK-05', 'Den førstefødte helliges', [(13, 2), (13, 12)], ['luk 2:23'], {}),
    ('SK-06', 'Brød fra himmelen', [(16, 4), (16, 15)], ['joh 6:31'], {}),
    ('SK-07', 'Manna: ikke for mye, ikke for lite', [(16, 18)], ['2co 8:15'], {}),
    ('SK-08', 'Kongerike av prester', [(19, 5), (19, 6)], ['1pe 2:9', 'rev 1:6', 'rev 5:10'], {}),
    ('SK-09', 'Fjellet som ikke må røres', [(19, 12), (19, 13)], ['heb 12:20'], {}),
    ('SK-10', 'Dekalogen, annen tavle', [(20, 12), (20, 13), (20, 14), (20, 15), (20, 16), (20, 17)],
     ['mat 5:21', 'mat 5:27', 'mat 15:4', 'mat 19:18', 'mat 19:19', 'mrk 10:19', 'luk 18:20',
      'rom 7:7', 'rom 13:9', 'eph 6:2', 'eph 6:3', 'jam 2:11'], {}),
    ('SK-11', 'Den som forbanner far eller mor', [(21, 17)], ['mat 15:4', 'mrk 7:10'], {(21, 17): (21, 16)}),
    ('SK-12', 'Høvdingen i folket', [(22, 27)], ['act 23:5'], {(22, 27): (22, 28)}),
    ('SK-13', 'Paktens blod', [(24, 8)], ['heb 9:20', 'mat 26:28', 'mrk 14:24', 'luk 22:20', '1co 11:25'], {}),
    ('SK-14', 'Mønsteret på fjellet', [(25, 40)], ['act 7:44', 'heb 8:5'], {(25, 40): (25, 39)}),
    ('SK-15', 'Gullkalven', [(32, 1), (32, 6), (32, 23)], ['act 7:40', '1co 10:7'], {}),
    ('SK-16', 'Nåde og barmhjertighet', [(33, 19)], ['rom 9:15'], {}),
]

# Dekalogbud i NT: (nøkkel, norsk etikett, gresk stamme uten aksenter)
BUD = [('F', 'far og mor', 'τιμα'), ('D', 'drap', 'φονευσ'), ('E', 'ekteskapsbrudd', 'μοιχευσ'),
       ('S', 'stjele', 'κλεψ'), ('V', 'falskt vitne', 'ψευδομαρτυρησ'), ('B', 'begjære', 'επιθυμησ'),
       ('A', 'snyte (ἀποστερέω)', 'αποστερησ'), ('N', 'elske nesten', 'αγαπησεισ')]
BUD_NT = ['mat 19:18', 'mat 19:19', 'mrk 10:19', 'luk 18:20', 'rom 13:9', 'jam 2:11']

# EX-TERM: (id, hebraisk, translit, Strong-krav, norsk arbeidsetikett, NT-gresk, opphav)
# krav: liste av Strong-tall som må stå i rekkefølge innen 'vindu' ord; ett tall = enkeltlemma.
TERMER = [
    ('EX-TERM-01', 'פֶּסַח', 'pesach', [6453], 'påske / påskeoffer', 'τὸ πάσχα (G3957)', 'ordre'),
    ('EX-TERM-02', 'מַצָּה / מַצּוֹת', 'matsot', [4682], 'usyret brød', 'τὰ ἄζυμα (G0106)', 'ordre'),
    ('EX-TERM-03', 'כַּפֹּרֶת', 'kapporet', [3727], 'nådestol (TK-08 ifølge ordren)', 'ἱλαστήριον (G2435)', 'ordre'),
    ('EX-TERM-04', 'מִשְׁכָּן', 'mishkan', [4908], 'tabernakel / bolig (TK-22 ifølge ordren)', 'σκηνή (G4633)', 'ordre'),
    ('EX-TERM-05', 'אֹהֶל מוֹעֵד', 'ohel moed', [168, 4150], 'sammenkomstens telt (TK-22 ifølge ordren)',
     'ἡ σκηνὴ τοῦ μαρτυρίου (G4633 + G3142)', 'ordre'),
    ('EX-TERM-06', 'עֵדוּת', 'edut', [5715], 'vitnesbyrdet (alle forekomster)', 'τὸ μαρτύριον (G3142)', 'ordre'),
    ('EX-TERM-07', 'אֲרוֹן הָעֵדוּת', 'aron ha-edut', [727, 5715], 'vitnesbyrdets ark', 'ἡ κιβωτὸς τοῦ μαρτυρίου', 'ordre'),
    ('EX-TERM-08', 'לֻחֹת הָעֵדוּת', 'luchot ha-edut', [3871, 5715], 'vitnesbyrdets tavler', 'αἱ πλάκες τοῦ μαρτυρίου', 'ordre'),
    ('EX-TERM-09', 'מִשְׁכַּן הָעֵדוּת', 'mishkan ha-edut', [4908, 5715], 'vitnesbyrdets tabernakel',
     'ἡ σκηνὴ τοῦ μαρτυρίου', 'ordre'),
    ('EX-TERM-10', 'אֹהֶל הָעֵדוּת', 'ohel ha-edut', [168, 5715], 'vitnesbyrdets telt', 'ἡ σκηνὴ τοῦ μαρτυρίου', 'ordre'),
    ('EX-TERM-11', 'פָּרֹכֶת', 'parokhet', [6532], 'forhenget (det indre)', 'τὸ καταπέτασμα (G2665)', 'ordre'),
    ('EX-TERM-12', 'מָסָךְ', 'masakh', [4539], 'teppet / forhenget ved inngangen', 'LXX: ἐπίσπαστρον / καταπέτασμα', 'ordre'),
    ('EX-TERM-13', 'מִזְבַּח הָעֹלָה', 'mizbach ha-olah', [4196, 5930], 'brennofferalteret',
     'τὸ θυσιαστήριον (G2379)', 'ordre'),
    ('EX-TERM-14', 'מִזְבַּח (מִקְטַר) הַקְּטֹרֶת', 'mizbach ha-qetoret', [4196, 7004], 'røkelsesalteret',
     'τὸ θυσιαστήριον τοῦ θυμιάματος (Luk 1,11)', 'ordre'),
    ('EX-TERM-15', 'לֶחֶם (הַ)פָּנִים', 'lechem ha-panim', [3899, 6440], 'skuebrødene',
     'οἱ ἄρτοι τῆς προθέσεως (G0740 + G4286)', 'ordre'),
    ('EX-TERM-16', 'מִזְבֵּחַ', 'mizbeach', [4196], 'alter (alle forekomster, kontrolltall)', 'θυσιαστήριον (G2379)',
     'tillegg'),
    ('EX-TERM-17', 'אֲרוֹן', 'aron', [727], 'ark (alle forekomster)', 'ἡ κιβωτός (G2787)', 'tillegg'),
    ('EX-TERM-18', 'בְּרִית', 'berit', [1285], 'pakt', 'ἡ διαθήκη (G1242)', 'tillegg'),
    ('EX-TERM-19', 'תַּבְנִית', 'tavnit', [8403], 'mønster / forbilde', 'τύπος (G5179), παράδειγμα', 'tillegg'),
    ('EX-TERM-20', 'קֹדֶשׁ הַקֳּדָשִׁים', 'qodesh ha-qodashim', [6944, 6944], 'Det aller helligste',
     'ἅγια ἁγίων (G0039, Heb 9,3)', 'tillegg'),
]

STEM = {'q': 'qal', 'N': 'nifal', 'p': 'piel', 'P': 'pual', 'h': 'hifil', 'H': 'hofal', 't': 'hitpael',
        'o': 'polel', 'O': 'polal', 'r': 'hitpolel', 'm': 'poel', 'M': 'poal', 'k': 'palel', 'K': 'pulal',
        'Q': 'qal passiv', 'l': 'pilpel', 'L': 'polpal', 'f': 'hitpalpel', 'D': 'nitpael', 'j': 'pealal',
        'i': 'pilel', 'u': 'hotpaal', 'c': 'tifil', 'v': 'hishtafel', 'w': 'nitpalel', 'y': 'nitpoel',
        'z': 'hitpoel'}
VTYPE = {'p': 'perfektum', 'q': 'weqatal', 'i': 'imperfektum', 'w': 'wayyiqtol', 'h': 'kohortativ',
         'j': 'jussiv', 'v': 'imperativ', 'r': 'partisipp aktiv', 's': 'partisipp passiv',
         'a': 'infinitiv absolutt', 'c': 'infinitiv konstrukt'}
PERS = {'1': '1.', '2': '2.', '3': '3.'}
GEN = {'m': 'm', 'f': 'f', 'c': 'c', 'b': 'm/f'}
NUM = {'s': 'sg', 'p': 'pl', 'd': 'du'}
STATE = {'a': 'abs', 'c': 'kstr', 'd': 'best'}


def morf_no(code):
    """OSHB-morfologikode til kort norsk forklaring."""
    if not code:
        return ''
    out = []
    for i, seg in enumerate(code.split('/')):
        if i == 0:
            seg = seg[1:]  # språkmerke H/A
        if not seg:
            continue
        p, r = seg[0], seg[1:]
        if p == 'V':
            s = 'verb ' + STEM.get(r[:1], r[:1]) + ' ' + VTYPE.get(r[1:2], r[1:2])
            t = r[2:]
            if r[1:2] in 'rs':
                s += ' ' + ''.join(GEN.get(t[0:1], '')) + ' ' + NUM.get(t[1:2], '') + ' ' + STATE.get(t[2:3], '')
            elif r[1:2] not in 'ac':
                s += ' ' + PERS.get(t[0:1], '') + GEN.get(t[1:2], '') + ' ' + NUM.get(t[2:3], '')
            out.append(' '.join(s.split()))
        elif p == 'N':
            kind = {'c': 'subst', 'p': 'egennavn', 'g': 'gentilicium'}.get(r[:1], 'subst')
            s = kind + ' ' + GEN.get(r[1:2], '') + ' ' + NUM.get(r[2:3], '') + ' ' + STATE.get(r[3:4], '')
            out.append(' '.join(s.split()))
        elif p == 'A':
            kind = {'a': 'adj', 'c': 'grunntall', 'g': 'gentilicium', 'o': 'ordenstall'}.get(r[:1], 'adj')
            s = kind + ' ' + GEN.get(r[1:2], '') + ' ' + NUM.get(r[2:3], '') + ' ' + STATE.get(r[3:4], '')
            out.append(' '.join(s.split()))
        elif p == 'P':
            kind = {'d': 'dem.pron', 'f': 'ubest.pron', 'i': 'spørrepron', 'p': 'pers.pron', 'r': 'rel.pron'}.get(r[:1], 'pron')
            s = kind + ' ' + PERS.get(r[1:2], '') + GEN.get(r[2:3], '') + ' ' + NUM.get(r[3:4], '')
            out.append(' '.join(s.split()))
        elif p == 'S':
            kind = {'d': 'retnings-he', 'h': 'paragogisk he', 'n': 'paragogisk nun', 'p': 'suffiks'}.get(r[:1], 'suffiks')
            s = kind + ' ' + PERS.get(r[1:2], '') + GEN.get(r[2:3], '') + ' ' + NUM.get(r[3:4], '')
            out.append(' '.join(s.split()))
        elif p == 'T':
            out.append({'a': 'bekreftende part', 'd': 'artikkel', 'e': 'formaning', 'i': 'spørrepart',
                        'j': 'interjeksjon', 'm': 'påpekende part', 'n': 'nektelse', 'o': 'objektsmerke',
                        'r': 'relativpart'}.get(r[:1], 'partikkel'))
        elif p == 'C':
            out.append('konj')
        elif p == 'R':
            out.append('prep' + (' m/art' if r[:1] == 'd' else ''))
        elif p == 'D':
            out.append('adv')
        else:
            out.append(seg)
    return ' + '.join(out)


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for blk in iter(lambda: f.read(1 << 20), b''):
            h.update(blk)
    return h.hexdigest()


def find_term(ex, req, window=3):
    """Treff på lemmasekvens. Returnerer liste av (kap, vers, ordindeks, hebraisk form)."""
    hits = []
    for (c, v), toks in ex.items():
        ws = g.words(toks)
        nums = [g.strong_num(w['strong']) for w in ws]
        for i, n in enumerate(nums):
            if n != req[0]:
                continue
            if len(req) == 1:
                hits.append((c, v, i, ws[i]['h'].replace('/', '')))
                continue
            j_end = i
            ok = True
            for r in req[1:]:
                nxt = [j for j in range(j_end + 1, min(len(nums), j_end + 1 + window)) if nums[j] == r]
                if not nxt:
                    ok = False
                    break
                j_end = nxt[0]
            if ok:
                hits.append((c, v, i, ' '.join(w['h'].replace('/', '') for w in ws[i:j_end + 1])))
    return hits


def fmt_ref(c, v, vm):
    if (c, v) in vm:
        kc, kv, _ = vm[(c, v)]
        return '%d,%d [%d,%d]' % (c, v, kc, kv)
    return '%d,%d' % (c, v)


def compress(refs, vm):
    """[(kap, vers), ...] -> '25,17.18.19; 26,34' med vestlig nummer i klammer der det avviker."""
    by = collections.OrderedDict()
    for c, v in refs:
        by.setdefault(c, []).append(v)
    parts = []
    for c, vs in by.items():
        cnt = collections.Counter(vs)
        items = []
        for v in sorted(cnt):
            s = str(v)
            if (c, v) in vm:
                s += ' [%d,%d]' % vm[(c, v)][:2]
            if cnt[v] > 1:
                s += ' (x%d)' % cnt[v]
            items.append(s)
        parts.append('%d,%s' % (c, '.'.join(items)))
    return '; '.join(parts)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--src', required=True)
    ap.add_argument('--nt', required=True)
    ap.add_argument('--out-md', required=True)
    ap.add_argument('--out-app', required=True)
    ap.add_argument('--out-json', required=True)
    ap.add_argument('--kommentar')
    ap.add_argument('--hode')
    ap.add_argument('--kilder')
    a = ap.parse_args()

    p_ex = os.path.join(a.src, 'oshb', 'Exod.xml')
    p_vm = os.path.join(a.src, 'oshb', 'VerseMap.xml')
    p_ta = glob.glob(os.path.join(a.src, 'step', '**', 'TAHOT Gen-Deu*.txt'), recursive=True)[0]
    p_sw = os.path.join(a.src, 'swete', 'data', '02.Exodus.txt')
    ex = g.parse_oshb(p_ex)
    vm = g.parse_versemap(p_vm, 'Exod')
    ta = g.parse_tahot(p_ta, 'Exo')
    sw = g.parse_swete(p_sw)
    kommentar = json.load(open(a.kommentar, encoding='utf-8')) if a.kommentar else {}
    kilder = json.load(open(a.kilder, encoding='utf-8')) if a.kilder else {}

    nt, sc, ntmeta = {}, {}, {}

    def ntv(ref):
        b, cv = ref.split()
        c, v = map(int, cv.split(':'))
        if b not in nt:
            nt[b], ntmeta[b] = g.load_nt_book(os.path.join(a.nt, b + '.json'))
            sc[b] = g.parse_scrivener(os.path.join(a.src, 'scrivener', 'textonly', BOK[b][1] + '.SCV'))
        return BOK[b][0], c, v, nt[b].get((c, v), {}).get('t', ''), sc[b].get((c, v), '')

    L = []
    w = L.append
    data = {'bok': 'Exod', 'kilder': {}, 'versparitet': {}, 'ankre': [], 'termer': []}

    # ---------- hode ----------
    if a.hode:
        w(open(a.hode, encoding='utf-8').read().rstrip())
        w('')
    w('## Kilder brukt i denne kjøringen')
    w('')
    w('| Kilde | Fil | SHA-256 | Festet ved |')
    w('|---|---|---|---|')
    for navn, path, key in (('OSHB / WLC', p_ex, 'oshb'), ('OSHB VerseMap', p_vm, 'oshb'),
                            ('STEP TAHOT Gen-Deu', p_ta, 'step'), ('Swete LXX Exodus', p_sw, 'swete'),
                            ('Scrivener 1894 (Robinson)', os.path.join(a.src, 'scrivener', 'textonly', 'RO.SCV'), 'scrivener')):
        h = sha256(path)
        data['kilder'][os.path.basename(path)] = h
        w('| %s | `%s` | `%s` | %s |' % (navn, os.path.basename(path), h, kilder.get(key, '')))
    w('')
    w('MANTELEN NT er lest fra offentlig leserdata (%s).' % kilder.get('nt', 'mantelen.no'))
    w('')

    # ---------- 3.1 ----------
    cc = collections.Counter(c for c, _ in ex)
    kj = collections.Counter(vm.get(k, (k[0], k[1]))[0] for k in ex)
    swc = collections.Counter(k[0] for k in sw)
    nwords = sum(len(g.words(t)) for t in ex.values())
    w('## 3.1 Vers- og kapittelparitet')
    w('')
    w('Maskinelt resultat: OSHB/WLC har %d kapitler, %d vers og %d ordposter i 2. Mosebok. '
      'STEP/TAHOT har %d vers og %d ordrader. Ordantallet stemmer i alle vers (avvik: %d). '
      'TAHOTs engelske adresse stemmer med OSHB VerseMap i alle vers (avvik: %d).' % (
          len(cc), len(ex), nwords, len(ta), sum(map(len, ta.values())),
          sum(1 for k in ex if len(g.words(ex[k])) != len(ta.get(k, []))),
          sum(1 for k in ex if k in ta and ta[k][0]['eng'] != vm.get(k, (k[0], k[1]))[:2])))
    w('')
    w('### 3.1.1 Kapitler der verstallet avviker')
    w('')
    w('| Kapittel | WLC (OSHB) | Vestlig (KJV, VerseMap) | Swete LXX (denne digitale utgaven) |')
    w('|---|---|---|---|')
    for c in range(1, 41):
        if cc[c] != kj[c]:
            w('| %d | %d | %d | %d |' % (c, cc[c], kj[c], swc[c]))
    w('| Sum hele boken | %d | %d | %d |' % (sum(cc.values()), sum(kj.values()), sum(swc.values())))
    w('')
    w('Kapittel 20 har %d vers i WLC og %d i vestlig nummerering; det er ingen forskyvning i dekalogen i denne kilden.'
      % (cc[20], kj[20]))
    w('')
    w('### 3.1.2 Alle %d forskjøvne vers' % len(vm))
    w('')
    w('| WLC | Vestlig | Forskyvning | Første ord i WLC |')
    w('|---|---|---|---|')
    blocks = []
    for k, (kc, kv, typ) in vm.items():
        if blocks and blocks[-1]['wlc'][-1][0] == k[0] and blocks[-1]['kjv'][-1][0] == kc \
                and blocks[-1]['wlc'][-1][1] + 1 == k[1]:
            blocks[-1]['wlc'].append(k)
            blocks[-1]['kjv'].append((kc, kv))
        else:
            blocks.append({'wlc': [k], 'kjv': [(kc, kv)]})
    for b in blocks:
        a0, a1, k0, k1 = b['wlc'][0], b['wlc'][-1], b['kjv'][0], b['kjv'][-1]
        first = ' '.join(x['h'].replace('/', '') for x in g.words(ex[a0])[:3])
        if a0[0] != k0[0]:
            skift = 'kapittelgrense: %d vers flyttet' % len(b['wlc'])
        else:
            skift = 'versnummer %+d' % (k0[1] - a0[1])
        w('| %d,%d-%d | %d,%d-%d | %s | %s |' % (a0[0], a0[1], a1[1], k0[0], k0[1], k1[1], skift, first))
        data['versparitet'].setdefault('blokker', []).append(
            {'wlc': '%d:%d-%d' % (a0[0], a0[1], a1[1]), 'vestlig': '%d:%d-%d' % (k0[0], k0[1], k1[1])})
    w('')
    w(kommentar.get('3.1.merking', ''))
    w('')

    # NT-noter med 2 Mos-henvisning i forskyvningssonene
    w('### 3.1.3 Hva MANTELEN NT gjør i dag i forskyvningssonene')
    w('')
    pat = re.compile(r'2\.?\s*Mos(?:ebok)?\.?\s+(\d+)[,:](\d+)')
    rows, tot, forms = [], 0, collections.Counter()
    for f in sorted(glob.glob(os.path.join(a.nt, '*.json'))):
        b = os.path.basename(f)[:-5]
        if b == 'index':
            continue
        d = json.load(open(f, encoding='utf-8'))
        for n in d.get('notes', []):
            txt = re.sub(r'<[^>]+>', ' ', n.get('html', ''))
            for m in pat.finditer(txt):
                tot += 1
                forms[':' if ':' in m.group(0) else ','] += 1
                c, v = int(m.group(1)), int(m.group(2))
                if c in (8, 22) or (c == 7 and v >= 26) or (c == 21 and v >= 37):
                    ctx = ' '.join(txt[max(0, m.start() - 60):m.end() + 70].split())
                    rows.append((BOK.get(b, (b,))[0], n.get('c'), n.get('a'), n.get('b'), m.group(0), ctx))
    w('NT-notene har %d henvisninger til 2. Mosebok (skilletegn: %s). Av disse faller %d i kapitlene som er forskjøvet:'
      % (tot, ', '.join('«%s» %d' % kv for kv in forms.most_common()), len(rows)))
    w('')
    w('| NT-note | Henvisning slik den står | Sammenheng |')
    w('|---|---|---|')
    for r in rows:
        w('| %s %s,%s-%s | `%s` | %s |' % (r[0], r[1], r[2], r[3], r[4], r[5].replace('|', '/')))
    w('')
    w(kommentar.get('3.1.ntfunn', ''))
    w('')

    # Dekalogen
    w('### 3.1.4 Dekalogen 2 Mos 20,1-17: vers, petucha (פ) og setuma (ס)')
    w('')
    w('| Vers | Ord | Avsnittsmerke etter verset | Alternativ aksentuering (OSHB-noter) | Innledning |')
    w('|---|---|---|---|---|')
    dek = []
    for v in range(1, 18):
        toks = ex[(20, v)]
        marks = [t['h'] for t in toks if t['k'] == 'seg' and t['type'] in ('x-pe', 'x-samekh')]
        inner = any(t['k'] == 'seg' and t['type'] in ('x-pe', 'x-samekh') and i < len(toks) - 1
                    and any(x['k'] == 'w' for x in toks[i + 1:]) for i, t in enumerate(toks))
        alt = sum(1 for t in toks if t['k'] == 'note' and t.get('rdg_type') == 'x-accent')
        first = ' '.join(x['h'].replace('/', '') for x in g.words(toks)[:3])
        w('| 20,%d | %d | %s%s | %d | %s |' % (v, len(g.words(toks)), ' '.join(marks) or 'ingen',
                                             ' (inne i verset)' if inner else '', alt, first))
        dek.append({'vers': v, 'merker': marks, 'alt_aksent': alt})
    data['dekalog'] = dek
    w('')
    w('### 3.1.5 Budrekkefølgen i NT (Scrivener 1894) mot WLC og LXX')
    w('')
    w('Rekkefølgen er lest maskinelt av den greske teksten ved verbstammene. '
      'F = far og mor, D = drap, E = ekteskapsbrudd, S = stjele, V = falskt vitne, B = begjære, '
      'A = «snyt ikke» (μὴ ἀποστερήσῃς), N = elske nesten.')
    w('')
    w('| Sted | Rekkefølge | MANTELEN NT (ordrett) |')
    w('|---|---|---|')
    w('| 2 Mos 20,12-17 WLC | F D E S V B | (GT, se paritetsfilen) |')
    lx = ' '.join(sw.get((20, v), '') for v in (12, 13, 14, 15, 16, 17))
    w('| 2 Mos 20,12-17 LXX (Swete) | F E S D V B | %s |' % kommentar.get('3.1.lxxbud', ''))
    order_data = {}
    grp = collections.OrderedDict()
    for ref in BUD_NT:
        bn, c, v, no, gr = ntv(ref)
        key = (bn, c)
        grp.setdefault(key, {'v': [], 'no': [], 'gr': ''})
        grp[key]['v'].append(v)
        grp[key]['no'].append(no)
        grp[key]['gr'] += ' ' + gr
    for (bn, c), d in grp.items():
        gr = d['gr'].replace('ς', 'σ')
        pos = sorted((gr.find(st), k) for k, _, st in BUD if gr.find(st) >= 0)
        seq = ' '.join(k for _, k in pos)
        ref = '%s %d,%s' % (bn, c, '-'.join(map(str, d['v'])) if len(d['v']) > 1 else d['v'][0])
        order_data[ref] = seq
        w('| %s | %s | %s |' % (ref, seq, ' '.join(d['no']).replace('|', '/')))
    data['budrekkefolge'] = order_data
    w('')
    w(kommentar.get('3.1.dekalog', ''))
    w('')

    # ---------- 3.2 ----------
    w('## 3.2 Direkte NT-sitatankre i 2. Mosebok')
    w('')
    w(kommentar.get('3.2.innledning', ''))
    w('')
    APP = ['# 2. Mosebok pre-flight: orddata for sitatankrene',
           '',
           'Vedlegg til `02_2mosebok_PREFLIGHT.md`. Én rad per ord i WLC: OSHB-ord-ID, form, Strong (OSHB-lemma), '
           'OSHB-morfologi med norsk utskrift, og STEP/TAHOT (utvidet Strong og engelsk glosse). '
           'Maskinelt uttrekk; ingen oversettelsesvalg er tatt her.', '']
    for aid, tittel, verses, ntrefs, swmap in ANKRE:
        w('### %s  %s' % (aid, tittel))
        w('')
        entry = {'id': aid, 'tittel': tittel, 'wlc': [], 'nt': []}
        w('| WLC | Hebraisk (OSHB) | STEP/TAHOT, løpende glosse | LXX (Swete) |')
        w('|---|---|---|---|')
        APP.append('## %s  %s' % (aid, tittel))
        APP.append('')
        for (c, v) in verses:
            toks = ex[(c, v)]
            heb = g.verse_text(toks)
            gl = ' '.join(' '.join(r['gloss'].replace('/', ' ').split()) for r in ta[(c, v)])
            sref = swmap.get((c, v), (c, v))
            lxx = sw.get(sref, '')
            lxxlab = '' if sref == (c, v) else ' (Swete %d,%d)' % sref
            w('| 2 Mos %s | %s | %s | %s%s |' % (fmt_ref(c, v, vm), heb, gl.replace('|', '/'), lxx, lxxlab))
            entry['wlc'].append({'ref': '%d:%d' % (c, v), 'vestlig': '%d:%d' % vm[(c, v)][:2] if (c, v) in vm else None,
                                 'hebraisk': heb, 'tahot_glosse': gl, 'lxx_swete': lxx,
                                 'ord': [{'id': x['id'], 'h': x['h'], 'strong': 'H' + x['strong'], 'morf': x['morph'],
                                          'tahot': r['strong'], 'glosse': r['gloss']}
                                         for x, r in zip(g.words(toks), ta[(c, v)])]})
            APP.append('### 2 Mos %s' % fmt_ref(c, v, vm))
            APP.append('')
            APP.append('| # | ID | Form | Strong | Morfologi | Norsk utskrift | TAHOT | Glosse |')
            APP.append('|---|---|---|---|---|---|---|---|')
            for i, (x, r) in enumerate(zip(g.words(toks), ta[(c, v)]), 1):
                APP.append('| %d | %s | %s | H%s | `%s` | %s | %s | %s |' % (
                    i, x['id'], x['h'], x['strong'], x['morph'], morf_no(x['morph']), r['strong'],
                    r['gloss'].replace('|', '/')))
            notes = [t for t in toks if t['k'] == 'note']
            if notes:
                APP.append('')
                APP.append('OSHB-noter i verset: ' + '; '.join(
                    (n.get('rdg_type') or n['type'] or 'note') + ': ' + n['text'] for n in notes))
            APP.append('')
        w('')
        w('| NT-sted | Scrivener 1894 (uten aksenter) | MANTELEN NT (ordrett) |')
        w('|---|---|---|')
        for ref in ntrefs:
            bn, c, v, no, gr = ntv(ref)
            w('| %s %d,%d | %s | %s |' % (bn, c, v, gr, no.replace('|', '/')))
            entry['nt'].append({'ref': '%s %d:%d' % (bn, c, v), 'scrivener': gr, 'mantelen_nt': no})
        w('')
        k = kommentar.get(aid)
        if k:
            w(k)
            w('')
        data['ankre'].append(entry)

    # ---------- 3.3 ----------
    w('## 3.3 Kult-, tabernakel- og paktsterminologi (EX-TERM-01 til EX-TERM-20)')
    w('')
    w(kommentar.get('3.3.innledning', ''))
    w('')
    w('| ID | Hebraisk | Strong | Treff | Vers | Kapitler (treff) | NT-gresk | Arbeidsetikett | Opphav |')
    w('|---|---|---|---|---|---|---|---|---|')
    detail = []
    for tid, heb, tr, req, etikett, gresk, opphav in TERMER:
        hits = find_term(ex, req)
        chs = collections.Counter(h[0] for h in hits)
        w('| %s | %s (%s) | %s | %d | %d | %s | %s | %s | %s |' % (
            tid, heb, tr, ' + '.join('H%04d' % r for r in req), len(hits), len({(h[0], h[1]) for h in hits}),
            ', '.join('%d (%d)' % (c, n) for c, n in sorted(chs.items())) or 'ingen', gresk, etikett, opphav))
        detail.append((tid, heb, hits))
        data['termer'].append({'id': tid, 'hebraisk': heb, 'strong': ['H%04d' % r for r in req], 'treff': len(hits),
                               'vers': sorted({'%d:%d' % (h[0], h[1]) for h in hits},
                                              key=lambda s: tuple(map(int, s.split(':'))))})
    w('')
    w('### 3.3.1 Versliste per term (WLC-adresse, vestlig i klammer der den avviker)')
    w('')
    for tid, heb, hits in detail:
        w('- **%s %s**: %s' % (tid, heb, compress([(h[0], h[1]) for h in hits], vm) or 'ingen forekomst i 2. Mosebok'))
    w('')
    # mishkan / ohel moed i samme vers
    mi = {(h[0], h[1]) for h in find_term(ex, [4908])}
    om = {(h[0], h[1]) for h in find_term(ex, [168, 4150])}
    oh = collections.Counter((h[0], h[1]) for h in find_term(ex, [168]))
    both = sorted(mi & om)
    w('### 3.3.2 Kontrollpunkt TK-22: מִשְׁכָּן og אֹהֶל מוֹעֵד')
    w('')
    w('- מִשְׁכָּן står i %d vers, אֹהֶל מוֹעֵד i %d vers. Begge står i samme vers %d steder: %s.' % (
        len(mi), len(om), len(both), compress(both, vm)))
    ohel_alone = sorted(k for k in oh if k not in om)
    w('- אֹהֶל uten מוֹעֵד (innen tre ord) står i %d vers: %s.' % (len(ohel_alone), compress(ohel_alone, vm)))
    forms = collections.Counter(h[3] for h in find_term(ex, [4908, 168], window=2))
    w('- Sammensetningen מִשְׁכַּן אֹהֶל מוֹעֵד («sammenkomstteltets bolig») og nærstilling av de to ordene: %s.' % (
        '; '.join('%s (%d)' % kv for kv in forms.most_common()) or 'ingen'))
    w('')
    w(kommentar.get('3.3.tk22', ''))
    w('')
    # parokhet / masakh former
    for label, req in (('פָּרֹכֶת (EX-TERM-11)', [6532]), ('מָסָךְ (EX-TERM-12)', [4539])):
        hits = find_term(ex, req)
        ctx = collections.Counter()
        for c, v, i, _ in hits:
            ws = g.words(ex[(c, v)])
            ctx[' '.join(x['h'].replace('/', '') for x in ws[i:i + 3])] += 1
        w('- %s, de vanligste ordgruppene: %s.' % (label, '; '.join('%s (%d)' % kv for kv in ctx.most_common(6))))
    w('')
    for label, req in (('פָּרֹכֶת הַמָּסָךְ (begge ord i ett uttrykk)', [6532, 4539]),
                       ('מִזְבַּח הַזָּהָב (gullalteret)', [4196, 2091]),
                       ('מִזְבַּח הַנְּחֹשֶׁת (bronsealteret)', [4196, 5178])):
        hits = find_term(ex, req, window=2)
        w('- %s: %d treff: %s.' % (label, len(hits), compress([(h[0], h[1]) for h in hits], vm) or 'ingen'))
    w('')
    w(kommentar.get('3.3.avslutning', ''))
    w('')
    w(kommentar.get('slutt', ''))

    os.makedirs(os.path.dirname(os.path.abspath(a.out_json)), exist_ok=True)
    open(a.out_md, 'w', encoding='utf-8').write('\n'.join(L).rstrip() + '\n')
    open(a.out_app, 'w', encoding='utf-8').write('\n'.join(APP).rstrip() + '\n')
    json.dump(data, open(a.out_json, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('skrevet', a.out_md, len(L), 'linjer;', a.out_app, len(APP), 'linjer')


if __name__ == '__main__':
    main()
