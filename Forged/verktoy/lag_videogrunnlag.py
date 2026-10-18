#!/usr/bin/env python3
"""Stiller det gamle videomanuset opp mot dagens bok, dag for dag.

Leser voiceover-linjene fra FORGED_40_Day_Video_Prompts.pdf (hentet ut til
bok/kilder/videomanus_2026-08-05.json) og henter tittel, bibelvers, åpning,
The Practice og Healing Forge fra ut/FORGED_manus.md. Hver gammel linje merkes
med om den står ordrett i dagens bok. Resultatet er vedlegget ChatGPT får
sammen med videoene.

Bruk: python3 lag_videogrunnlag.py bok/kilder/videomanus_2026-08-05.json \
          bok/ut/FORGED_manus.md bok/15-vedlegg-videomanus-mot-bok.md
"""
import json, re, sys, pathlib

vo_fil, manus_fil, ut = map(pathlib.Path, sys.argv[1:4])
vo = json.loads(vo_fil.read_text(encoding="utf-8"))
t = manus_fil.read_text(encoding="utf-8")


def norm(s):
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", s).strip().lower()


tn = norm(t)
deler = re.split(r"^## (?=Day \d+: )", t, flags=re.M)
dager = {}
for d in deler[1:]:
    hode, _, kropp = d.partition("\n")
    n = int(re.match(r"Day (\d+)", hode).group(1))
    kropp = kropp.split("*End of Day")[0]
    seksjoner = re.split(r"^### ", kropp, flags=re.M)
    innled = seksjoner[0]
    vers = [l[1:].strip() for l in innled.splitlines() if l.startswith(">") and l[1:].strip()]
    apning = [p.strip() for p in innled.split("\n\n") if p.strip() and not p.lstrip().startswith(">")]
    s = {}
    for sek in seksjoner[1:]:
        tittel, _, tekst = sek.partition("\n")
        s[tittel.strip()] = tekst.strip()
    hf = next(k for k in s if k.startswith("Healing Forge"))
    dager[n] = {"tittel": hode.split(": ", 1)[1].strip(), "vers": vers, "apning": apning,
                "praksis": s["The Practice"], "hf_tittel": hf, "hf": s[hf]}

ordrett = ikke = tittelavvik = 0
o = ["# Vedlegg til videoprompten: gammelt videomanus mot dagens bok",
     "",
     "Laget maskinelt 18.10.2026 med `verktoy/lag_videogrunnlag.py`.",
     "",
     "- **Gammelt videomanus:** voiceover-linjene i `FORGED_40_Day_Video_Prompts.pdf` (Drive, sist endret 05.08.2026). "
     "Det er skrevet mot en eldre versjon av boken.",
     "- **Dagens bok:** `ut/FORGED_manus.md`, endelig tekst 18.10.2026.",
     "- **Merket «ordrett»** betyr at linjen står ord for ord i dagens bok. Det sier ikke at linjen er feil. "
     "Mange linjer er korte sammendrag, og de må vurderes etter mening.",
     "- Linjen «The practice for today.» og tittel-linjen er ikke tatt med.",
     "",
     "SAMMENDRAG_HER",
     ""]
for n in range(1, 41):
    d = dager[n]
    v = vo[str(n)]
    o.append(f"## Day {n}: {d['tittel']}")
    o.append("")
    if v["title"].upper().replace("'", "’") != d["tittel"].upper():
        tittelavvik += 1
        o.append(f"**Tittel i videomanuset:** {v['title']} (avviker fra boken)")
        o.append("")
    o.append(f"**Bibelvers (ESV):** {d['vers'][0]} ({d['vers'][1]})")
    o.append("")
    o.append("**Åpningen i boken nå:**")
    o.append("")
    for p in d["apning"]:
        o.append("> " + p)
        o.append(">")
    o.pop()
    o.append("")
    o.append("**Voiceover i det gamle videomanuset:**")
    o.append("")
    o.append("| Scene | Linje | Ordrett i boken nå? |")
    o.append("|---|---|---|")
    for i, linje in enumerate(v["vo"], start=2):
        if i == 2 or linje == "The practice for today.":
            continue
        hit = norm(linje).rstrip(".?") in tn
        ordrett += hit
        ikke += not hit
        o.append(f"| {i} | {linje} | {'ordrett' if hit else 'nei'} |")
    o.append("")
    o.append("**The Practice i boken nå:**")
    o.append("")
    for l in d["praksis"].splitlines():
        o.append("> " + l if l.strip() else ">")
    o.append("")
    o.append(f"**{d['hf_tittel']}**")
    o.append("")
o[o.index("SAMMENDRAG_HER")] = (f"**Sammendrag:** {ordrett} av {ordrett + ikke} voiceover-linjer står ordrett i dagens bok. "
                                + ("Alle 40 dagtitler stemmer med boken." if not tittelavvik else f"{tittelavvik} dagtitler avviker fra boken."))
ut.write_text("\n".join(o).rstrip() + "\n", encoding="utf-8")
print("skrev", ut, f"ordrett {ordrett}, ikke ordrett {ikke}")
