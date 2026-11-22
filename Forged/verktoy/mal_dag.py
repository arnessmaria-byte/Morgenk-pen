#!/usr/bin/env python3
"""Måler dager og seksjoner i ekte 5 x 8-sats (mesterordren 22.11.2026).

Bruk: python3 mal_dag.py [--grunnlag MAPPE] [--seksjon FIL ...] [DAGFIL ...]

DAGFIL er day-NN.md (fra «## Day N:» til «*End of Day N*»). En seksjonsfil
begynner med sin toppoverskrift («# Introduction», «# Appendix A: ...») og
erstatter alt fram til neste toppoverskrift. Med --grunnlag flettes først alle
day-*.md i MAPPE inn, så de oppgitte filene. Alt skjer i en midlertidig kopi;
repoets manus røres ikke, og flere kan måle samtidig.

Hele boka settes med sett_bok.py (5 x 8). Skriptet skriver sider og ledige
linjer på siste side for hver dag, og trykt startside for hver del, mot
budsjettet i bok/kilder/m22/budsjett_5x8_2026-11-21.json og originalens
startsider. Exit 0 = alle oppgitte dager har sitt sidetall, minst 3 linjer på
siste side, og ingen del har flyttet seg.
"""
import argparse, json, os, pathlib, re, shutil, subprocess, sys, tempfile
import pymupdf

V = pathlib.Path(__file__).resolve().parent
BOK = V.parent / "bok"
FILER = ["01-front-intro-phase1.md", "02-phase2-phase3.md", "03-phase4-phase5.md", "04-back.md"]
B = json.loads((BOK / "kilder/m22/budsjett_5x8_2026-11-21.json").read_text())
HEADS = {"FORGED", "ELIASSOLBAKÅRNES"}
# Trykte startsider i den godkjente 124-sidersutgaven 21.11.2026
DELER = {"INTRODUCTION": None, "COMPANIONVIDEOS": None, "PHASEI": None, "PHASEII": None, "PHASEIII": None,
         "PHASEIV": None, "PHASEV": None, "CONCLUSION": None, "APPENDIXA": None, "APPENDIXB": None,
         "APPENDIXC": 113, "ABOUTTHEAUTHOR": 115}

def flett_dag(tekster, blokk):
    m = re.match(r"## Day (\d+):", blokk)
    assert m, "dagfilen må begynne med «## Day N:»"
    n = int(m.group(1))
    assert blokk.endswith(f"*End of Day {n}*"), f"Day {n}: filen må slutte med «*End of Day {n}*»"
    mønster = re.compile(r"^## Day %d:.*?^\*End of Day %d\*$" % (n, n), re.M | re.S)
    treff = [f for f, t in tekster.items() if mønster.search(t)]
    assert len(treff) == 1, f"Day {n}: fant {len(treff)} steder"
    tekster[treff[0]] = mønster.sub(lambda _: blokk, tekster[treff[0]], count=1)
    return n

def flett_seksjon(tekster, blokk):
    hode = blokk.split("\n")[0]
    assert hode.startswith("# "), "seksjonsfilen må begynne med en toppoverskrift"
    mønster = re.compile(r"^" + re.escape(hode) + r"\n.*?(?=^# |\Z)", re.M | re.S)
    treff = [f for f, t in tekster.items() if mønster.search(t)]
    assert len(treff) == 1, f"{hode}: fant {len(treff)} steder"
    tekster[treff[0]] = mønster.sub(lambda _: blokk.rstrip() + "\n\n", tekster[treff[0]], count=1)
    return hode

def linjer(p):
    ls = [l for l in p.get_text().split("\n") if l.strip()]
    if ls and ls[0].replace(" ", "") in HEADS:
        ls = ls[1:]
    if ls and re.fullmatch(r"\s*([ivxlc]+|\d+)\s*", ls[-1]):
        ls = ls[:-1]
    return ls

