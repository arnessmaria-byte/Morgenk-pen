# KDP-sjekkliste: FORGED, pocket (paperback) og Kindle

**Dato:** 2026-10-18 · **Hovedfil:** `ut/FORGED_Interior_6x9_KDP.pdf` · **E-bok:** `ut/FORGED_Kindle.epub`

**Dom: klar med navngitte rettelser.** Innmaten og e-boken består alle tekniske kontroller. Før opplasting må tre ting være på plass: Sverre Johannes' godkjenning av forordet, forfatterens avgjørelse om fem teologiske formuleringer og omslaget.

## Utgivelsesfakta (forslag, forfatteren bekrefter)

| Felt | Verdi |
|---|---|
| Format | Paperback 6 × 9 tommer, svart-hvitt innmat, uten utfallende sider (no bleed) |
| Alternativ | 5 × 8 tommer: `ut/FORGED_Interior_5x8_KDP.pdf`, 122 sider |
| Sidetall | 118 (6 × 9), partall, siste side tom |
| Papir | Hvitt eller krem: forfatterens valg. De to første bøkene avgjør. |
| ISBN | KDP-tildelt gratis ISBN, eller eget. Copyright-siden har ingen ISBN-linje i dag. |
| Tittel | Forged |
| Undertittel | A 40-Day Path to Durable Faith for Young Men |
| Forfatter | Elias Solbak Årnes |
| Bidragsyter | Sverre Johannes Langeland (Foreword) |

## Innmat (PDF), kontrollert maskinelt

| Punkt | Krav | Målt | OK |
|---|---|---|---|
| Sidestørrelse | 6,00 × 9,00 in | 6,00 × 9,00 in, alle sider | Ja |
| Indre marg | ≥ 0,375 in (24–150 sider) | 0,739 in | Ja |
| Ytre marg | ≥ 0,25 in | 0,659 in | Ja |
| Topp / bunn | ≥ 0,25 in | 0,377 / 0,429 in (topptekst og folio) | Ja |
| Fonter innebygd | Alle | EB Garamond Regular, Italic, Bold, alle som delsett | Ja |
| Annotasjoner, lenker, skjemafelt | Ingen | 0 | Ja |
| Faser og hovedseksjoner starter på høyreside | Ja | Alle fem faser, forord, introduksjon, Conclusion, vedlegg. Hver dag starter øverst på ny side, som i de to første bøkene. | Ja |
| Tomme sider uten topptekst og folio | Ja | 10 tomme sider, alle rene | Ja |
| Innholdsliste mot faktiske sider | 50 av 50 | 50 av 50 | Ja |
| Siste side | Ingen feil | «About the Author» på s. 117, tom s. 118 | Ja |
| Metadata | Tittel og forfatter | «Forged: A 40-Day Path…», «Elias Solbak Årnes» | Ja |

Den samme kontrollen er kjørt på 5 × 8-filen: indre marg 0,662 in, ytre 0,492 in, topp 0,328 in, bunn 0,383 in, innholdsliste 50 av 50.

## Omslag (må lages)

Omslaget kan først lages når papirtypen er valgt, fordi ryggbredden avhenger av den. Tallene under gjelder 6 × 9 med 118 sider. Bruk KDPs omslagsmal-generator med det endelige sidetallet for å få eksakte mål.

| Papir | Ryggbredde | Omslag med 0,125 in utfall |
|---|---|---|
| Hvitt | 118 × 0,002252 = 0,266 in | 12,516 × 9,25 in |
| Krem | 118 × 0,0025 = 0,295 in | 12,545 × 9,25 in |

Ryggtekst: KDP tillater tekst på ryggen fra 79 sider, så det går. Med en så smal rygg bør teksten være liten og ha god klaring.

## E-bok (EPUB)

| Punkt | Resultat |
|---|---|
| EPUBCheck 5.1.0 | 0 feil, 0 advarsler |
| Innholdsliste (navigasjon) | Alle dager, faser, forord, vedlegg |
| Fonter | EB Garamond innebygd (lesebrettet kan overstyre) |
| Filstørrelse | 1,0 MB |

## Pris og royalty (regneeksempel)

Satsene er KDPs gjeldende satser slik vi kjenner dem (US-markedet). Bekreft dem i KDP på opplastingsdagen, fordi de endres.

**Pocket, 118 sider, svart-hvitt:** trykkostnad = 1,00 USD + 118 × 0,012 USD = **2,42 USD**.
Royalty er 60 % av listeprisen fra 9,99 USD og oppover, og 50 % under 9,99 USD. Trykkostnaden trekkes fra.

| Listepris | Sats | Regnestykke | Per bok |
|---|---|---|---|
| 14,99 USD | 60 % | 8,99 − 2,42 | 6,58 USD |
| 12,99 USD | 60 % | 7,79 − 2,42 | 5,38 USD |
| 9,99 USD | 60 % | 5,99 − 2,42 | 3,58 USD |
| 8,99 USD | 50 % | 4,50 − 2,42 | 2,08 USD |

**Kindle:** 70 % royalty gjelder for priser fra 2,99 til 9,99 USD, minus leveringskostnad på omtrent 0,15 USD per MB.

| Listepris | Regnestykke | Per bok |
|---|---|---|
| 4,99 USD | 0,70 × (4,99 − 0,15) | 3,39 USD |
| 6,99 USD | 0,70 × (6,99 − 0,15) | 4,79 USD |

## Før opplasting

- [x] Forordet står uendret, også Hammarskjöld-sitatet (forfatterens beslutning 18.10.2026)
- [ ] Sverre Johannes har godkjent den engelske teksten til forordet (tiltak 6)
- [ ] Sluttleserens teologiske merknader avgjort (tiltak 11)
- [x] «sexuality» strøket fra OBSERVE-listen (tiltak 12)
- [ ] Papirtype valgt, og omslaget laget med KDPs mal for 118 sider
- [ ] ISBN valgt. Med eget ISBN legges linjen inn i `verktoy/sett_bok.py`, og PDF-en bygges på nytt.
- [ ] Beskrivelse, sju søkeord og kategorier skrevet (ikke en del av denne runden)
- [ ] KDP-forhåndsvisningen lest side for side, også siste side
- [ ] Pris satt og royalty kontrollert i KDP
- [ ] Lenken til MantleOfElias i forfatteromtalen testet

Ingenting er lastet opp. Forfatteren publiserer selv.
