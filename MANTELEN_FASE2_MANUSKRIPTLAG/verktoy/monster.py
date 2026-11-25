#!/usr/bin/env python3
"""Felles hjelpefunksjoner for Trinn 0: normalisering, beleggsoek og maskinelt vitnemoenster.

Brukes baade av byggeskriptet og av validatoren, slik at vitnemoensteret (akse 1) kan
regnes ut paa nytt fra pilotfilen og registrene og sammenlignes med det som er lagret.
"""
import re
import unicodedata

EARLY_CUTOFF = 500  # foerstehender med INTF-datering (origLate) foer dette aaret regnes som tidlige


def strip_marks(s):
    s = unicodedata.normalize('NFD', s)
    return ''.join(c for c in s if not unicodedata.combining(c))


def gnorm(s):
    """Gresk: uten aksenter og tegn, smaa bokstaver, lik sigma."""
    s = strip_marks(s or '').lower().replace('ς', 'σ')
    return re.sub(r'\s+', ' ', re.sub(r'[^α-ω ]', ' ', s)).strip()


def hnorm(s):
    """Hebraisk: bare konsonanter og ordskiller."""
    s = strip_marks(s or '').replace('־', ' ')
    return re.sub(r'\s+', ' ', re.sub(r'[^א-ת ]', '', s)).strip()


def flagged(text, lang, with_pos=False):
    """Gjoer en transkripsjon om til ren tekst pluss merke per tegn.

    Merker: 'r' = rekonstruert (hakeparentes), 'u' = usikker (parentes eller ?), '' = lest.
    Med with_pos foelger ogsaa plassen til hvert tegn i den opprinnelige (NFD) teksten.
    """
    src = unicodedata.normalize('NFD', text or '')
    plain, flags, pos, state = [], [], [], ''
    for i, ch in enumerate(src):
        if ch == '[':
            state = 'r'; continue
        if ch == ']':
            state = ''; continue
        if ch == '(':
            state = 'u'; continue
        if ch == ')':
            state = ''; continue
        if ch == '?':
            if flags: flags[-1] = flags[-1] or 'u'
            continue
        if unicodedata.combining(ch) or ch in '‾׳·,.;:’\'':
            continue
        ch = ch.lower().replace('ς', 'σ')
        ok = ('α' <= ch <= 'ω') if lang == 'grc' else ('א' <= ch <= 'ת')
        if ok:
            plain.append(ch); flags.append(state); pos.append(i)
        elif ch.isspace() or ch in '…ε':
            if plain and plain[-1] != ' ':
                plain.append(' '); flags.append(state); pos.append(i)
    while plain and plain[-1] == ' ':
        plain.pop(); flags.pop(); pos.pop()
    if with_pos:
        return ''.join(plain), flags, pos, src
    return ''.join(plain), flags


def attest(text, lang, pattern, nospace=True):
    """Soeker etter lesningen i en transkripsjon.

    Gir (utdrag slik transkripsjonen har det, sikkerhet) eller (None, None). Med nospace
    sammenlignes bokstavrekken uten ordskiller, fordi linjeskift i haandskriftet deler ord i
    transkripsjonen. Moensteret skrives da uten mellomrom.
    """
    plain, flags, pos, src = flagged(text, lang, with_pos=True)
    if nospace:
        keep = [i for i, c in enumerate(plain) if c != ' ']
        plain, flags, pos = ''.join(plain[i] for i in keep), [flags[i] for i in keep], [pos[i] for i in keep]
    m = re.search(pattern, plain)
    if not m or m.end() == m.start():
        return None, None
    span = [f for f, c in zip(flags[m.start():m.end()], plain[m.start():m.end()]) if c != ' ']
    if span and all(f == 'r' for f in span):
        cert = 'rekonstruert'
    elif any(f == 'r' for f in span):
        cert = 'delvis rekonstruert'
    elif any(f == 'u' for f in span):
        cert = 'usikre bokstaver'
    else:
        cert = 'lest'
    i, j = pos[m.start()], pos[m.end() - 1] + 1
    while i > 0 and not src[i - 1].isspace(): i -= 1
    while j < len(src) and not src[j].isspace(): j += 1
    return unicodedata.normalize('NFC', src[i:j]), cert


def edge_certainty(text, lang, tail=True, n=10):
    """Sikkerheten i slutten (tail) eller begynnelsen av et vers. Brukes ved utelatelser."""
    plain, flags = flagged(text, lang)
    pairs = [(c, f) for c, f in zip(plain, flags) if c != ' ']
    seg = pairs[-n:] if tail else pairs[:n]
    if not seg:
        return 'mangler'
    if all(f == 'r' for _, f in seg):
        return 'rekonstruert'
    if any(f == 'r' for _, f in seg):
        return 'delvis rekonstruert'
    return 'usikre bokstaver' if any(f == 'u' for _, f in seg) else 'lest'


def reading_groups(unit):
    """Lesninger som bare er ortografiske eller formmessige utgaver av samme lesning, regnes sammen."""
    root = {}
    for r in unit['readings']:
        root[r['readingId']] = r.get('agreesWith') or r['readingId']
    for k in list(root):
        while root[k] in root and root[root[k]] != root[k]:
            root[k] = root[root[k]]
    return root


