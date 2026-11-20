"""Kildelesere for MANTELEN GT pre-flight og tverrkorpuskontroll.

Leser offentlige grunntekstkilder (ingen av dem ligger i dette repoet):
  - OSHB / WLC (openscriptures/morphhb, wlc/<Bok>.xml)      CC BY 4.0
  - OSHB VerseMap.xml (WLC mot KJV-versifikasjon)
  - STEP Bible TAHOT (Translators Amalgamated Hebrew OT)     CC BY 4.0
  - Scrivener 1894 (byztxt/greektext-scrivener, textonly)    Public Domain
  - Swete LXX (nathans/lxx-swete, data/*.txt)                CC BY-SA 4.0
  - MANTELEN NT leserdata (<bokid>.json fra mantelen.no)

Bare standardbiblioteket brukes.
"""
import collections
import json
import re
import xml.etree.ElementTree as ET

OSIS = '{http://www.bibletechnologies.net/2003/OSIS/namespace}'
VMAP = '{http://www.APTBibleTools.com/namespace}'


def lemma_strong(lemma):
    """'c/1696' -> ('1696', ['c']); '1254 a' -> ('1254a', [])."""
    parts = lemma.split('/')
    main = re.sub(r'[^0-9a-z]', '', parts[-1].lower())
    return main, parts[:-1]


def strong_num(s):
    """'1254a' -> 1254"""
    m = re.match(r'(\d+)', s)
    return int(m.group(1)) if m else None


def parse_oshb(path):
    """Returnerer OrderedDict[(kap, vers)] -> liste av token-dicter.

    token: {'k': 'w', 'h': hebraisk med morfemskille '/', 'lemma': rå, 'strong': '1696',
            'pre': ['c'], 'morph': 'HC/Vpw3ms', 'id': ...}
           {'k': 'seg', 'type': 'x-pe' | 'x-samekh' | 'x-maqqef' | 'x-sof-pasuq' | 'x-paseq', 'h': tegn}
           {'k': 'note', 'type': 'variant' | 'alternative' | '', 'text': ...}
    """
    root = ET.parse(path).getroot()
    verses = collections.OrderedDict()
    for v in root.iter(OSIS + 'verse'):
        _, c, n = v.get('osisID').split('.')
        toks = []
        for el in v:
            tag = el.tag.replace(OSIS, '')
            if tag == 'w':
                s, pre = lemma_strong(el.get('lemma', ''))
                toks.append({'k': 'w', 'h': ''.join(el.itertext()), 'lemma': el.get('lemma', ''),
                             'strong': s, 'pre': pre, 'morph': el.get('morph', ''), 'id': el.get('id', '')})
            elif tag == 'seg':
                toks.append({'k': 'seg', 'type': el.get('type', ''), 'h': ''.join(el.itertext())})
            elif tag == 'note':
                d = {'k': 'note', 'type': el.get('type', ''), 'text': ' '.join(''.join(el.itertext()).split())}
                rdg = el.find(OSIS + 'rdg')
                if rdg is not None:
                    d['rdg_type'] = rdg.get('type', '')
                    d['rdg'] = ' '.join(''.join(rdg.itertext()).split())
                cw = el.find(OSIS + 'catchWord')
                if cw is not None:
                    d['catch'] = ''.join(cw.itertext())
                toks.append(d)
        verses[(int(c), int(n))] = toks
    return verses


def verse_text(toks, keep_marks=True):
    """Sammenhengende hebraisk verstekst (uten morfemskille)."""
    out = []
    for t in toks:
        if t['k'] == 'w':
            out.append(t['h'].replace('/', ''))
            out.append(' ')
        elif t['k'] == 'seg':
            if t['type'] == 'x-maqqef':
                if out and out[-1] == ' ':
                    out.pop()
                out.append('־')
            elif t['type'] == 'x-sof-pasuq':
                if out and out[-1] == ' ':
                    out.pop()
                out.append('׃ ')
            elif t['type'] == 'x-paseq':
                out.append('׀ ')
            elif keep_marks and t['type'] in ('x-pe', 'x-samekh'):
                out.append(t['h'] + ' ')
    return ''.join(out).strip()


def words(toks):
    return [t for t in toks if t['k'] == 'w']


