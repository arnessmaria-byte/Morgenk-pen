# Oppdrag: FORGED, full redigering og KDP-klar utgave (runde 4)

Dette er bestillingen slik den ble presisert og utført 18.10.2026. Den kan brukes ordrett igjen, for eksempel på neste bok, med titler og filnavn byttet ut.

## Bestilling

1. **Grunnlag.** Teksten forfatteren leser og kommenterer: `FORGED_5x8.1_Print_Interior_KDP.pdf` (Drive › Forged). Ren tekstkilde: `Forged_v5_7_Manuscript.docx`. Avvik mellom de to kartlegges maskinelt før redigering; PDF-en vinner der den er nyere (her: 15 bibelsitater rettet til ESV).
2. **Alle tilbakemeldinger inn.** Forfatterens PDF-kommentarer og andre leseres kommentarer (her: Maria i Drive-kopien av 5.7) hentes ut med ankertekst. Hver kommentar får et svar: utført, utført på annen måte, eller ikke utført med begrunnelse.
3. **Redigering, hele boken i ett løp.** Ezra-reglene: ingen nye fakta eller detaljer, skriftsitater ordrett, teologiske påstander klargjøres men endres ikke, strukturendringer foreslås og logges. Forfatterens stemme (korte slag i par, konkrete bilder) beholdes.
4. **AI-slop, målt og sperret.** To maskinelle sperrer må passere før levering: Ezra `slop_scan.py --gate` og en egen teller for engelske antiteser og metakommentarer (`antitese_scan.py`), med grenser per dag. Telleren kjøres også på redaktørens egne nye formuleringer, slik at gamle maler ikke byttes mot nye.
5. **Uavhengig kontroll.** Tre kaldlesere som bare ser den redigerte teksten (hver sin tredjedel), én troskapsrevisor som sammenligner original og redigert linje for linje, én skriftkontroll mot ESV på nett, og én sluttleser på hele boken. Funnene rettes i nye runder til sperrene og revisorene er fornøyd.
6. **Typografi som de to første bøkene.** Måles fra trykkfilene til *The Supervised Hours* og *The Foundation of Knowing*: skrift, størrelse, linjeavstand, marger, topptekst, folio, kapittelåpning, innholdsliste. Settes maskinelt fra manusfilen, så rettelser går rett inn i PDF-en.
7. **KDP-kontroll.** Sidestørrelse, innebygde fonter, marger mot KDPs minstekrav, innholdslistens sidetall mot faktiske sider, EPUB mot EPUBCheck, KDP-sjekkliste med royalty-utregning.
8. **Ikke stopp for spørsmål.** Åpne beslutninger tas med en begrunnet standard og føres i beslutningsloggen, slik at forfatteren kan overprøve dem.

## Leveranser

PDF-innmat 6×9 (hovedformat, som de to første bøkene) og 5×8 (alternativ), EPUB for Kindle, rent manus (md og docx), sporede endringer (docx), redaktørrapport, slop-revisjon, endringslogg med dekningskontroll, formliste, kommentarkart, verifiseringsrapport, KDP-sjekkliste, beslutningslogg.

## Runde 5: klarspråk (18.10.2026)

Bestilling: «Det skal være så jordnært, enkelt og lett forståelig som overhodet mulig.» Forordet og bibelsitatene holdes utenfor.

1. **Ett felles kort.** Det inneholder testen for hver setning, ordlisten, faste setninger og blokkerte mønstre (`manus/klarsprak_kort.md`).
2. **Åtte deler parallelt.** Hver del går gjennom omskriving, troskapsrevisor, kaldleser i målgruppen og retting. Maskinell kontroll av struktur, sitater, navn, tall og sperrer skjer etter hvert trinn.
3. **Hele boken samlet.** Den leses med fire linser: konsekvens, leser, teologi og stemme. Så følger retting per fil og en sluttrevisor.
4. **Måling før og etter.** `verktoy/lesbarhet.py` måler abstrakte ord, Flesch, Flesch-Kincaid og setningslengde.
5. **Leveranser.** PDF i 6×9 og 5×8, EPUB, Word i EB Garamond, Markdown, Google Docs og rapporten `12-klarsprak.md`.