def gt_pattern(unit, register):
    """Akse 1 for GT: hvilke tradisjoner (M, Q, G, SP) som gaar sammen. Ren utregning fra dataene."""
    root = reading_groups(unit)
    by = {}
    for r in unit['readings']:
        g = by.setdefault(root[r['readingId']], {'M': [], 'Q': [], 'G': [], 'SP': [], 'andre': []})
        for w in r.get('manuscriptWitnesses', []) + r.get('versionWitnesses', []):
            if w['verification']['status'] == 'IKKE_AVLEST' or w.get('certainty') == 'rekonstruert':
                continue
            t = register['witnesses'][w['siglum']].get('tradition')
            g[t if t in g else 'andre'].append(w['siglum'])
    where = {t: sorted(k for k, g in by.items() if g[t]) for t in ('M', 'Q', 'G', 'SP')}
    m, q, gg = where['M'], where['Q'], where['G']
    if not q:
        code = 'G ≠ M' if gg and gg != m else 'ingen Qumran-vitner'
    elif len(q) > 1:
        code = 'Q delt'
    elif gg == q and q != m:
        code = 'Q = G ≠ M'
    elif m == q and gg and gg != m:
        code = 'Q = M ≠ G'
    elif gg and gg != q and gg != m and q != m:
        code = 'Q ≠ G ≠ M'
    elif q != m and not gg:
        code = 'Q alene'
    else:
        code = 'Q = M'
    return {'computed': True, 'scheme': 'GT (plan 2.3, akse 1)', 'code': code,
            'traditionsByReading': {k: {t: v for t, v in g.items() if v} for k, g in by.items()},
            'rule': 'Bare vitner som er bekreftet mot belegg, teller, og ikke steder som er helt rekonstruert. Lesninger merket agreesWith regnes sammen med lesningen de viser til.'}


def nt_pattern(unit, register):
    """Akse 1 for NT: forholdet mellom TR, den bysantinske utgaven og de tidlige greske foerstehendene."""
    root = reading_groups(unit)
    tr = byz = None
    early, later, corr, fathers_in, fathers_out, versions = {}, {}, {}, {}, {}, {}
    for r in unit['readings']:
        g = root[r['readingId']]
        for e in r.get('editionSupport', []):
            if e['edition'] in ('R10', 'SCR1894'): tr = g
            if e['edition'] == 'RP2018': byz = g
        for w in r.get('manuscriptWitnesses', []):
            if w['verification']['status'] == 'IKKE_AVLEST' or w.get('certainty') == 'rekonstruert':
                continue
            reg = register['witnesses'][w['siglum']]
            late = (reg.get('dateRange') or {}).get('notAfter')
            first = w.get('hand') in (None, '*')
            if not first:
                corr.setdefault(g, []).append(w['siglum'] + w['hand'])
            elif late is not None and late < EARLY_CUTOFF:
                early.setdefault(g, []).append(w['siglum'])
            else:
                later.setdefault(g, []).append(w['siglum'])
        for w in r.get('patristicWitnesses', []):
            if w['verification']['status'] == 'IKKE_AVLEST':
                continue
            inside = register['witnesses'][w['siglum']].get('window') == 'hovedvindu'
            (fathers_in if inside else fathers_out).setdefault(g, []).append(w['siglum'] + ' ' + w['locator'])
        for w in r.get('versionWitnesses', []):
            if w['verification']['status'] != 'IKKE_AVLEST':
                versions.setdefault(g, []).append(w['siglum'])
    rel = 'TR = Byz' if tr == byz else 'TR ≠ Byz'
    if not early:
        tail = 'ingen tidlige førstehender bekreftet'
    elif len(early) > 1:
        tail = 'tidlige førstehender delt (' + '; '.join('%s: %s' % (k, ', '.join(v)) for k, v in sorted(early.items())) + ')'
    else:
        k = next(iter(early))
        if k == tr and k == byz: tail = 'tidlige førstehender = TR = Byz'
        elif k == byz: tail = 'Byz = tidlige førstehender'
        elif k == tr: tail = 'TR = tidlige førstehender'
        else: tail = 'tidlige førstehender har lesning %s mot TR og Byz' % k
    return {'computed': True, 'scheme': 'NT (strømmene i plan 3.1)', 'code': rel + '; ' + tail,
            'trReading': tr, 'byzReading': byz, 'earlyCutoffYear': EARLY_CUTOFF,
            'earlyFirstHands': early, 'laterFirstHands': later, 'correctors': corr,
            'fathersMainWindow': fathers_in, 'fathersOutsideWindow': fathers_out, 'versions': versions,
            'rule': 'Tidlig = første hånd i gresk håndskrift med INTF-datering som slutter før år %d. Bare vitner bekreftet mot belegg teller, og ikke steder som er helt rekonstruert. Antall er ikke vekt.' % EARLY_CUTOFF}


def pattern(unit, register):
    return gt_pattern(unit, register) if unit['anchor']['testament'] == 'GT' else nt_pattern(unit, register)


def computed_kind(unit):
    """Mekanisk grovsortering av variantarten (akse 2). Den faglige arten staar i variantKind.assigned."""
    lang = unit['readings'][0]['lang']
    norm = gnorm if lang == 'grc' else hnorm
    toks = [norm(r['text']).split() for r in unit['readings'] if r['lang'] == lang]
    if any(not t for t in toks):
        return 'pluss_minus'
    a = toks[0]
    kinds = set()
    for b in toks[1:]:
        if sorted(a) == sorted(b) and a != b:
            kinds.add('ordfølge')
        elif len(a) != len(b) and (set(a) <= set(b) or set(b) <= set(a)):
            kinds.add('pluss_minus')
        elif len(a) == len(b):
            kinds.add('leksikalsk_eller_morfologisk')
        else:
            kinds.add('pluss_minus_og_annet_ord')
    return '+'.join(sorted(kinds)) or 'lik'
