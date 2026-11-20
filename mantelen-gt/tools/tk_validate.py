#!/usr/bin/env python3
"""Låskontroll for MANTELEN GT og MANTELEN NT mot termregistre (KR og TK).

Leser leserdata i prosjektets format (én JSON per bok):
  {"id": "gt-exo", "chapters": [{"n": 1, "v": [{"n": 1, "t": "<norsk>", "w": [{"s": "H1697G" | 3056, ...}]}]}]}

og ett eller flere registre i formatet til tk_concordance.json. Samme motor brukes for
KR-registeret når det finnes som fil (kr_register.json i samme format, med id-er KR-..).

Bruk:
  tk_validate.py check   --register tk_concordance.json [--register kr_register.json] BOK.json [...]
  tk_validate.py observe --strong H3727 [--strong G2435] BOK.json [...]

`check` skriver en rapport og gir returkode:
  0  alle håndhevede låser består
  1  minst ett låsbrudd i en VEDTATT oppføring
  2  registeret er ikke klart for bokgodkjenning (oppføringer uten kilde eller uten vedtak),
     eller et påkrevd register mangler

Skriptet leser bare. Det endrer aldri bibelfiler.
"""
import argparse
import json
import re
import sys

HANDHEVES = {'VEDTATT'}
IKKE_KLAR = {'MANGLER_KILDE', 'UBEKREFTET'}


def norm_strong(s):
    """'H1697G' -> 'H1697'; 3056 -> 'G3056'; 'G0846' -> 'G846'; 'H0430G' -> 'H430'."""
    if isinstance(s, int):
        return 'G%d' % s
    m = re.match(r'^([HG])0*(\d+)', str(s).strip())
    if m:
        return m.group(1) + m.group(2)
    m = re.match(r'^0*(\d+)$', str(s).strip())
    return ('G' + m.group(1)) if m else str(s)


def load_book(path):
    with open(path, encoding='utf-8') as f:
        d = json.load(f)
    verses = []
    for ch in d.get('chapters', []):
        for v in ch.get('v', []):
            strongs = []
            for w in v.get('w', []):
                for key in ('sx', 's', 'lemma'):
                    if key in w and w[key] not in (None, ''):
                        val = w[key]
                        if key == 'lemma':
                            val = 'H' + str(val)
                        strongs.append(norm_strong(val))
                        break
            verses.append((int(ch['n']), int(v['n']), v.get('t', ''), strongs))
    return d.get('id', path), d.get('abbrev', d.get('id', path)), verses


def seq_in(strongs, req, window=3):
    """Finnes Strong-sekvensen req i rekkefølge innen vinduet?"""
    for i, s in enumerate(strongs):
        if s != req[0]:
            continue
        j, ok = i, True
        for r in req[1:]:
            nxt = [k for k in range(j + 1, min(len(strongs), j + 1 + window)) if strongs[k] == r]
            if not nxt:
                ok = False
                break
            j = nxt[0]
        if ok:
            return True
    return False


def side_hits(entry_side, verses):
    """Vers der oppføringens kildeord står. entry_side: {'strong': [...], 'sekvens': bool}"""
    req = [norm_strong(s) for s in entry_side.get('strong', [])]
    if not req:
        return []
    out = []
    for c, v, t, strongs in verses:
        if entry_side.get('sekvens'):
            hit = seq_in(strongs, req)
        else:
            hit = any(r in strongs for r in req)
        if hit:
            out.append((c, v, t))
    return out


def check(registers, books, out=sys.stdout):
    brudd = 0
    ikke_klar = []
    varsler = 0
    loaded = [load_book(b) for b in books]
    for reg_path in registers:
        try:
            reg = json.load(open(reg_path, encoding='utf-8'))
        except FileNotFoundError:
            print('REGISTER MANGLER: %s' % reg_path, file=out)
            ikke_klar.append(reg_path)
            continue
        print('== Register %s (%s), status %s' % (reg.get('register', reg_path), reg_path, reg.get('status')), file=out)
        if reg.get('status') not in HANDHEVES:
            ikke_klar.append('%s: registerstatus %s' % (reg_path, reg.get('status')))
        for e in reg.get('oppforinger', []):
            st = e.get('status')
            if st in IKKE_KLAR:
                ikke_klar.append('%s %s' % (e['id'], st))
            if st == 'MANGLER_KILDE':
                continue
            for side, key in (('GT', 'hebraisk'), ('NT', 'gresk')):
                src = e.get(key) or {}
                term = (e.get('laast_term') or {}).get(side)
                if not src.get('strong') or not term or not term.get('regex'):
                    continue
                rx = re.compile(term['regex'], re.I)
                unntak = set(term.get('unntak', []))
                for bid, abbrev, verses in loaded:
                    is_gt = str(bid).startswith('gt-')
                    if (side == 'GT') != is_gt:
                        continue
                    for c, v, t in side_hits(src, verses):
                        ref = '%s %d,%d' % (abbrev, c, v)
                        if ref in unntak or rx.search(t):
                            continue
                        if st in HANDHEVES:
                            brudd += 1
                            print('LÅSBRUDD %s %s: forventet /%s/ : %s' % (e['id'], ref, term['regex'], t), file=out)
                        else:
                            varsler += 1
                            print('VARSEL   %s %s (%s): mangler /%s/ : %s' % (e['id'], ref, st, term['regex'], t), file=out)
    print('-- %d låsbrudd, %d varsler, %d forhold som hindrer bokgodkjenning' % (brudd, varsler, len(ikke_klar)), file=out)
    for x in ikke_klar:
        print('   IKKE KLAR: %s' % x, file=out)
    if brudd:
        return 1
    if ikke_klar:
        return 2
    return 0


def observe(strongs, books, out=sys.stdout):
    req = {norm_strong(s) for s in strongs}
    n = 0
    for b in books:
        bid, abbrev, verses = load_book(b)
        for c, v, t, ss in verses:
            if req & set(ss):
                n += 1
                print('%s %d,%d\t%s' % (abbrev, c, v, t), file=out)
    print('-- %d vers' % n, file=out)
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    c = sub.add_parser('check')
    c.add_argument('--register', action='append', required=True)
    c.add_argument('books', nargs='+')
    o = sub.add_parser('observe')
    o.add_argument('--strong', action='append', required=True)
    o.add_argument('books', nargs='+')
    a = ap.parse_args()
    if a.cmd == 'check':
        sys.exit(check(a.register, a.books))
    sys.exit(observe(a.strong, a.books))


if __name__ == '__main__':
    main()
