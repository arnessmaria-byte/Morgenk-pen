# Voffgenics: spesifikasjon (den forbedrede prompten)

Opprinnelig bestilling: "Lag et spill som Mewgenics, bare en mikroversjon (MVP) med hunder i stedet for katter, og gjør det spillbart for meg her og nå."

Under er bestillingen skrevet om til noe som kan bygges og etterprøves.

## Mål

Et nettleserspill i én HTML-fil, uten byggesteg og uten server, som fanger kjernen i Mewgenics:
avl med arv og mutasjoner hjemme, taktiske rutenettkamper ute, permanent død, og veteraner som
pensjoneres og blir avlsdyr. Hunder i stedet for katter, katter (og rotter og måker) som fiender.
Spillbart med mus eller touch, på PC og mobil, publisert som Artifact slik at det kan spilles med én gang.

## Kjerneløkke

1. **Kennelen**: se hundene, par en hann og en tispe, adopter gatehunder, send et lag på tur, sov til neste dag.
2. **Natten**: parede hunder får 1-3 valper. Valper kan verken gå på tur eller pare seg før neste dag.
3. **Turen**: velg 1-4 voksne hunder og gi hver et halsbånd (klasse). Gå gjennom 5 steg der du velger
   mellom to noder (kamp, elitekamp, hendelse, hvil), og møt Kattekongen til slutt. Du kan gå hjem når som helst mellom stegene.
4. **Hjemkomst**: overlevende blir veteraner. De kan pare seg, men aldri gå på tur igjen. De døde havner i minnelunden.

## Genetikk

- Seks egenskaper (1-10): Styrke, Smidighet, Utholdenhet, Intelligens, Hurtighet, Flaks.
- Valpen arver hver egenskap fra én av foreldrene (60 % sjanse for den høyeste), med 15 % sjanse for ±1.
- Lærte evner arves: 70 % sjanse for én fra foreldrenes samlede evner, 25 % for en til (maks 2).
- Mutasjoner arves med 50 % hver, og 10 % sjanse for en ny. Maks 3.
- Innavl: søsken, halvsøsken eller forelder og barn gir høy risiko (55 %) for defekt-mutasjon og svekkede
  egenskaper. Søskenbarn gir 20 %. Slektskap regnes ut fra et register som også husker døde hunder.
- Utseende (pelsfarge, mønster, ører, snute, øyne) arves og tegnes prosedyrisk. Mutasjoner synes på portrettet.

## Kamp

- Rutenett 8 x 6 med hindringer. Spillerfase (alle hunder, valgfri rekkefølge), så fiendefase.
- Hver hund kan flytte én gang og så handle én gang. Handling avslutter hundens tur.
- Fem halsbånd: Slåsshund (stormløp), Vokter (skjold og provokasjon), Jakthund (avstand og tilbakeslag),
  Mystiker (magi med områdeskade som også treffer egne), Pleier (helbreder og gjenoppliver).
- Lærbare evner fra nivåøkning: aktive (halespinn, grav tunnel, legg bæsj, rull i gresset, skremmebjeff,
  loppeskyss, dobbeltglefs) og passive (skarpe klør, tykk pels, supersnute, lette poter, seigpining).
- 0 HP betyr at hunden ligger nede. Etter kampen slår nede hunder et overlevelseskast (Flaks hjelper).
  Overlever de, får de et arr (-1 på en egenskap). Feiler de, dør de for godt.
- Fiender: rotte, måke (flyr over hindringer), gatekatt, hvesekatt (avstand), kloakkrotte (elite),
  Kattekongen (sjef som tilkaller katter). Vanskelighetsgrad øker med antall seire.

## Ikke med i MVP

Mat og sult, aldring, hus-statistikk, flere områder, butikk, lyd. Lagring skjer lokalt i nettleseren.

## Akseptansekriterier (selvverifikasjon)

Automatisk testet med Playwright mot den ekte siden (`tests/playtest.mjs`):

1. Siden laster uten konsollfeil eller sidefeil, i både skrivebords- og mobilbredde, uten horisontal rulling.
2. Genetikk over 2000 parringer: alle egenskaper i 1-10, hver valpeegenskap er innen ±1 av en forelders
   verdi, valpens lærte evner kommer fra foreldrene, maks 2 evner og 3 mutasjoner.
3. Innavl gir målbart flere defekter enn ubeslektede foreldre.
4. 300 autospilte kamper: alltid ferdige innen 60 runder, aldri to enheter på samme rute, aldri enhet på
   hindring, HP aldri over maks eller NaN.
5. 100 autospilte turer fra start til slutt: ender alltid i seier, tap eller hjemgang, døde fjernes,
   overlevende blir veteraner, dagen går fram.
6. Balanse: en autospiller med et vanlig startlag vinner en del turer, men ikke alle (mål: 15-85 %).
7. Én ekte kamp spilles med museklikk i DOM (velg hund, flytt, angrip, avslutt tur), og et parringsløp
   gjøres med klikk, med skjermbilder av hver skjerm.
8. Lagring overlever omlasting av siden.
