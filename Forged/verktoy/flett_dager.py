#!/usr/bin/env python3
"""Fletter omskrevne dager inn i kildefilene manus/01-03.

Bruk (fra Forged/bok): python3 ../verktoy/flett_dager.py MAPPE [--seksjon FIL ...]
MAPPE har day-01.md til day-40.md, hver fra «## Day N:» til «*End of Day N*».
Dager som mangler i mappen blir stående som de er.
En seksjonsfil begynner med sin toppoverskrift («# Introduction», «# Appendix B: ...»)
og erstatter alt fram til neste toppoverskrift (i manus/01-04).
"""
import pathlib, re, sys
import argparse
ap = argparse.ArgumentParser(); ap.add_argument("mappe"); ap.add_argument("--seksjon", action="append", default=[])
a = ap.parse_args()
mappe = pathlib.Path(a.mappe)
filer = [pathlib.Path("manus") / f for f in ("01-front-intro-phase1.md", "02-phase2-phase3.md", "03-phase4-phase5.md", "04-back.md")]
tekster = {f: f.read_text(encoding="utf-8") for f in filer}
byttet = []
for n in range(1, 41):
    ny = mappe / f"day-{n:02d}.md"
    if not ny.exists():
        continue
    blokk = ny.read_text(encoding="utf-8").strip()
    assert blokk.startswith(f"## Day {n}:") and blokk.endswith(f"*End of Day {n}*"), f"Day {n}: feil start eller slutt"
    mønster = re.compile(r"^## Day %d:.*?^\*End of Day %d\*$" % (n, n), re.M | re.S)
    treff = [f for f, t in tekster.items() if mønster.search(t)]
    assert len(treff) == 1, f"Day {n}: fant {len(treff)} steder"
    tekster[treff[0]] = mønster.sub(lambda m: blokk, tekster[treff[0]], count=1)
    byttet.append(n)
for s in a.seksjon:
    blokk = pathlib.Path(s).read_text(encoding="utf-8").strip()
    hode = blokk.split("\n")[0]
    assert hode.startswith("# "), f"{s}: må begynne med en toppoverskrift"
    mønster = re.compile(r"^" + re.escape(hode) + r"\n.*?(?=^# |\Z)", re.M | re.S)
    treff = [f for f, t in tekster.items() if mønster.search(t)]
    assert len(treff) == 1, f"{hode}: fant {len(treff)} steder"
    tekster[treff[0]] = mønster.sub(lambda m: blokk + "\n\n", tekster[treff[0]], count=1)
    byttet.append(hode[2:])
for f, t in tekster.items():
    f.write_text(t.rstrip() + "\n" if f.name == "04-back.md" else t, encoding="utf-8")
print("flettet inn:", byttet)
