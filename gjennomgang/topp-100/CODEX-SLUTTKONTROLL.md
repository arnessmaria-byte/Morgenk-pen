# Instruks til Codex: sluttkontroll av topp 100 via fellesområdet på Google Drive

## Fellesområdet

Fra nå av utveksler Claude og Codex filer gjennom en felles mappe på Google Drive, ikke gjennom Captain:

**`BIBELOVERSETTELSE/gjennomgang/topp-100/`**
<https://drive.google.com/drive/folders/1UnWAgbFbPzu1dGwCKjvIaGgzn67PeLZ3>

| Mappe eller fil | Innhold | Hvem skriver |
|---|---|---|
| `STATUS.md` | Hvem venter på hvem. Én linje per overlevering, nyeste øverst. | Alle |
| `pakke/` | Den endelige versjonen: `Topp-100-Bibelen-og-tidligste-kirke.md`, `CLAUDE-AVGJORELSER.md`, `rangering.py` og denne instruksen | Bare Claude |
| `fra-codex/` | Codex' leveranser, én undermappe per runde (`runde-1/`, `runde-2/` ...) | Bare Codex |
| `fra-claude/` | Claudes svar på Codex' leveranser | Bare Claude |

Disse filene er uendret fra forrige runde, og du har dem allerede lokalt i `gjennomgang\topp-100\` fra ZIP-pakken. Bruk dem derfra:
- `CODEX-PROMPT.md`
- `CODEX-RETTEINSTRUKS.md`
- `forrige-versjon-ortodoks-vekting.md`
- `kilder/mantelen/*.txt`

Har du ikke skrivetilgang til Drive, skriver du leveransene lokalt i `gjennomgang\topp-100\runde-2\`. Be Captain laste dem opp til `fra-codex/runde-2/` og legge inn statuslinjen.

## Steg 1: legg inn forrige runde

Last opp disse fire filene fra forrige runde til `fra-codex/runde-1/`, uendret:
- `CODEX-RAPPORT.md`
- `CODEX-RAPPORT.json`
- `RETTELOGG.md`
- `RETTELOGG.json`

Claude har bare sett teksten Captain limte inn, ikke selve filene.

## Steg 2: ta inn den endelige versjonen

1. Gi din lokale versjon av hoveddokumentet nytt navn: `Topp-100-Bibelen-og-tidligste-kirke.codex-runde-1.md`.
2. Hent `Topp-100-Bibelen-og-tidligste-kirke.md`, `CLAUDE-AVGJORELSER.md` og `rangering.py` fra `pakke/`.

## Steg 3: sluttkontrollen

Du skal kontrollere Claudes endringer etter din runde. Du skal ikke endre hoveddokumentet. Du skal bare rapportere.

Codex ser etter feil i Claudes arbeid. Claude ser etter feil i Codex' arbeid. Ingen av dere har siste ord fordi de skrev sist.

### A. Claudes sju korreksjoner av dine rettelser

Se tabellen i `CLAUDE-AVGJORELSER.md` del 1. Gi hver korreksjon ett av disse utfallene: STØTTET, DELVIS STØTTET, AVVIST eller UAVKLART. Begrunn utfallet med belegg.

Kontroller disse henvisningene mot primærkilden:
- **K-025:** Justin, *1 Apol.* 27, og Tertullian, *Om kyskhet* (*De pudicitia*) 4. Stemmer det at Tertullian utelukker lyster «mot både kropper og kjønn»? Stemmer det at Justin, *Dial.* 95, ikke handler om seksualetikk?
- **K-040:**
  - Irenaeus, *Mot kjetterne* I.13.2: Markus og kvinner ved nattverden.
  - Tertullian, *Om kjetternes forskrivning* 41.
  - Firmilians brev til Kyprian om profetinnen i Kappadokia: brev 75,10 i Hartels nummerering, 74 i ANF. Oppgi nummereringen du bruker.
  - Innskrifter med tittelen *presbytera*.
  - Gelasius' brev fra 494 om kvinner ved alteret i Sør-Italia: brevnummer og kapittel.
  - Holder påstanden «før 325 bare kjent fra grupper og tilfeller kirken avviste» mot det du finner?
- **K-092:** Holder påstanden om at slaveriet aldri begrunnes i skapelsen? Kontroller husordningene, blant annet Ef 6,5-9, Kol 3,22-4,1 og 1 Pet 2,18-25.
- **K-057:**
  - Tertullian, *Om engifte* 8: sier han at Maria levde i ekteskap etter fødselen?
  - Origenes, *Matteuskommentaren* X.17: protoevangeliet og Jesu brødre.
  - *Jakobs protoevangelium* 9: Josef som enkemann med sønner.
- **K-048:** Står «fra unnfangelse til død» i *Fundamentet* 9 på mantelen.no?
- **K-021:** Viser innslaget «Våre argumenter må også tåle kontroll» på mantelen.no til Westminsterbekjennelsen kap. 1, punkt 6 og 9?
- **K-088:** Den katolske kirkes katekisme 1367: står uttrykket «sant soningsoffer» («truly propitiatory») der?
- **Nr. 1:** Gir «enten muntlig eller ved brev» en riktig gjengivelse av 2 Tess 2,15?

### B. Claudes avgjørelser i de 15 åpne punktene

Se `CLAUDE-AVGJORELSER.md` del 2. Kontroller tre ting:
1. Er hver avgjørelse i samsvar med definisjonene av S, D, A og U som nå står i metodedelen, og er regelen mot dobbelttelling brukt likt overalt? Pek ut steder der regelen skulle ha gitt et annet utfall.
2. Er de nye tekstene i nr. 13 (begrenset forsoning), nr. 51 (selvmord og gravferd), nr. 54 (ledere og overgrep) og nr. 56 (motargumentet fra CA XXI) korrekte og belagt? Er sikkerhetsgraden rimelig?
3. Stemmer endringen av D fra 6 til 7 for Nådegavene, og står den riktig i `rangering.py` og i tabellen?

### C. Regresjoner

Sammenlign `Topp-100-Bibelen-og-tidligste-kirke.codex-runde-1.md` med den nye versjonen fra `pakke/`. Lag en liste over alle forskjeller som ikke står i `CLAUDE-AVGJORELSER.md`. Vurder hver av dem: er den en bevisst redaksjonell endring, eller har en av dine 98 rettelser gått tapt eller blitt endret utilsiktet?

### D. Kontroller

1. `python3 rangering.py` stemmer med rekkefølgen og poengtabellen.
2. Dokumentet har 102 oppføringer, nummerert fortløpende fra 1 til 102.
3. Alle henvisninger av typen «nr. X» peker til riktig spørsmål.
4. Mantelen-sitatene er ordrette.
5. Dokumentet inneholder ingen U+2013, U+2014 eller U+2015.

## Leveranse (i `fra-codex/runde-2/`)

### 1. `SLUTTKONTROLL.md`, på norsk

Filen har seks deler:
1. **Sammendrag** på høyst ti linjer.
2. **Del A:** Claudes sju korreksjoner.
3. **Del B:** De 15 avgjørelsene.
4. **Del C:** Regresjoner.
5. **Del D:** Kontroller.
6. **Del E, Til Claude:** åpne spørsmål, formulert slik at de kan besvares med ja eller nei eller med et valg mellom alternativer.

Hver post har dette formatet:

```
S-001 · K-040 · AVVIST
Sted: nr. 11 Kvinners ordinasjon
Claudes tekst: «...»
Funn: én til tre setninger.
Belegg: verk, kapittel, utgave eller URL, og om det er kontrollert mot primærkilde.
Forslag: konkret ordlyd, eller «ingen endring».
```

### 2. `SLUTTKONTROLL.json`

Én post per funn, med feltene `id`, `gjelder`, `utfall`, `nr`, `claudes_tekst`, `funn`, `belegg`, `kontrollmetode`, `forslag`.

## STATUS.md

Når du er ferdig, legger du øverst i `STATUS.md` en linje i samme form som i MANTELEN-arbeidsindeksen:

```
Venter på Claude: sluttkontroll runde 2; fra-codex/runde-2/SLUTTKONTROLL.md; ÅÅÅÅ-MM-DD.
```

Stopper du fordi noe mangler, skriver du `Venter på Captain:` og hva som mangler.

## Regler

- Ikke endre filene i `pakke/` eller `fra-claude/`.
- Ikke dikt opp kilder. Er du usikker, skriver du UAVKLART og forklarer hvorfor.
- Hold faktafeil og faglige uenigheter adskilt, slik som i forrige runde.
- Skriv på norsk bokmål. Ikke bruk tegnene U+2013, U+2014 eller U+2015.
- Ikke legg til personopplysninger utover det som allerede står i dokumentet.
