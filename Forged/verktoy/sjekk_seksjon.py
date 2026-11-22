#!/usr/bin/env python3
"""Kontroll av en omskrevet innledning eller et vedlegg mot originalen (mesterordren 22.11.2026).

Bruk: python3 sjekk_seksjon.py ORIGINAL.md NY.md --ledige L --brukt B
Exit 0 = alle sperrer består. Linjetallet er et anslag; den bygde PDF-en avgjør.
"""
import argparse, math, re, sys

FASTE = ["You are not beyond repair.",
         "If you might hurt yourself or someone else, get emergency help now.",
         "This book was written to form you.",
         "Healing Forge is part of the training and no detour from it.",
         "You are not measured by momentum. You are formed by faithfulness.",
         "Young men rarely fail because they think their faith is wrong. They fail because they have not trained it.",
         "you end up better organized on the outside and still not whole inside."]

def linjer(tekst):
    n = 0
    for para in [p for p in re.split(r"\n\s*\n", tekst) if p.strip()]:
        rader = [l for l in para.split("\n") if l.strip()]
        if not rader or rader[0].startswith(("#", "|", ">")):
            n += 2 if rader and rader[0].startswith("#") else 0
            continue
        if all(r.startswith("- ") for r in rader):
            n += sum(math.ceil(len(re.sub(r"\*", "", r[2:])) / 52) for r in rader)
        else:
            n += math.ceil(len(re.sub(r"\*", "", " ".join(rader))) / 63)
    return n

ap = argparse.ArgumentParser()
ap.add_argument("orig"); ap.add_argument("ny")
ap.add_argument("--ledige", type=int, required=True); ap.add_argument("--brukt", type=int, required=True)
a = ap.parse_args()
o, n = open(a.orig, encoding="utf-8").read().strip(), open(a.ny, encoding="utf-8").read().strip()
feil = []
def sjekk(ok, tekst):
    print(("  OK   " if ok else "  FEIL ") + tekst)
    if not ok:
        feil.append(tekst)
sjekk(o.split("\n")[0] == n.split("\n")[0], "overskriften er uendret")
for f in FASTE:
    if f in o:
        sjekk(f in n, f"fast setning står: «{f[:50]}»")
sjekk(not any(c in n for c in (chr(0x2014), chr(0x2015))), "ingen lange tankestreker")
sjekk(not re.search(" " + chr(0x2013) + " ", n) and not re.search(r"[A-Za-z]" + chr(0x2013) + r"[A-Za-z]", n), "ingen korte tankestreker i prosa")
prosa = "\n".join(l for l in n.split("\n") if not l.startswith(">"))
sjekk(not any(c in prosa for c in "“”’‘"), "rette anførselstegn og apostrofer i prosaen")
sjekk(len(re.findall(r"fits? together", n, re.I)) <= 1, "«fit together» høyst én gang")
d = linjer(n) - linjer(o)
sjekk(d <= a.ledige - 1, f"anslått endring {d:+d} linjer, høyst {a.ledige - 1:+d}")
sjekk(d >= -(a.brukt - 4), f"anslått endring {d:+d} linjer, minst {-(a.brukt - 4):+d}")
print("RESULTAT:", "består" if not feil else f"{len(feil)} feil")
sys.exit(1 if feil else 0)
