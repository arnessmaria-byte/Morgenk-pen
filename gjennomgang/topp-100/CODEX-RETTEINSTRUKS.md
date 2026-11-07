# Instruks til Codex: gå gjennom funnene og rett hoveddokumentet

## Oppdraget

Gå gjennom alle 113 funnene i `CODEX-RAPPORT.md` og `CODEX-RAPPORT.json`, ett for ett. Behandle de 19 kritiske funnene først. Kontroller hvert funn mot hoveddokumentet og mot kilden. Rett hoveddokumentet der belegget holder. Før en kort logg per funn-ID. Hold faglige uenigheter adskilt fra faktafeil.

Du skrev funnene selv. Behandle dem likevel som om en annen hadde skrevet dem. Et funn er ikke riktig fordi det står i rapporten; det er riktig hvis belegget holder ved ny kontroll.

## Filer (mappen `gjennomgang/topp-100/`)

| Fil | Hva du gjør med den |
|---|---|
| `Topp-100-Bibelen-og-tidligste-kirke.md` | Hoveddokumentet. Det er dette du retter. |
| `CODEX-RAPPORT.md` og `CODEX-RAPPORT.json` | Funnene du skal gå gjennom. |
| `kilder/mantelen/*.txt` | Fasit for alt dokumentet sier om Guds Sanne Menighet og Mantelen. |
| `rangering.py` | Poengsummene bak rangeringen. Endres bare hvis et funn krever det. |
| `forrige-versjon-ortodoks-vekting.md` | Bare til kontroll av merkene «Endret» og «Uendret». Skal ikke rettes. |
| `CODEX-PROMPT.md` | Det opprinnelige oppdraget. Skal ikke endres. |

Lag en sikkerhetskopi før du endrer noe: `Topp-100-Bibelen-og-tidligste-kirke.før-retting.md`.

## Rekkefølge

1. Kritiske funn (19)
2. Vesentlige funn
3. Mindre funn
4. Uenigheter

Innenfor hver gruppe følger du ID-rekkefølgen. Retter et tidligere funn noe som et senere funn også gjelder, logger du det senere funnet som ALLEREDE RETTET.

## Slik behandler du hvert funn

1. **Finn stedet i hoveddokumentet.** Sitér ordlyden slik den står nå. Finnes ikke påstanden, eller er den annerledes enn rapporten sier, logger du funnet som AVVIST, med grunnen.
2. **Kontroller belegget på nytt:**
   - Henvisninger til kirkefedre, konsiler, kanoner, bekjennelsesskrifter og håndskrifter kontrollerer du mot primærkilden i en navngitt utgave eller standardoversettelse.
   - Hvis rapporten bare bygde på en sekundærkilde, prøver du å finne primærkilden.
   - Påstander om Guds Sanne Menighet og Mantelen kontrollerer du ordrett mot `kilder/mantelen/`.
3. **Avgjør utfallet** med én av disse kodene:
   - **RETTET:** belegget holder, og dokumentet er endret.
   - **DELVIS RETTET:** en del av funnet holder.
   - **AVVIST:** belegget holder ikke, eller dokumentet sier ikke det funnet påstår.
   - **UAVKLART:** du fikk ikke kontrollert belegget, eller retting krever et faglig skjønn som ikke er ditt. Skriv det åpne spørsmålet presist.
   - **ALLEREDE RETTET** eller **DUPLIKAT:** vis til ID-en.
4. **Rett minimalt.** Endre bare det belegget dekker:
   - Behold forfatterens stemme og oppsett.
   - Legg ikke inn nye påstander uten kilde.
   - Kan du ikke bekrefte en påstand, skal den gjøres svakere eller tas ut, ikke erstattes med en ny påstand du ikke har kontrollert.

## Faktafeil og faglige uenigheter

Dette skillet er det viktigste i oppdraget.

- **Faktafeil** (type FEIL) og **tydelige mangler** rettes når belegget holder. Det gjelder feil kildehenvisning, feil årstall, feil sitat, feil gjengivelse av en person og en bibelhenvisning som ikke sier det den brukes til.
- **Svakheter** (type SVAKHET) rettes når de kan rettes med bedre ordlyd, en presisering eller en lavere sikkerhetsgrad. Posisjonen skal ikke endres for det.
- **Faglige uenigheter** (type UENIGHET) endrer ikke dokumentets posisjoner. Logg dem, og vurder kort om dokumentets egne kriterier taler for endring. Kriteriene er Skriften 45 %, den tidligste kirken 30 % og logikk 25 %. Mener du det, merker du funnet UAVKLART og skriver hvorfor. Posisjonen avgjør Claude.
- **Et funn som påviser at dokumentet bryter sine egne kriterier,** for eksempel at den tidligste kirken avgjør i ett spørsmål og overstyres i et annet uten grunn, er en SVAKHET, ikke en uenighet. Rett den ved å begrunne forskjellen eller justere sikkerheten. Krever retting at en posisjon endres, merker du funnet UAVKLART.

