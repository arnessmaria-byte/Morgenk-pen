# Slop-revisjon: FORGED, hele boken (runde 4)

**Original:** Forged_v5_7_Manuscript.docx med ESV-rettelsene fra 5x8.1-PDF-en · **Redigert:** `manus/FORGED_manus.md` · **Dato:** 2026-10-18

To maskinelle sperrer er kjørt. Ezra `slop_scan.py --gate` måler forbudte ord, tankestreker, trikolon og retoriske spørsmål. `antitese_scan.py` er laget for denne boken og teller de engelske mønstrene forfatteren pekte på i margen, med grense per dag.

## Sperrende mål, før og etter

| Mål | Før | Etter | Grense |
|---|---|---|---|
| Harde treff (forbudte ord og fraser) | 0 | 0 | 0 |
| Tankestreker i brødtekst | 143 (8,9 per 1000 ord) | 0 | ≤ 2,5 per 1000 ord |
| Retorisk spørsmål med svar | 1 | 0 | 0 |
| Trikolon | 3 | 1 | ≤ 2 |
| **Ezra-sperren, exit-kode** | **1** | **0** | 0 |

## Forfatterens mønster: «not X. It is Y.» og slektninger

| Mønster | Før | Etter | Grense |
|---|---|---|---|
| To-setnings-antitese («X is not A. It is B.») | 131 | 19 | maks 1 per dag |
| «not X, but Y» | 40 | 0 | maks 1 per dag |
| «This day is not about …» | 39 | 0 | 0 |
| «You are not X. You are Y.» | 17 | 0 | 0 |
| «not because …» | 18 | 0 | 0 |
| Fragment som starter med «Not …» | 25 | 1 | |
| «X does not Y. It Z.» | 48 | 15 | |
| Signalfraser («Let me say», «And one more thing», «Here is what») | 15 | 0 | 0 |
| «This is different / This is not that» | 4 | 0 | 0 |
| «The question is …» | 3 | 0 | 0 |
| «For some men» (åpning på Healing Forge) | 38 | 6 | ≤ 8 i boken |
| «quietly» | 46 | 30 | ≤ 30 i boken |
| **Sperrende brudd totalt** | **134** | **0** | 0 |

Begge kolonnene er talt med unntakslisten (se under). Uten den blir tallene 132, 18 og 136 før, og 20, 1 og 1 etter. Ezra-skriptets rå tankestrekmål (49,8 per 1000 ord før) teller også skillelinjene i tabellene. Tallet over gjelder bare tankestreker i løpende tekst.

De 19 antitesene som står igjen, er bærende: én per dag på det meste, og bare der kontrasten er dagens tese. Ett bevisst unntak er ført i `verktoy/antitese_unntak.txt`: «You are not measured by momentum. You are formed by faithfulness.» Det er bokens nøkkelsetning, og den står ordrett.

Telleren ble også kjørt på redaktørens egne nye formuleringer underveis. Tre nye maler ble fanget og tynnet ut: «Today is about» (40 til 8), «may once have» (15 til 4) og «more than» (33 til omkring 15).

## Rådgivende mål

| Mål | Før | Etter | Mål | Kommentar |
|---|---|---|---|---|
| LIX | 37,5 | 34,0 | 40–50 | Riktig for målgruppen. Korte slag er forfatterens stemme, og leserne er 17–22 år. Ingen leddsetninger er lagt til for å løfte tallet. |
| Adverb per 1000 ord | 17,5 | 12,1 | ≤ 12 | Resten skyldes for en stor del overskriften «What This Day Is Really About», som står 40 ganger og er bokens faste form. |
| Passiv per 1000 ord | 9,4 | 7,0 | | |
| Setningslengde, snitt | 8,9 | 10,1 | | Flere korte setninger er slått sammen. |
| Metronom-kjeder (fire like korte setninger på rad) | 84 | 43 | | Rytmen er brutt opp der kjedene var mekaniske. Kjedene som står, er forfatterens slag i Healing Forge og scenariene. |
| Gjentatt frase «this day is not about» | 39 | 0 | | |

## Ord til kontroll, ikke feil

- «leverage» (Day 19) og «optimize» (Day 26) står i originalen og brukes i sin vanlige betydning. Beholdt.

## Sluttlesernes funn om mønstre

Sluttleseren fant at fem Healing Forge-avslutninger brukte samme formel, «You are not being X; you are being Y.» To er kortet (Day 12 og Day 40). Day 38 er beholdt. Day 39 slutter nå med én positiv setning, «You are being trained to be trusted.», uten kontrastleddet, og er beholdt. Day 30 er endret etter forfatterens avgjørelse 18.10.2026: «His silence is not neglect. He has not let go of you.»

## Uavklarte

Ingen. Begge sperrene står på null.
