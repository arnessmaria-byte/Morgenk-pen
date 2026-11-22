#!/usr/bin/env python3
"""Kontrollerer manus og KDP-PDF mot reglene R1-R10 fra forfatterens instruks 20.11.2026.

Reglene er de samme som i forged_apply_r1_r10.py fra økten «Mantelen kommandobro»,
men kontrollen her skriver ingenting og bruker repoets egne kilder:
grunnlinja fra 20.11 (git 263ff22) og oktoberrettelsene i kilder/nov12.
R6 kontrolleres mot setningen forfatteren godkjente 21.11 («Choosing for yourself …»).

Bruk (fra Forged/bok): python3 ../verktoy/sjekk_r1_r10.py manus/FORGED_manus.md ut/FORGED_Interior_5x8_KDP.pdf
Exit 0 = alt består.
"""
import hashlib, json, re, subprocess, sys, pathlib

URL = "https://www.youtube.com/playlist?list=PLSG5mjEhTu-s"
R3 = "One new video is released each day from January 1 through February 9, 2027, at 4:00 p.m. New York time."
R4_7 = {
    "R4": (12, "### The Practice", "Take that small step without drama or announcement. Most costs are paid in private."),
    "R5": (18, "### What This Day Is Really About", "Failure is feedback: it shows where you counted on a strength you had not trained."),
    "R6": (28, "### Healing Forge: When Control Once Meant Safety", "Choosing for yourself is gentler than rigid control. Start with one chosen limit rather than trying to control everything."),
    "R7": (39, "### What This Day Is Really About", "Authority grows wherever someone carries responsibility without asking for credit."),
}
FREDET = {5: "Some discomfort is a signal.", 6: "Strength comes with responsibility attached.",
          10: "Whatever surrounds you will end up teaching you.", 29: "Pressure shows how well you prepared.",
          38: "Real growth builds up inside you, and it does not need to be announced."}
TILBAKE = {19: "He kept its correction general and never felt it was meant for him. He came away sure he was fine and rarely looked hard at himself.",
           40: "The temptations were still there, and his discipline still needed work. His surroundings were the same, but he carried himself differently in them."}
EN = "–"
LOVLIG_EN = re.compile(r"\b\d+:\d+" + EN + r"\d+\b|\bDays \d+" + EN + r"\d+\b")
n = lambda s: s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')

feil = []
def sjekk(regel, ok, tekst):
    print(("  OK   " if ok else "  FEIL ") + regel + " " + tekst)
    if not ok:
        feil.append(regel)

def nivaa1(t):
    m = list(re.finditer(r"^# .+$", t, re.M))
    return {x.group(0): t[x.start():(m[i + 1].start() if i + 1 < len(m) else len(t))].rstrip() for i, x in enumerate(m)}

def dager(t):
    h = list(re.finditer(r"^(#{1,2}) .+$", t, re.M)); out = {}
    for i, x in enumerate(h):
        d = re.match(r"^## Day (\d+):", x.group(0))
        if d:
            out[int(d.group(1))] = t[x.start():(h[i + 1].start() if i + 1 < len(h) else len(t))]
    return out

def under(dag, overskrift):
    i = dag.find(overskrift + "\n")
    if i < 0:
        return ""
    rest = dag[i + len(overskrift) + 1:]
    m = re.search(r"^(### |\*End of Day)", rest, re.M)
    return rest[:m.start()] if m else rest

md_path, pdf_path = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
t = md_path.read_text(encoding="utf-8")
grunn = subprocess.run(["git", "show", "263ff22:Forged/bok/ut/FORGED_manus.md"], capture_output=True, text=True,
                       cwd=pathlib.Path(__file__).resolve().parent).stdout
okt = json.loads((pathlib.Path(__file__).resolve().parent.parent / "bok/kilder/nov12/oktober_rettelser_mot_nov12.json").read_text())
print("Manus:", md_path, hashlib.sha256(t.encode()).hexdigest())

# R1
hd = [m.group(0) for m in re.finditer(r"^# .+$", t, re.M)]
sjekk("R1", "# Also by Elias Solbak Årnes" not in t and hd[-1] == "# About the Author" and hd[-2].startswith("# Appendix C"),
      "ingen «Also by» i manus; About the Author kommer rett etter Appendix C")
# R2, R3
cv = nivaa1(t).get("# Companion videos", "")
lik = [v for v in re.findall(r"PLSG5mjEhTu.s", t) if v != "PLSG5mjEhTu-s"]
sjekk("R2", cv.count(URL) == 2 and t.count(URL) == 2 and not lik, "adressen står to ganger med U+002D, ingen varianter")
sjekk("R3", cv.count(R3) == 1, "setningen om utgivelsesvinduet står én gang")
# R4-R7
D = dager(t)
for r, (d, oh, s) in R4_7.items():
    sjekk(r, s in under(D[d], oh) and t.count(s) == 1, f"Day {d}, {oh[4:]}: teksten står én gang og på riktig sted")
