# MANTELEN: felles prosjektinstruks for alle AI-er

Redaksjonsordre fra ansvarlig redaktør Elias Solbak Årnes, 25. november 2026.
Gjelder MANTELENs journalistikk, kildekorrespondanse og YouTube-produksjon, og
gjelder Cursor, Codex, Claude, Grok Bot og alle andre modeller og bakgrunnsjobber.
Ordren går foran eldre instrukser der de strider mot den.

## 1. Vis leseren hvem som sier hva

- Gjengi en kildes beskrivelser og idealer som kildens. Redaksjonen overtar dem ikke.
- Bevar kildenes ordlyd og rekkefølgen utsagnene kom i. Når en kilde har sagt
  ulike ting på ulike steder, skal leseren kunne se forskjellen. Slå dem ikke sammen.
- Gjengi en presisering med kildens egne ord. La den enkeltes motiv for sin tro stå åpent.
- Hold tre spørsmål fra hverandre: hva en kilde mener politisk (hvem som kan bo
  i et land, hvilke religioner staten skal tillate), hva som gjelder religiøs tro,
  og hva Skriften sier. Det siste er bibeltolkning, og da er punkt 2 i kraft.

## 2. Egen teologisk vurdering krever redaktørens ja til den ferdige versjonen

Ansvarlig redaktør skal uttrykkelig godkjenne den ferdige versjonen før MANTELEN
publiserer noen form for egen teologisk vurdering. Det er innholdet som avgjør,
også når overskriften «MANTELENs teologiske vurdering» mangler. Regelen gjelder:

- egne saker og blandingssaker
- bibeltolkning i en ingress
- et spørsmål som forutsetter redaksjonens teologiske svar
- en konklusjon i en tittel, bildetekst, et videomanus, en fortellerstemme, et
  skjermbilde, en undertekst, en beskrivelse eller en Shorts-video

En navngitt kildes teologiske utsagn kan gjengis som journalistikk når leseren
tydelig ser hvem som hevder det. Bibelens forfattere er ikke kilder i denne
forstand: bruker teksten Paulus til å si noe om frelse, tolker MANTELEN Skriften.

Slik legges en vurdering frem:

1. Legg frem den nøyaktige teksten eller den ferdige videoversjonen.
2. Hent gjeldende versjon av hovedfilen for Guds Menighets Topp 100-liste ved
   behandlingen, og noter versjonen i saken.
3. Oppgi hvilke punkter vurderingen bygger på, hva punktene faktisk behandler,
   og vis kort hvordan vurderingen samsvarer med dem.
4. Går spørsmålet utover det listen avgjør, legges det åpent frem.

Samtykke til listen, til en tidligere sak eller til en serie gir ingen
godkjenning av et nytt resonnement. Endres den teologiske ordlyden etter
godkjenning, skal den nye versjonen forelegges på nytt. En publisert sak med
teologisk vurdering endres ikke før redaktøren har tatt stilling til et forelagt
endringsutkast.

## 3. Marias journalistikk og e-post

- En faktabasert artikkel som Maria Solbak Årnes faktisk har skrevet, og som er
  fri for MANTELENs egne teologiske vurderinger, følger ordinær publiseringsvei
  uten redaktørens involvering.
- Synlig byline: «Av Maria Solbak Årnes, journalist i MANTELEN». Forfatter i Ghost: Maria.
- Kildekorrespondanse, også fra fellesadressen: avsendernavn «Maria Solbak Årnes,
  MANTELEN», signatur «Maria Solbak Årnes, journalist i MANTELEN». Gjelder første
  forespørsel, oppfølgingsspørsmål og melding etter publisering.
- «Redaksjonen» alene er utilstrekkelig for Marias saker.
- Hennes navn brukes bare når hun faktisk er journalist eller avsender. En AI
  kan ikke tildele henne forfatterskap, signere som henne på eget initiativ
  eller få en sak gjennom ved å bytte byline.
- Legger en AI til en teologisk vurdering i hennes tekst, skal hele den
  aktuelle versjonen til ansvarlig redaktør.
- Navneregelen for e-post gir ingen ny sendefullmakt.

## 4. Porten i produksjonen

`redaksjonsport/port.py` kontrollerer den endelige kanalversjonen. Se
`redaksjonsport/README.md` for saksformat, kommandoer og innkobling.

- Kjør kontrollen både ved planlegging og rett før noe går ut. Dette gjelder
  også direktekall mot Ghost, YouTube og e-post, arbeid i nettleser,
  bakgrunnsjobber og saker og videoer som allerede er planlagt.
- Svarer porten `HOLDES`, eller kan den ikke kjøres, blir innholdet liggende
  som utkast. Teologisk eller uavklart innhold holdes i utkast når redaktørens
  godkjenning mangler.
- En AI skal aldri fylle ut, signere, kopiere eller gjenbruke en godkjenning på
  redaktørens vegne, og aldri røre nøklene porten stoler på. Det samme gjelder
  Marias bekreftelse av eget forfatterskap.
- Innholdsskjermen i porten er et gulv. At den ikke slår ut, er ingen
  godkjenning. Skriv aldri om en tekst for å komme forbi den.
- Ingen test skal sende e-post eller publisere stoff til publikum.

Er du i tvil om noe er egen teologisk vurdering: hold det i utkast og spør redaktøren.
