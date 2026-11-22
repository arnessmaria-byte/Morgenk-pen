#!/usr/bin/env python3
"""Sidebudsjett for 5 x 8-PDF-en (mesterordren 22.11.2026).

Bruk: python3 sjekk_sider.py PDF MANUS BUDSJETT.json
Kontrollerer: 124 sider, 8 romertallssider, Appendix C på trykt side 113 og
About the Author på trykt side 115, like mange sider per dag som i budsjettet,
minst 3 tekstlinjer på siste side av hver dag, 40 av 40 «Today's Action» i manus,
og ingen lange tankestreker. Skriver ledige linjer per dag. Exit 0 = alt består.
"""
import json, re, sys
import pymupdf

pdf, manus, budsjett = sys.argv[1], sys.argv[2], sys.argv[3]
d = pymupdf.open(pdf)
md = open(manus, encoding="utf-8").read()
B = json.load(open(budsjett))
HEADS = {"FORGED", "ELIASSOLBAKÅRNES"}
feil = []
def sjekk(ok, tekst):
    print(("  OK   " if ok else "  FEIL ") + tekst)
    if not ok:
        feil.append(tekst)

def linjer(p):
    ls = [l for l in p.get_text().split("\n") if l.strip()]
    if ls and ls[0].replace(" ", "") in HEADS:
        ls = ls[1:]
    if ls and re.fullmatch(r"\s*([ivxlc]+|\d+)\s*", ls[-1]):
        ls = ls[:-1]
    return ls

def folio(p):
    ls = [l.strip() for l in p.get_text().split("\n") if l.strip()]
    return ls[-1] if ls and re.fullmatch(r"[ivxlc]+|\d+", ls[-1]) else None

sjekk(len(d) == 124, f"{len(d)} sider (skal være 124)")
romer = [i for i in range(len(d)) if folio(d[i]) and re.fullmatch(r"[ivxlc]+", folio(d[i]))]
sjekk(max(romer) + 1 == 8 if romer else False, f"forsatsen har 8 sider (romertall), siste romertall på fysisk side {max(romer) + 1 if romer else '?'}")
def trykt(i):
    return i + 1 - 8
for navn, mal in (("APPENDIXC", 113), ("ABOUTTHEAUTHOR", 115)):
    sider = [i for i in range(10, len(d)) if (linjer(d[i]) or [""])[0].replace(" ", "").upper().startswith(navn)]
    sjekk(bool(sider) and trykt(sider[0]) == mal, f"{navn} starter på trykt side {trykt(sider[0]) if sider else '?'} (skal være {mal})")
start, slutt = {}, {}
for p in d:
    ls = linjer(p)
    if ls:
        m = re.fullmatch(r"D\s*A\s*Y\s+([\d\s]+)", ls[0].strip())
        if m:
            start[int(m.group(1).replace(" ", ""))] = p.number
    for m in re.finditer(r"E\s*N\s*D\s+O\s*F\s+D\s*A\s*Y\s+([\d\s]+?)(?=\s*$|\s{2}|\n)", p.get_text()):
        slutt[int(m.group(1).replace(" ", "").replace("\n", ""))] = p.number
avvik, korte, ledige = [], [], {}
for n in range(1, 41):
    s, e = start.get(n), slutt.get(n)
    if s is None or e is None:
        avvik.append(f"Day {n}: fant ikke start eller slutt"); continue
    sider = e - s + 1
    if sider != B[str(n)]["pages"]:
        avvik.append(f"Day {n}: {sider} sider, skal være {B[str(n)]['pages']}")
    ls = linjer(d[e])
    if len(ls) < 3:
        korte.append(f"Day {n}: {len(ls)} linjer på siste side")
    blokker = [b for b in d[e].get_text("blocks") if b[4].strip() and not re.fullmatch(r"\s*\d+\s*", b[4])]
    ledige[n] = int((8 - 0.75 - max(b[3] for b in blokker) / 72) / (14.2 / 72))
sjekk(not avvik, "hver dag har like mange sider som før" + ("" if not avvik else ": " + "; ".join(avvik)))
sjekk(not korte, "ingen dag ender med en side med under 3 linjer" + ("" if not korte else ": " + "; ".join(korte)))
print("  ledige linjer på siste side:", " ".join(f"{k}:{v}" for k, v in ledige.items()))
deler = re.split(r"^## Day ", md, flags=re.M)[1:]
med = [int(x.split(":")[0]) for x in deler if "**Today’s Action:**" in x or "**Today's Action:**" in x]
sjekk(len(med) == 40, f"{len(med)} av 40 dager har «Today's Action» i The Practice")
hel = "\n".join(p.get_text() for p in d)
sjekk(hel.count(chr(0x2014)) + hel.count(chr(0x2015)) == 0 and md.count(chr(0x2014)) + md.count(chr(0x2015)) == 0, "ingen lange tankestreker i manus eller PDF")
print("RESULTAT:", "alt består" if not feil else f"{len(feil)} feil")
sys.exit(1 if feil else 0)