sjekk("R6", "Choosing one limit for yourself" not in t, "Day 28 har ikke lenger «one limit» og «one chosen limit» rett etter hverandre")
# R8
problemer, flere = [], []
for d in range(1, 41):
    ls = D[d].split("\n"); tl = [i for i, l in enumerate(ls) if l.startswith("|")]
    rader = [[c.strip() for c in ls[i].strip().strip("|").split("|")] for i in tl]
    j = tl[0] - 1
    while not ls[j].strip():
        j -= 1
    tm = re.fullmatch(r"### (.+) vs\. (.+)", ls[j])
    if tl != list(range(tl[0], tl[-1] + 1)) or any(len(r) != 2 for r in rader) or not tm or [tm.group(1), tm.group(2)] != rader[0]:
        problemer.append(d)
    k, linjer = tl[-1] + 1, []
    while k < len(ls) and not ls[k].startswith("### "):
        if ls[k].strip():
            linjer.append(ls[k].strip())
        k += 1
    if len(linjer) != 1 or (d in FREDET and linjer[0] != FREDET[d]):
        problemer.append(d)
    elif len(re.findall(r"[.!?](?=\s|$)", linjer[0])) > 1:
        flere.append(d)
sjekk("R8", not problemer, f"40 tabeller med to kolonner, tittel «X vs. Y» og én linje under; de fem fredede linjene står{'' if not problemer else '; avvik: ' + str(problemer)}")
print(f"  NOTE R8 to setninger i linja under tabellen på {len(flere)} dager: {flere} (forfatterens tekst, ikke endret)")
# R9
# Forfatterens komplette mesterordre 22.11.2026 ba om nye, konkrete scenarioer på Day 2-40.
# Da er de gjenopprettede scenariosetningene på Day 19 og 40 og oktoberrettelse nr. 4
# (scenariet på Day 4) erstattet etter ordre, og de meldes som merknad, ikke feil.
for d, s in TILBAKE.items():
    if s in under(D[d], "### The Scenario"):
        sjekk("R9", True, f"Day {d}: den godkjente teksten står i The Scenario")
    else:
        print(f"  NOTE R9 Day {d}: scenariet er skrevet nytt etter mesterordren 22.11 (den gjenopprettede teksten fra 20.11 er erstattet)")
for h in ("# Foreword", "# About the Author"):
    sjekk("R9", nivaa1(t).get(h) == nivaa1(grunn).get(h), f"{h[2:]} er uendret mot 20.11")
ERSTATTET = {11: "R5", 4: "mesterordren 22.11 (nytt scenario på Day 4)"}
mangler = [c["n"] for c in okt if c["n"] not in ERSTATTET and n(c["new"]) not in n(t)]
borte = [c["n"] for c in okt if c["n"] in ERSTATTET and n(c["new"]) not in n(t)]
sjekk("R9", not mangler, f"oktoberrettelsene: {22 - len(mangler) - len(borte)} av 22 står ordrett"
      + "".join(f"; nr. {k} er erstattet av {ERSTATTET[k]}" for k in borte) + ("" if not mangler else f"; mangler: {mangler}"))
# R10
strek = t.count(chr(0x2014)) + t.count(chr(0x2015))
ulovlig = [i for i, l in enumerate(t.split("\n"), 1) if EN in LOVLIG_EN.sub("", l)]
sjekk("R10", strek == 0 and not ulovlig and "�" not in t, f"lange streker {strek}; korte streker utenfor tallspenn på linje {ulovlig}")

# PDF
info = subprocess.run(["pdfinfo", str(pdf_path)], capture_output=True, text=True).stdout
sider = int(re.search(r"^Pages:\s+(\d+)", info, re.M).group(1))
str_ = re.search(r"^Page size:\s+([\d.]+) x ([\d.]+) pts", info, re.M)
tekst = subprocess.run(["pdftotext", "-layout", str(pdf_path), "-"], capture_output=True, text=True).stdout.split("\f")
print("PDF:", pdf_path, hashlib.sha256(pdf_path.read_bytes()).hexdigest(), sider, "sider")
sjekk("R1", sider == 124, f"sidetall {sider}, ventet 124")
sjekk("R1", not any("ALSO BY ELIAS" in p or "Also by Elias" in p for p in tekst), "ingen «Also by»-side og ingen linje for den i innholdslisten")
sjekk("R10", (float(str_.group(1)), float(str_.group(2))) == (360.0, 576.0) and sider % 2 == 0, "5 x 8 tommer (360 x 576 pt), partall sider")
sider_url = [(i, re.findall(r"https://www\.youtube\.com/playlist\?list=\S+", p), re.findall(r"^\s*(\d+)\s*$", p, re.M)) for i, p in enumerate(tekst, 1) if "PLSG5" in p]
sjekk("R2", len(sider_url) == 1 and sider_url[0][1] == [URL] and sider_url[0][2][-1:] == ["5"],
      f"adressen står udelt på trykt side 5: {sider_url}")
hel = "\n".join(tekst)
sjekk("R10", hel.count(chr(0x2014)) + hel.count(chr(0x2015)) == 0 and "�" not in hel and not [i for i, p in enumerate(tekst, 1) if EN in LOVLIG_EN.sub("", p)],
      "ingen lange streker, ingen erstatningstegn, korte streker bare i tallspenn")
flat = re.sub(r"\s+", " ", re.sub(r"(\w)-\n\s*(\w)", r"\1\2", re.sub("\u00ad\\s*", "", hel)))   # myk bindestrek og orddeling ved linjeskift
for r, (d, oh, s) in list(R4_7.items()) + [("R3", (0, "", R3))]:
    sjekk(r, re.sub(r"\s+", " ", s) in flat, f"PDF-en har teksten: «{s[:60]}»")
print("RESULTAT:", "alt består" if not feil else "feil i " + ", ".join(sorted(set(feil))))
sys.exit(1 if feil else 0)