def mål(pdf):
    d = pymupdf.open(pdf)
    start, slutt, deler = {}, {}, {}
    for p in d:
        ls = linjer(p)
        if ls:
            m = re.fullmatch(r"D\s*A\s*Y\s+([\d\s]+)", ls[0].strip())
            if m:
                start[int(m.group(1).replace(" ", ""))] = p.number
            hode = ls[0].replace(" ", "").upper()
            for navn in DELER:
                treff = hode == navn if navn.startswith("PHASE") else hode.startswith(navn)
                if treff and navn not in deler and p.number >= 8:
                    deler[navn] = p.number + 1 - 8
        for m in re.finditer(r"E\s*N\s*D\s+O\s*F\s+D\s*A\s*Y\s+([\d\s]+?)(?=\s*$|\s{2}|\n)", p.get_text()):
            slutt[int(m.group(1).replace(" ", "").replace("\n", ""))] = p.number
    def ledige_på(i):
        blokker = [b for b in d[i].get_text("blocks") if b[4].strip() and not re.fullmatch(r"\s*([ivxlc]+|\d+)\s*", b[4])
                   and b[4].replace(" ", "").strip() not in HEADS]
        return None if not blokker else int((8 - 0.75 - max(b[3] for b in blokker) / 72) / (14.2 / 72))
    navn = list(DELER)
    halen = {}
    for a, b in zip(navn, navn[1:]):
        if a in deler and b in deler:
            halen[a] = ledige_på(deler[b] + 8 - 2)
    deler["_halen"] = halen
    dager = {}
    for n in range(1, 41):
        s, e = start.get(n), slutt.get(n)
        if s is None or e is None:
            continue
        blokker = [b for b in d[e].get_text("blocks") if b[4].strip() and not re.fullmatch(r"\s*\d+\s*", b[4])]
        ledige = int((8 - 0.75 - max(b[3] for b in blokker) / 72) / (14.2 / 72))
        dager[n] = (e - s + 1, ledige, len(linjer(d[e])))
    return len(d), dager, deler

def sett(tekster, mappe):
    m = mappe / "manus"
    m.mkdir(parents=True)
    for f, t in tekster.items():
        (m / f).write_text(t, encoding="utf-8")
    shutil.copytree(BOK / "manus" / "assets", m / "assets")
    subprocess.run([sys.executable, str(V / "bygg_manus.py"), str(m)], check=True, capture_output=True)
    pdf = mappe / "ut.pdf"
    r = subprocess.run([sys.executable, str(V / "sett_bok.py"), str(m / "FORGED_manus.md"), str(pdf), "--trim", "5x8"],
                       capture_output=True, text=True)
    if r.returncode:
        sys.exit("settingen feilet:\n" + r.stderr[-2000:])
    return mål(pdf)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("filer", nargs="*")
    ap.add_argument("--grunnlag")
    ap.add_argument("--seksjon", action="append", default=[])
    ap.add_argument("--pdf", help="ta vare på PDF-en her")
    a = ap.parse_args()
    orig = {f: (BOK / "manus" / f).read_text(encoding="utf-8") for f in FILER}
    tekster = dict(orig)
    if a.grunnlag:
        for f in sorted(pathlib.Path(a.grunnlag).glob("day-*.md")):
            flett_dag(tekster, f.read_text(encoding="utf-8").strip())
    egne = [flett_dag(tekster, pathlib.Path(f).read_text(encoding="utf-8").strip()) for f in a.filer]
    for f in a.seksjon:
        flett_seksjon(tekster, pathlib.Path(f).read_text(encoding="utf-8").strip())
    with tempfile.TemporaryDirectory() as tmp:
        sider, dager, deler = sett(tekster, pathlib.Path(tmp))
        if a.pdf:
            shutil.copy(pathlib.Path(tmp) / "ut.pdf", a.pdf)
    with tempfile.TemporaryDirectory() as tmp:
        _, _, deler0 = sett(orig, pathlib.Path(tmp))
    feil = []
    vis = egne if (egne or a.seksjon) else sorted(dager)
    halen = deler.pop("_halen"); deler0.pop("_halen")
    for f in a.seksjon:
        hode = pathlib.Path(f).read_text(encoding="utf-8").split("\n")[0][2:].split(":")[0].replace(" ", "").upper()
        if hode in halen:
            print(f"  MERK {hode}: {halen[hode] if halen[hode] is not None else 'tom side'} ledige linjer på siste side")
    for n in vis:
        if n not in dager:
            feil.append(f"Day {n}: fant ikke start eller slutt"); continue
        s, l, ls = dager[n]
        ok = s == B[str(n)]["pages"] and ls >= 3
        print(f"  {'OK  ' if ok else 'FEIL'} Day {n}: {s} sider (budsjett {B[str(n)]['pages']}), "
              f"{ls} linjer på siste side, {l} ledige linjer")
        if not ok:
            feil.append(f"Day {n}")
    for navn in DELER:
        mal = DELER[navn] or deler0.get(navn)
        ok = deler.get(navn) == mal
        if not ok or a.seksjon:
            print(f"  {'OK  ' if ok else 'FEIL'} {navn} starter på trykt side {deler.get(navn)} (skal være {mal})")
        if not ok:
            feil.append(navn)
    print(f"  {'OK  ' if sider == 124 else 'MERK'} hele boka: {sider} sider (skal være 124)")
    print("RESULTAT:", "består" if not feil else f"{len(feil)} feil: " + ", ".join(feil))
    sys.exit(1 if feil else 0)

if __name__ == "__main__":
    main()
