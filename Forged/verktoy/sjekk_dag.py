#!/usr/bin/env python3
"""Kontroll av én omskrevet dag mot originalen (mesterordren 22.11.2026).

Bruk: python3 sjekk_dag.py ORIGINAL_DAG.md NY_DAG.md --dag N --ledige L --brukt B
  L = ledige linjer på dagens siste side i 5 x 8 (fra budsjettet)
  B = linjer brukt på dagens siste side
Exit 0 = alle sperrer består. Linjetallet er et anslag (63 tegn per linje,
52 i punktlister); den bygde PDF-en avgjør til slutt.
"""
import argparse, math, re, sys

FASTE = ["You are not beyond repair.",
         "God often steers you through your attention, and where your attention stays, your life follows.",
         "Feeling distant is not the same as being abandoned.",
         "His silence is not neglect. He has not let go of you.",
         "Being a witness means being the same man at school, at work, at home, and online. It is not a show.",
         "| Advertises conviction | Carries it quietly |",
         "If the heaviness will not let up, talk to a pastor, a doctor, or a licensed counselor.",
         "He asked you to be alive",
         "Write the answers down where only you will see them. Understanding your anger helps you control it.",
         "Do not rush to analyze it or point it at someone else. Let it show you yourself first.",
         "Do not chase anything new today: no new message, no signs, no fresh reassurance.",
         "Take that small step without drama or announcement. Most costs are paid in private.",
         "Failure is feedback: it shows where you counted on a strength you had not trained.",
         "Choosing for yourself is gentler than rigid control.",
         "Authority grows wherever someone carries responsibility without asking for credit.",
         "Some discomfort is a signal.", "Strength comes with responsibility attached.",
         "Whatever surrounds you will end up teaching you.", "Pressure shows how well you prepared.",
         "Real growth builds up inside you, and it does not need to be announced."]
BREMSER = ["Do not act on it today", "You do not need to act yet", "Delete nothing yet", "Leave the fixing for later",
           "do not need to act", "Do not act yet", "for later"]
DASH = (chr(0x2014), chr(0x2015))

def deler(t):
    """Seksjoner: '_innled' (vers og åpning) og hver '### '-overskrift."""
    out, cur, buf = {}, "_innled", []
    for l in t.split("\n"):
        if l.startswith("### "):
            out[cur] = "\n".join(buf).strip(); cur, buf = l[4:].strip(), []
        else:
            buf.append(l)
    out[cur] = "\n".join(buf).strip()
    return out

def linjer(tekst):
    n = 0
    for para in [p for p in re.split(r"\n\s*\n", tekst) if p.strip()]:
        rader = [l for l in para.split("\n") if l.strip()]
        if rader and all(r.startswith("- ") for r in rader):
            n += sum(math.ceil(len(re.sub(r"\*", "", r[2:])) / 52) for r in rader)
        elif rader and not rader[0].startswith(("|", ">")) and not re.fullmatch(r"\*End of Day \d+\*", rader[0]):
            n += math.ceil(len(re.sub(r"\*", "", " ".join(rader))) / 63)
    return n

def ord_(s):
    return len(re.findall(r"[A-Za-z0-9’']+", s))

ap = argparse.ArgumentParser()
ap.add_argument("orig"); ap.add_argument("ny")
ap.add_argument("--dag", type=int, required=True); ap.add_argument("--ledige", type=int, required=True)
ap.add_argument("--brukt", type=int, required=True)
a = ap.parse_args()
o, n = open(a.orig, encoding="utf-8").read().strip(), open(a.ny, encoding="utf-8").read().strip()
feil = []
def sjekk(ok, tekst):
    print(("  OK   " if ok else "  FEIL ") + tekst)
    if not ok:
        feil.append(tekst)

so, sn = deler(o), deler(n)
lo, ln = o.split("\n"), n.split("\n")
sjekk(lo[0] == ln[0], "dagtittelen er uendret")
sjekk([l for l in lo if l.startswith(">")] == [l for l in ln if l.startswith(">")], "bibelverset (epigrafen) er uendret")
ko, kn = list(so), list(sn)
tab_o = [k for k in ko if " vs. " in k]; tab_n = [k for k in kn if " vs. " in k]
sjekk([k if k not in tab_o else "TABELL" for k in ko] == [k if k not in tab_n else "TABELL" for k in kn],
      f"seksjonene står i samme rekkefølge: {kn}")
