#!/usr/bin/env python3
"""Teologisk og praktisk sjekkliste for FORGED (forfatterens komplette mesterordre 22.11.2026).

Bruk: python3 sjekk_teologi.py MANUS.md            (hele boka)
      python3 sjekk_teologi.py FIL [FIL ...]        (enkeltdager eller seksjoner: bare kravene for det som står i filene)
Kontrollerer at hvert punkt i ordren står der det skal: trosbekjennelsen fra 381
uten filioque, læregrunnlaget (Skriften alene, rettferdiggjørelsen, omvendelsen,
dåpen, nattverden, nådegavene, skapelsen, renheten, livet), oppgjøret
(Jezebels ånd, kvinnelige prester, vigsel av likekjønnede, utstøting av
bibeltro prester, leiesvenner), 40 av 40 «Today's Action», fasesjekk på dag 8,
16, 24, 32 og 40, ingen terapifraser, og ingen tankestreker.
Exit 0 = alt står. Sidetallet kontrolleres av sjekk_sider.py.
"""
import re, sys

md = "\n\n".join(open(f, encoding="utf-8").read() for f in sys.argv[1:])
md = md.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
feil = []
def sjekk(ok, tekst):
    print(("  OK   " if ok else "  FEIL ") + tekst)
    if not ok:
        feil.append(tekst)

def dag(n):
    m = re.search(r"^## Day %d:.*?^\*End of Day %d\*$" % (n, n), md, re.M | re.S)
    return m.group(0) if m else ""

def seksjon(hode):
    m = re.search(r"^# " + re.escape(hode) + r".*?(?=^# |\Z)", md, re.M | re.S)
    return m.group(0) if m else ""

STEDER = {"Introduction": seksjon("Introduction"), "Appendix A": seksjon("Appendix A"),
          "Appendix B": seksjon("Appendix B"), "Appendix C": seksjon("Appendix C")}
for n in range(1, 41):
    STEDER[f"Day {n}"] = dag(n)

# (sted, [regex som alle må treffe], beskrivelse)
KRAV = [
    ("Introduction", [r"Constantinople", r"381", r"God from God", r"John 15:26", r"Galatians 4:6"], "trosbekjennelsen fra 381: Faderen eneste kilde, Sønnen Gud av Gud, Ånden fra Faderen"),
    ("Introduction", [r"1 Corinthians 11:3", r"order"], "den guddommelige ordenen (1 Kor 11:3)"),
    ("Introduction", [r"postmodern", r"feminis", r"woke", r"demasculiniz|feminized"], "fienden navngitt: postmodernisme, radikalfeminisme, woke, demaskulinisert kultur og feminisert kirke"),
    ("Introduction", [r"Jezebel"], "Jezebels ånd nevnt i innledningen"),
    ("Introduction", [r"10 p\.m\.|10:00 p\.m\.|before 10"], "hver Today's Action kan gjøres før kl. 22"),
    ("Introduction", [r"John 10:35"], "Skriften alene som norm"),
    ("Day 2", [r"apostle"], "dag 2: brudd med kirke eller krets som har forlatt apostlenes lære"),
    ("Day 3", [r"John 10:35|Acts 17:11"], "dag 3: Skriften alene"),
    ("Day 4", [r"Father", r"1 Corinthians 11:3|order without lesser worth"], "dag 4: orden uten mindre verd"),
    ("Day 6", [r"Genesis 1:27", r"Acts 17:26", r"NKJV", r"Adam"], "dag 6: skapelsen, ett blod (Apg 17:26 NKJV), den historiske Adam"),
    ("Day 12", [r"Elijah", r"Jezebel", r"1 Kings 18:21|Revelation 2:20"], "dag 12: Elia på Karmel og Jezebels ånd"),
    ("Day 13", [r"council", r"Christ"], "dag 13: kirkeråd som krever kompromiss"),
    ("Day 16", [r"Flee from sexual immorality", r"Mark 10:6"], "dag 16: renhet og ekteskapet mellom én mann og én kvinne"),
    ("Day 18", [r"Peter", r"Galatians 2:16|Romans 3:25", r"1 John 1:9"], "dag 18: Peter, rettferdiggjørelse ved tro, omvendelse i Healing Forge"),
    ("Day 19", [r"1 Timothy 3:16", r"NKJV", r"received|Masoretic"], "dag 19: Skriften alene med mottatt lesemåte (1 Tim 3:16 NKJV)"),
    ("Day 19", [r"Today's Action:\*\*[^\n]*(congregation|church|elders)"], "dag 19: Today's Action prøver egen menighet"),
    ("Day 20", [r"2 Timothy 2:2"], "dag 20: brorskap med prøvde menn"),
    ("Day 20", [r"Today's Action:\*\*[^\n]*(text|message)"], "dag 20: Today's Action sender melding til en bibeltro bror"),
    ("Day 21", [r"1 John 1:9", r"Mark 9:4[3-8]"], "dag 21: omvendelse, rensing, og Jesu advarsel (Mark 9)"),
    ("Day 21", [r"Today's Action:\*\*[^\n]*(brother|secre)", r"Today's Action:\*\*[^\n]*trigger"], "dag 21: bryt hemmeligholdet og kutt hovedutløseren"),
    ("Day 22", [r"John 15:26", r"Galatians 4:6", r"Checklist Faith"], "dag 22: Ånden fra Faderen, gitt som Sønnens Ånd; tabellen «Checklist Faith»"),
    ("Day 24", [r"Mark 16:16", r"Acts 8:37", r"NKJV"], "dag 24: troendes dåp (Apg 8:37 NKJV)"),
    ("Day 27", [r"Jeremiah 23:16|2 Peter 2:1"], "dag 27: vokt deg for falske profeter"),
    ("Day 30", [r"1 Corinthians 10:16", r"1 Corinthians 11:2[89]"], "dag 30: nattverden for døpte troende som prøver seg selv"),
    ("Day 31", [r"Psalm 139:13", r"conception"], "dag 31: kjønn gitt med kroppen, det ufødte liv hellig fra unnfangelsen"),
    ("Day 33", [r"hireling", r"John 10:1[1-3]", r"2 Peter 2:1", r"Biblical Shepherd vs\. Hireling Prophet"], "dag 33: leiesvenner og falske profeter; tabellen «Biblical Shepherd vs. Hireling Prophet»"),
    ("Day 33", [r"Genesis 1:27"], "dag 33: likt gudsbilde for kvinner og menn (verdighetssetningen)"),
    ("Day 35", [r"Jezebel", r"1 Kings 21:25"], "dag 35: Jezebel styrte med press og manipulasjon"),
    ("Day 38", [r"Acts 4:31|Acts 1:8", r"gift"], "dag 38: Åndens gaver har ikke opphørt"),
    ("Appendix A", [r"John 10:35|Acts 17:11"], "vedlegg A: Skriften alene"),
    ("Appendix B", [r"Constantinople", r"381", r"God from God", r"Light from Light", r"begotten, not made", r"proceeds from the Father"], "vedlegg B: hele bekjennelsen fra 381"),
    ("Appendix B", [r"1 John 1:9|cleans"], "vedlegg B: Healing Forge som omvendelse og Kristi rensing"),
    ("Appendix C", [r"2 Timothy 2:2", r"Jezebel", r"women (pastors|priests)"], "vedlegg C: kirkestandarden"),
]
HEL = all(STEDER.values())
if not HEL:
    print("  MERK delkontroll: bare kravene for", ", ".join(k for k, v in STEDER.items() if v))
