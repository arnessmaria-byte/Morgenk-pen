#!/usr/bin/env python3
"""Kontrollerer bibelsitater i en tekst mot den kontrollerte versteksten.

Bruk: python3 sjekk_sitater.py FIL [FIL ...]
Finner sitater i rette eller krøllete anførselstegn som står like foran en
henvisning i parentes, for eksempel: "Scripture cannot be broken" (John 10:35).
Sitatet må stå ordrett i verset (oversettelsen står i parentesen, ESV er standard).
Epigrafene (linjer som begynner med «>») hoppes over.
Exit 1 hvis et sitat ikke stemmer. Henvisninger uten kontrollert tekst meldes som merknad.
"""
import json, pathlib, re, sys

V = json.loads((pathlib.Path(__file__).resolve().parent.parent / "bok/kilder/m22/vers_kontrollert.json").read_text())
def norm(s):
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = re.sub(r"[\"']", "", s)
    return re.sub(r"\s+", " ", s).strip().lower().rstrip(".,;:!?")

def finn_vers(ref, ver):
    m = re.match(r"(.+?)\s+(\d+):(\d+)", ref)
    if not m:
        return None
    bok, kap, v = m.group(1), int(m.group(2)), int(m.group(3))
    for k, tekst in V.items():
        km = re.match(r"(.+?)\s+(\d+):(\d+)(?:-(\d+))?\s+\((\w+)\)", k)
        if km and km.group(1) == bok and int(km.group(2)) == kap and km.group(5) == ver:
            a = int(km.group(3)); b = int(km.group(4) or a)
            if a <= v <= b:
                return tekst
    return None

feil, merk = [], []
for fil in sys.argv[1:]:
    t = pathlib.Path(fil).read_text(encoding="utf-8")
    t = "\n".join(l for l in t.split("\n") if not l.startswith(">"))
    for m in re.finditer(r"[\"“]([^\"“”]{3,400}?)[\"”]\s*\(([^()]*?\d+:\d+[^()]*)\)", t):
        sitat, ref = m.group(1), m.group(2)
        ver = "NKJV" if "NKJV" in ref else "ESV"
        første = re.split(r";", ref)[0].replace(", NKJV", "").replace(" NKJV", "").strip()
        vers = finn_vers(første, ver)
        if vers is None:
            merk.append(f"{fil}: «{sitat[:50]}» ({ref}) har ingen kontrollert tekst")
            continue
        biter = [b for b in re.split(r"\s*(?:\.\.\.|…)\s*", sitat) if b.strip()]
        if not all(norm(b) in norm(vers) for b in biter):
            feil.append(f"{fil}: «{sitat[:60]}» står ikke ordrett i {første} ({ver})")
for x in merk:
    print("  MERK", x)
for x in feil:
    print("  FEIL", x)
print("RESULTAT:", "alle kontrollerbare sitater stemmer" if not feil else f"{len(feil)} sitat(er) stemmer ikke")
sys.exit(1 if feil else 0)