sjekk(sum(1 for l in ln if re.fullmatch(r"\*End of Day \d+\*", l.strip())) == 1 and ln[-1].strip() == f"*End of Day {a.dag}*", "slutter med End of Day")
# tabell
to = [l for l in lo if l.startswith("|")]; tn = [l for l in ln if l.startswith("|")]
sjekk(len(to) == len(tn) and all(l.count("|") == 3 for l in tn), "tabellen har like mange rader og to kolonner")
if tab_n:
    m = re.fullmatch(r"(.+) vs\. (.+)", tab_n[0]); hode = [c.strip() for c in tn[0].strip().strip("|").split("|")]
    sjekk(bool(m) and [m.group(1), m.group(2)] == hode, "tabelltittelen stemmer med kolonnecellene")
    etter = sn[tab_n[0]].split("\n"); under = [l for l in etter if l.strip() and not l.startswith("|")]
    sjekk(len(under) == 1, "én oppsummeringslinje under tabellen")
# faste setninger
for f in FASTE:
    if f in o:
        sjekk(f in n, f"fast setning står: «{f[:50]}»")
# scenario
if a.dag != 1:
    w = ord_(sn.get("The Scenario", ""))
    sjekk(55 <= w <= 85, f"scenariet har {w} ord (55 til 85)")
# øvelsen
pr = sn.get("The Practice", "")
sjekk(pr.count("**Today's Action:**") == 1, "The Practice har nøyaktig én «**Today's Action:**»")
sjekk(not [b for b in BREMSER if b.lower() in pr.lower()], "ingen bremseformuleringer i The Practice")
sp = sum(1 for l in pr.split("\n") if l.strip().startswith("- ")) + len(re.findall(r"\?", " ".join(l for l in pr.split("\n") if not l.startswith("- "))))
sjekk(2 <= sp <= 4, f"The Practice har {sp} spørsmål (2 til 3, høyst 4)")
# bibelforankring
wd = sn.get("What This Day Is Really About", "")
vers = " ".join(l[1:].strip() for l in ln if l.startswith(">") and l[1:].strip())
ref = [l[1:].strip() for l in ln if l.startswith(">") and l[1:].strip()][-1]
bok = re.sub(r"\s*\d+:\d+.*$", "", ref)
sjekk(("Christ" in wd or "Jesus" in wd), "What This Day Is Really About nevner Kristus")
# sitater fra verset må stå ordrett
for q in re.findall(r"[“\"]([^”\"]+)[”\"]", wd):
    vn = vers.replace("“", "").replace("”", "").replace('"', "")
    sjekk(q.strip(" ,.") in vn, f"sitatet «{q[:40]}» står ordrett i verset")
# tegn
sjekk(not any(c in n for c in DASH), "ingen lange tankestreker")
sjekk(not re.search(" " + chr(0x2013) + " ", n) and not re.search(r"[A-Za-z]" + chr(0x2013) + r"[A-Za-z]", n), "ingen korte tankestreker i prosa")
prosa = "\n".join(l for l in ln if not l.startswith(">") and not l.startswith("## "))
sjekk(not any(c in prosa for c in "“”’‘"), "rette anførselstegn og apostrofer i prosaen, som i kildefilene")
sjekk(len(re.findall(r"fits? together", n, re.I)) <= 1, "«fit together» høyst én gang")
for fr in ("Here is the thing", "Let me be clear", "This day is not about", "Today is not about"):
    sjekk(fr not in n, f"ikke «{fr}»")
# linjebudsjett
d = linjer(n) - linjer(o)
sjekk(d <= a.ledige - 1, f"anslått endring {d:+d} linjer, høyst {a.ledige - 1:+d}")
sjekk(d >= -(a.brukt - 4), f"anslått endring {d:+d} linjer, minst {-(a.brukt - 4):+d} (ellers mister dagen en side)")
print(f"ord: {ord_(o)} -> {ord_(n)}")
print("RESULTAT:", "består" if not feil else f"{len(feil)} feil")
sys.exit(1 if feil else 0)