for sted, mønstre, tekst in KRAV:
    t = STEDER[sted]
    if not HEL and not t:
        continue
    mangler = [m for m in mønstre if not re.search(m, t, re.I if m.islower() else 0)]
    sjekk(bool(t) and not mangler, f"{sted}: {tekst}" + ("" if not mangler else f" (mangler: {', '.join(mangler)})"))

# Hele boka
if HEL:
  sjekk(not re.search(r"proceeds from the Father,? and (from )?the Son", md, re.I) and "filioque" not in md.lower().replace("without the filioque", ""),
        "ingen filioque: Ånden utgår fra Faderen alene")
  for mønster, tekst in [(r"1 Timothy 2:12", "kvinnelige prester og biskoper mot 1 Tim 2:12-13"),
                         (r"1 Timothy 3:2", "eldste og tilsynsmenn er prøvde menn (1 Tim 3:2)"),
                         (r"Titus 1:6", "Tit 1:6"),
                         (r"same-sex", "vigsel og velsignelse av likekjønnede mot Mark 10:6-9"),
                         (r"Romans 1:2[67]", "Rom 1:26-27"),
                         (r"1 Corinthians 6:9", "1 Kor 6:9-11"),
                         (r"pushes out the pastors|conscience and his paycheck", "press og utstøting av bibeltro prester"),
                         (r"hirelings", "«hirelings»"),
                         (r"Galatians 1:8", "Gal 1:8-9 mot et annet evangelium"),
                         (r"bear God's image equally", "verdighetssetningen: kvinner og menn bærer Guds bilde likt"),
                         (r"Mark 9:44", "mottatt lesemåte Mark 9:44 (NKJV)"),
                         (r"1 John 1:9", "1 Joh 1:9")]:
      sjekk(bool(re.search(mønster, md)), f"hele boka: {tekst}")
deler = re.split(r"^## Day ", md, flags=re.M)[1:]
med = [int(x.split(":")[0]) for x in deler if "**Today's Action:**" in x]
finnes = [n for n in range(1, 41) if STEDER[f"Day {n}"]]
sjekk(len(med) == len(finnes) and (len(finnes) == 40 or not HEL), f"{len(med)} av {len(finnes)} dager har «Today's Action»")
fdager = [n for n in (8, 16, 24, 32, 40) if n in finnes]
fase = [n for n in fdager if "**Phase Check:**" in dag(n)]
sjekk(len(fase) == len(fdager), f"fasesjekk på {fdager} ({len(fase)} av {len(fdager)})")
terapi = [f for f in ("self-care", "your truth", "inner child", "trauma response", "triggered", "safe space", "toxic masculinity") if f in md.lower()]
sjekk(not terapi, "ingen terapifraser" + ("" if not terapi else f": {', '.join(terapi)}"))
for f in ("makes your life fit together", "pulled off course"):
    sjekk(f not in md, f"ikke «{f}»")
sjekk(not any(c in md for c in (chr(0x2014), chr(0x2015))), "ingen lange tankestreker")
sjekk(not re.search(" " + chr(0x2013) + " ", md) and not re.search(r"[A-Za-z]" + chr(0x2013) + r"[A-Za-z]", md), "ingen korte tankestreker i prosa")
print("RESULTAT:", "alt står" if not feil else f"{len(feil)} mangler")
sys.exit(1 if feil else 0)
