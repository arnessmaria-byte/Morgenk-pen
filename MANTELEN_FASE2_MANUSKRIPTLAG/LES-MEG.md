# MANTELEN fase 2: manuskriptlaget, Trinn 0

Egen forskningsmappe for det dokumentariske manuskriptlaget. Ingen fil i låst R10/R11.1 ligger her, og ingen er endret. Laget leser R10 og viser hvor R10 står i forhold til vitnene.

Status 25. november 2026: registre, skjema og ti pilotenheter er bygd som **utkast**. Validatoren består. Enhetene er ikke låst.

## Innhold

| Sti | Hva |
|---|---|
| `registre/kildelisenser.json` | Captains skriftlige godkjenning av intern forskning, med bruksgrense per kilde. Ingen publisering. |
| `registre/vitneregister.json` | 69 oppslag: håndskrifter, ruller, oversettelser og fedreverk. Datering står bare her. |
| `registre/schema-manuscript-layer.json` | JSON Schema for variantenhetene. |
| `registre/r10-laas.json` | SHA-256 for de ni R10-bøkene og seks R11-ordlagene ankrene bygger på. |
| `piloter/trinn0-10-piloter.json` | De ti pilotenhetene. |
| `piloter/RAPPORT_TRINN0_10_PILOTER.md` | Lesbar rapport med de ti manuskriptkortene. |
| `piloter/manuskriptkort-prototype.html` | Prototype av kortvisningen. Åpnes i nettleser. |
| `piloter/VALIDERING_TRINN0.txt` | Siste utskrift fra validatoren. |
| `kilder/belegg/` | Utdrag av kildene med URL, revisjon og SHA-256. Hver bekreftelse i pilotfilen viser hit. |
| `validate_trinn0.py` | Validatoren. |
| `verktoy/` | Skriptene som hentet beleggene og bygde filene. |

## Kjøre validatoren

Krever Python 3.9 eller nyere og pakken `jsonschema`.

```bash
python validate_trinn0.py --r10-dir "<mappe med låst R10, den som har assets/data>"
```

Uten lokal R10-mappe kan validatoren lese de ni bokfilene fra www.mantelen.no:

```bash
python validate_trinn0.py --fetch
```

Den avslutter med 0 bare når skjema, ordanker, sigla, dateringsregel, belegg og vitnemønster består.

## Bygge på nytt

Bruk alltid en separat arbeidskopi. De opprinnelige byggeskriptene nedenfor gjenskaper førsteutkastet, ikke de kildekorrigerte kortene. Etter bygging av pilotene: bruk `migrer_origenes.py` med original pilot som inngang og en isolert lokal utmappe. Legg resultatets pilotfil og Koetschau-utdrag i arbeidskopien. Kjør så `verktoy/oppdater_katalog.py <arbeidskopien>` med vedleggene i `kilder/katalogkontroll/`, kjør validatoren, og lag rapporten på nytt. Behold kildegrunnlaget og de eldre kvitteringene. `SHA256SUMS.txt` gjelder gjeldende leveranse.

```bash
python verktoy/bygg_registre.py .
```

```bash
python verktoy/bygg_piloter.py . "<mappe med låst R10>"
```

```bash
python verktoy/rapport.py . piloter/VALIDERING_TRINN0.txt
```

`verktoy/hent_belegg.py` viser hvordan beleggene ble hentet. Det trenger rådataene som er listet i `kilder/belegg/proveniens.json`.

## Regel null

Se status på den enkelte opplysningen: maskinavlest utgave, transkripsjon, oversettelse, sekundærangivelse eller uavlest. Origenes II.4 og II.71 er sjekket i Koetschaus greske utgave. Ved II.71 avviker den engelske oversettelsen fra gresk. Katalogdato og paleografisk anslag må heller ikke blandes. Ingen pilot har to uavhengige menneskelige registreringer.

## Kjente begrensninger

- Vitner er lest i transkripsjon, ikke på bilde.
- NA28, THGNT, SBLGNT, Westcott–Hort og Tregelles er ført etter frie datasett, ikke etter utgavene selv.
- Qumran-transkripsjonene (ETCBC/dss) er CC BY-NC og er bare brukt til kontroll.
- Den digitale Swete-teksten har OCR-tap i 5 Mos 32:43.
- Dobbel registrering er ikke kjørt, og ingen vurdering i akse 3 er satt.