## Når en retting får følger andre steder

Endrer en retting posisjon, sikkerhet eller poeng, må du oppdatere alt som henger sammen med den:

1. **Selve oppføringen:** teksten, linjen «*Sikkerhet: ...*» og merket «Endret» eller «Uendret» sammenlignet med `forrige-versjon-ortodoks-vekting.md`.
2. **Delen om Guds Sanne Menighet og Mantelen,** hvis det berørte spørsmålet omtales der.
3. **Rangeringen,** hvis poeng endres:
   - Oppdater `rangering.py`, og kjør `python3 rangering.py`.
   - Sorter oppføringene i dokumentet etter den nye rekkefølgen, og nummerer dem fortløpende fra 1 til 102.
   - Oppdater poengtabellen bakerst.
   - Oppdater alle henvisninger av typen «se nr. 6» eller «nr. 6 og 67».
   - Oppdater kapitteloverskriftene (1-12, 13-30 osv.) og avsnittet «Utenfor topp 100».
4. **Innledningen,** hvis vektingen eller metoden beskrives annerledes enn før.

## Regler for dokumentet

- **Språk:** norsk bokmål og samme stil som dokumentet.
- **Bibelhenvisninger:** formen «Rom 3,21-28», med komma mellom kapittel og vers og bindestrek mellom versene.
- **Tankestrek:** tegnene U+2013, U+2014 og U+2015 skal ikke forekomme. Bruk komma, kolon, parentes eller vanlig bindestrek.
- **Personopplysninger:** ikke legg til noe om Elias Solbak Årnes, Maria Solbak Årnes eller andre utover det som allerede står.
- **Andre filer:** ikke endre `kilder/`, `CODEX-PROMPT.md`, `forrige-versjon-ortodoks-vekting.md` eller rapportfilene.

## Hva du skal levere (i samme mappe)

1. **`Topp-100-Bibelen-og-tidligste-kirke.md`,** rettet.
2. **`Topp-100-Bibelen-og-tidligste-kirke.før-retting.md`,** sikkerhetskopien.
3. **`RETTELOGG.md`,** på norsk, bygd opp slik:
   - **Sammendrag:** antall funn per utfall og alvorlighet, og de viktigste endringene i ti linjer eller færre.
   - **Del A, Faktafeil:** alle funn av type FEIL.
   - **Del B, Svakheter og mangler:** alle funn av type SVAKHET og MANGEL.
   - **Del C, Faglige uenigheter:** alle funn av type UENIGHET.
   - **Del D, Til Claude:** alle UAVKLART-funn samlet, med det åpne spørsmålet formulert slik at Claude kan svare ja eller nei, eller velge mellom alternativer.
   - **Del E, Kontroller:** se nederst.

   Hver logglinje skal ha dette formatet:

   ```
   K-001 · Kritisk · FEIL · RETTET
   Sted: nr. 3 Rettferdiggjørelsen
   Før: «...»
   Etter: «...»
   Begrunnelse: én til tre setninger, med belegg (verk, kapittel, utgave eller fil i kilder/).
   ```

   For funn som er AVVIST eller UAVKLART, utelater du «Etter» og skriver hvorfor.
4. **`RETTELOGG.json`:** én post per funn, med feltene `id`, `alvorlighet`, `type`, `utfall`, `nr`, `for`, `etter`, `begrunnelse`, `belegg`, `apent_sporsmal`.
5. **`rangering.py`,** bare hvis poeng er endret. Hver endrede poengsum skal ha en kommentar med funn-ID.

## Kontroller du skal kjøre til slutt (føres i del E)

1. Utskriften fra `python3 rangering.py` stemmer med rekkefølgen og poengtabellen i dokumentet.
2. Dokumentet har nøyaktig 102 nummererte oppføringer, fortløpende fra 1 til 102.
3. Alle henvisninger av typen «nr. X» peker til riktig spørsmål.
4. Alle ordrette sitater fra Mantelen finnes ordrett i `kilder/mantelen/` eller i de to utdragene i `CODEX-PROMPT.md`.
5. Dokumentet inneholder ingen U+2013, U+2014 eller U+2015.
6. Alle 113 funn-ID-er fra `CODEX-RAPPORT.json` finnes i `RETTELOGG.json`, og ingen er glemt.

## Hvis du bruker git

Commit endringene på en egen gren, for eksempel `codex/topp-100-retting`, og ikke på `main`. Bruk én commit per alvorlighetsgruppe, slik at endringene kan følges.