def parse_versemap(path, book):
    """WLC->KJV for én bok: dict[(kap, vers)] -> (kap, vers, type)."""
    root = ET.parse(path).getroot()
    out = collections.OrderedDict()
    for b in root.iter(VMAP + 'book'):
        if b.get('osisID') != book:
            continue
        for v in b.iter(VMAP + 'verse'):
            _, c, n = v.get('wlc').split('.')
            _, kc, kn = v.get('kjv').split('.')
            out[(int(c), int(n))] = (int(kc), int(kn), v.get('type'))
    return out


TAHOT_REF = re.compile(r'^([1-3A-Za-z]+)\.(\d+)\.(\d+)(?:\((?:(\d+)\.)?(\d+)\))?#(\d+)=(.+)$')


def parse_tahot(path, book):
    """dict[(heb_kap, heb_vers)] -> liste av rader (ordnet), pluss eng-ref.

    rad: {'n': ordnr, 'type': 'L' ..., 'h': hebraisk, 'tr': translit, 'gloss': engelsk,
          'dstrong': rå, 'strong': 'H1696', 'gram': ..., 'eng': (kap, vers)}
    """
    out = collections.OrderedDict()
    pref = book + '.'
    with open(path, encoding='utf-8-sig') as f:
        for line in f:
            if not line.startswith(pref):
                continue
            cols = line.rstrip('\n').split('\t')
            m = TAHOT_REF.match(cols[0])
            if not m:
                continue
            ec, ev = int(m.group(2)), int(m.group(3))
            if m.group(5):
                hc = int(m.group(4)) if m.group(4) else ec
                hv = int(m.group(5))
            else:
                hc, hv = ec, ev
            ms = re.findall(r'\{(H\d+[A-Za-z]?)\}', cols[4] if len(cols) > 4 else '')
            out.setdefault((hc, hv), []).append({
                'n': int(m.group(6)), 'type': m.group(7), 'h': cols[1] if len(cols) > 1 else '',
                'tr': cols[2] if len(cols) > 2 else '', 'gloss': cols[3] if len(cols) > 3 else '',
                'dstrong': cols[4] if len(cols) > 4 else '', 'strong': ms[0] if ms else '',
                'gram': cols[5] if len(cols) > 5 else '', 'eng': (ec, ev)})
    return out


_SCV = dict(zip('abgdezhyiklmnxoprsvtufcqw', 'αβγδεζηθικλμνξοπρσςτυφχψω'))


def scv_to_greek(s):
    return ''.join(_SCV.get(ch, ch) for ch in s)


def parse_scrivener(path):
    """dict[(kap, vers)] -> uaksentuert gresk (Scrivener 1894, Robinsons translitterasjon omsatt)."""
    out = collections.OrderedDict()
    cur = None
    with open(path, encoding='latin-1') as f:
        for line in f:
            line = re.sub(r'\[[^\]]*\]', ' ', line)
            m = re.match(r'\s*(\d+):(\d+)\s*(.*)$', line)
            if m:
                cur = (int(m.group(1)), int(m.group(2)))
                out[cur] = m.group(3).strip()
            elif cur is not None and line.strip():
                out[cur] = (out[cur] + ' ' + line.strip()).strip()
    return collections.OrderedDict((k, scv_to_greek(' '.join(v.split()))) for k, v in out.items())


def parse_swete(path):
    """dict[(kap, vers)] -> gresk LXX-tekst (Swete). Versnummerering følger Swete."""
    out = collections.OrderedDict()
    with open(path, encoding='utf-8') as f:
        for line in f:
            ref, _, w = line.rstrip('\n').partition(' ')
            p = ref.split('.')
            if len(p) < 3 or not w:
                continue
            try:
                key = (int(p[1]), int(p[2]))
            except ValueError:
                key = (p[1], p[2])
            out.setdefault(key, []).append(w)
    return collections.OrderedDict((k, ' '.join(v)) for k, v in out.items())


def load_nt_book(path):
    """MANTELEN NT leserdata -> dict[(kap, vers)] -> {'t': norsk, 'g': gresk, 'w': ordliste}."""
    with open(path, encoding='utf-8') as f:
        d = json.load(f)
    out = {}
    for ch in d.get('chapters', []):
        for v in ch.get('v', []):
            out[(int(ch['n']), int(v['n']))] = {
                't': v.get('t', ''), 'g': ' '.join(w.get('g', '') for w in v.get('w', [])), 'w': v.get('w', [])}
    return out, {k: d.get(k) for k in ('id', 'title', 'abbrev', 'status', 'source', 'sourceHash') if k in d}
