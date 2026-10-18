#!/usr/bin/env python3
"""Stiller det gamle videomanuset opp mot boken slik den er nå, dag for dag.

Leser voiceover-linjene fra FORGED_40_Day_Video_Prompts.pdf (hentet ut til
bok/kilder/videomanus_2026-08-05.json) og henter tittel, bibelvers, åpning,
The Practice og Healing Forge fra ut/FORGED_manus.md. Hver gammel linje merkes
med om den står ordrett i boken nå. Resultatet er vedlegget ChatGPT får
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
# Samme tekst med linjeskift beholdt, så setningsstart etter overskrift og avsnitt kan sees
tl = re.sub(r"[ \t]+", " ", t.replace("\u2019", "'").replace("\u2018", "'").replace("\u201c", '"').replace("\u201d", '"')).lower()
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

ordrett = ikke = tittelavvik = hele = 0
o = ["# Vedlegg til videoprompten: gammelt videomanus mot boken nå",
     "",
     "Laget maskinelt 18.10.2026 med `verktoy/lag_videogrunnlag.py`.",
     "",
     "- **Gammelt videomanus:** voiceover-linjene i `FORGED_40_Day_Video_Prompts.pdf` (Drive, sist endret 05.08.2026). "
     "Det er skrevet mot en eldre versjon av boken.",
     "- **Boken nå:** `ut/FORGED_manus.md`, endelig tekst 18.10.2026.",
     "- **«ja, hel setning»** betyr at linjen står ord for ord som en hel setning et sted i boken nå, ikke nødvendigvis samme dag.",
     "- **«del av en lengre setning»** betyr at ordene står i boken, men bare som en bit av en lengre setning. "
     "Da kan linjen si noe annet enn boken. «God does not always speak.» (Day 30) står for eksempel i boken som "
     "«God does not always speak to ease your discomfort.».",
     "- **«nei»** betyr at linjen ikke står ordrett i boken. Det sier ikke alene at linjen er feil, "
     "for mange linjer er korte sammendrag. De må vurderes etter mening.",
     "- **«Ask:» og «Ask yourself:»** først i en linje er ikke regnet med. Spørsmålet etter kolon er sammenlignet med boken.",
     "- **Scenenumrene følger manuset.** Scene 1 har ingen voiceover, bare en klikkelyd. Scene 2 er tittel-linjen, "
     "og scene 7 er «The practice for today.». Disse to linjene er ikke tatt med, så tabellene viser scene 3 til 6 og 8 til 10.",
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
    o.append("| Scene | Linje | Står i boken nå? |")
    o.append("|---|---|---|")
    for i, linje in enumerate(v["vo"], start=2):
        if i == 2 or linje == "The practice for today.":
            continue
        kjerne = re.sub(r"^ask(?: yourself)?: ", "", norm(linje)).rstrip(".?!")
        hel = re.search(r"(?:^|[.!?:]\s+|\n|[|\-]\s|\*\*\s*)" + re.escape(kjerne) + r"(?:[.!?]|(?=[ \t]*(?:$|\||\*)))", tl, re.M)
        hit = kjerne in tn
        ordrett += hit
        ikke += not hit
        hele += bool(hel)
        merke = "ja, hel setning" if hel else ("del av en lengre setning" if hit else "nei")
        o.append(f"| {i} | {linje} | {merke} |")
    o.append("")
    o.append("**The Practice i boken nå:**")
    o.append("")
    for l in d["praksis"].splitlines():
        o.append("> " + l if l.strip() else ">")
    o.append("")
    o.append(f"**{d['hf_tittel']}**")
    o.append("")
o[o.index("SAMMENDRAG_HER")] = (f"**Sammendrag:** Manuset har {sum(len(v['vo']) for v in vo.values())} voiceover-linjer. "
                                f"Uten tittel-linjen og «The practice for today.» er det {ordrett + ikke} linjer igjen. "
                                f"{ordrett} av dem står ordrett i boken nå, og bare {hele} som hele setninger. "
                                + ("Alle 40 dagtitler stemmer med boken." if not tittelavvik else f"{tittelavvik} dagtitler avviker fra boken."))
ut.write_text("\n".join(o).rstrip() + "\n", encoding="utf-8")
print("skrev", ut, f"ordrett {ordrett} (hele setninger {hele}), ikke ordrett {ikke}")
