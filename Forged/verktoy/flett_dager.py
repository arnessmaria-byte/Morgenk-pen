#!/usr/bin/env python3
"""Fletter omskrevne dager inn i kildefilene manus/01-03.

Bruk (fra Forged/bok): python3 ../verktoy/flett_dager.py MAPPE
MAPPE har day-01.md til day-40.md, hver fra «## Day N:» til «*End of Day N*».
Dager som mangler i mappen blir stående som de er.
"""
import pathlib, re, sys
mappe = pathlib.Path(sys.argv[1])
filer = [pathlib.Path("manus") / f for f in ("01-front-intro-phase1.md", "02-phase2-phase3.md", "03-phase4-phase5.md")]
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
for f, t in tekster.items():
    f.write_text(t, encoding="utf-8")
print("flettet inn:", byttet)
