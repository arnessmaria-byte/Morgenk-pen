# FORGED: rapport fra skyøkten, mesterordren 22.11.2026

Levert 23.11.2026. MANTELEN_KOMMANDOBRO.md kan ikke redigeres fra skyøkten, derfor står rapporten i denne filen.

## To versjoner av samme ordre

| | Skyøkten | Den lokale økten (Fable og Codex) |
|---|---|---|
| Manus | `FORGED_manus_2026-11-22_skyokt.md` | `FORGED_manus_gjeldende_2026-11-22.md` |
| SHA-256 manus | `51cc706aad96ee4826a5242cd331a63cef44f00a0d62a1548fc1b3723287cf63` | `9d9f8093fc63781121aecf46746558813156842393c63bdd4ed2d862a9eabab6` |
| Trykkfil | `FORGED_Interior_5x8_KDP_2026-11-22_skyokt.pdf` | `FORGED_Interior_5x8_KDP_2026-11-22.pdf` |
| SHA-256 PDF | `cdca3b7a5906c56aec4bc9d9d57b858910b6f73f2ce04da900a2143e867bc503` | `22e2289547a71c713b7e7bf1410d1685cca45daf1a475b0e47c05c02857f2253` |
| Plassering | FORGED-mappen (den opprinnelige) | Drive-roten og den nye FORGED-mappen i roten |
| Google Docs | «FORGED (skyøkt, 22.11.2026)» | ingen |

Skyøkten har ikke endret, flyttet eller kastet filene fra den lokale økten. Utgavene fra 21.11 er beholdt, fordi den lokale økten bruker dem som kilde. Forfatteren velger hvilken versjon som blir grunnlaget.

## Kontroller på skyversjonen

| Kontroll | Resultat |
|---|---|
| Sider | 124 (i-viii og 1-116), 360 × 576 pt, alle fonter innebygd |
| Sidebudsjett | alle 40 dager og alle deler har sitt gamle sidetall; Appendix C på 113, About the Author på 115 |
| Fredet tekst | forordet og About the Author uendret; videosiden på trykt side 5; de fem fredede R8-linjene står |
| QR-kode | leser `https://www.youtube.com/playlist?list=PLSG5mjEhTu-s` |
| Teologisk og praktisk sjekkliste (`sjekk_teologi.py`) | 53 av 53 punkter står |
| R1-R10 (`sjekk_r1_r10.py`) | består; R9 Day 19, 40 og oktoberrettelse nr. 4, 13, 14, 15 og 19 er erstattet etter ordren |
| Bibelsitater | alle kontrollerbare sitater stemmer |
| Ezra-sperren og antitesesperren | 0 sperrende brudd |
| EPUBCheck | 0 feil |
| Tankestreker | 0 U+2014, ingen U+2013 i prosa |
| Copyright-siden | ESV-linje, NKJV-linje for de mottatte lesemåtene, forordslinje |

`forged_apply_r1_r10_v2.py` er ikke kjørt i skyøkten. Ukjente skript fra Drive kjøres ikke der. De to egne kontrollene over dekker det samme. Den lokale økten har kjørt v2-skriptet: exit 1, fordi R4-R7 og deler av R9 er erstattet av ordren.

## Hva ordren har gitt i skyversjonen

- Trosbekjennelsen fra 381, oversatt fra gresk, med «God from God» fra Nikea (325) og uten filioque: innledningen, Day 4, Day 22 og vedlegg B.
- Skriften alene med masoretisk og mottatt tekst (Day 3, 19, vedlegg A). De mottatte lesemåtene 1 Tim 3:16, Apg 8:37, Apg 17:26 og Mark 9:44, 46, 48 er sitert etter NKJV.
- Rettferdiggjørelse, soning og omvendelse (Day 18, 21, Healing Forge), troendes dåp (24), nattverden (30), Åndens gaver (38), skapelsen og Adam (6), renheten og ekteskapet (16), kjønn og det ufødte liv (31).
- Oppgjøret: Jezebels ånd (Day 12, 35, vedlegg C), falske profeter og leiesvenner (27, 33), kvinnelige prester, vigsel av likekjønnede og utstøting av bibeltro prester. Hvert sted har et konkret krav. Tabellene «Apostolic Church vs. Feminized Church» (Day 27) og «Biblical Shepherd vs. Hireling Prophet» (Day 33) er med.
- Ny Today's Action på alle 40 dager, med frist før kl. 22. Fasesjekk på Day 8, 16, 24, 32 og 40.

## Sammenligningen

En uavhengig leser sammenlignet versjonene. Hele rapporten ligger i repoet: `Forged/bok/kilder/m22/sammenligning_sky_lokal_2026-11-23.md`.

Hullene i skyversjonen er rettet 23.11:
- merknad om 325 i vedlegg B
- Mark 9:46 og 48
- Kristus i seks Healing Forge-avsnitt
- menighetsprøve på Day 27

Den lokale versjonen har flere bibelske scener og Kristus i alle Healing Forge-avsnitt. Den har også feil som må rettes før den brukes:
- «order and authority» lagt inn i Gud selv (innledningen)
- 24-timersklokke i en amerikansk bok
- rette apostrofer synlige i PDF-en
- mottatte lesemåter merket «author's translation», med ordlyd lik NKJV
- en påstand om Den norske kirke som er skarpere enn kilden: bispemøtet skriver «ikke teologisk meningstvang» (BM 59/20)

## Åpne avgjørelser for forfatteren

1. Hvilken versjon blir grunnlaget, eller skal det beste fra begge flettes?
2. Forordets forfatter bør se den nye teologiske retningen før trykk.
3. Day 33: scenen med Jordan er en sammensatt illustrasjon. Copyright-siden sier at noen scener er sammensatte. Forfatteren avgjør om det holder.
4. Ingen opplasting til KDP er gjort. Bytt PDF-en i KDP-utkastet først når versjonen er valgt.
