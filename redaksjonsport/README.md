# Redaksjonsporten

Kontroll av den endelige kanalversjonen etter redaksjonsordren 25. november 2026
(se `AGENTS.md`). Porten publiserer ikke, planlegger ikke og sender ikke. Den
svarer `PASSERER` (avslutningskode 0) eller `HOLDES` (avslutningskode 1), og
verktøyet som kaller den, skal la innholdet ligge som utkast ved `HOLDES`.

Regelen gjelder fra 25. november 2026 og virker ikke tilbake i tid.

Status 25. november 2026: porten er skrevet og tørrkjørt i dette repoet. Den er
ikke koblet inn i verktøyene som faktisk planlegger, publiserer og sender. De
ligger utenfor dette repoet. Se «Innkobling» nederst.

## Hva porten prøver

1. **Hele kanalversjonen er lagt frem.** All tekst publikum møter, og for video
   også den ferdige filen. Mangler noe, er saken uavklart og holdes.
2. **Egen teologisk vurdering.** En innholdsskjerm leser tittel, ingress,
   brødtekst, bildetekster, manus, fortellerstemme, skjermtekst, undertekster og
   beskrivelse. Sitater i anførselstegn og setninger som tilskrives en navngitt
   kilde, regnes som gjengivelse. Skriftsteder og teologiske utsagn i
   redaksjonens egen stemme gir funn. Bibelens forfattere regnes ikke som kilder.
3. **Redaktørens ja.** Ved funn, ved erklært teologisk vurdering eller ved
   uavklart innhold kreves det at ansvarlig redaktør har svart ja til nøyaktig
   denne versjonen (SHA-256). Endres ett tegn eller én byte i videoen, gjelder
   ikke svaret lenger. Svaret må være notert ordrett, med tid og sted, sammen
   med Topp 100-versjonen og punktene vurderingen bygger på, eller hva som går
   utover listen.
4. **Marias navn.** Når Maria er oppgitt som journalist, kreves riktig byline,
   riktig forfatter i Ghost og riktig avsendernavn og signatur i e-post. Hennes
   navn brukt uten at hun er oppgitt som journalist, holdes. Byttet byline
   endrer ikke punkt 2 og 3.

## Slik går en godkjenning

1. Den som forbereder saken, lager spørsmålet:

```bash
python redaksjonsport/port.py forelegg sak.json --topp100-versjon "23.11.2026" --punkter 35,41 --samsvar "Én setning om hva punktene behandler." --utover "Hva som går utover listen."
```

2. Spørsmålet vises til redaktøren. Det er kort:

```text
TIL GODKJENNING: «Tittel» (ghost-artikkel)
Godkjenner du denne teologiske vurderingen? Svar ja eller nei.

Dette sier MANTELEN selv:
  1. Paulus skriver i Romerbrevet 12,2 at ...
  2. Kirken bør derfor ...

Topp 100 (23.11.2026): punkt 35. Én setning om hva punktet behandler.
Går utover listen: ...
Versjon 910f6cb326d4. Hele teksten står under.
```

3. Redaktøren svarer ja eller nei. Svaret noteres ordrett:

```bash
python redaksjonsport/port.py svar sak.json --svar ja --ord "Ja" --hvor "Hvor svaret ble gitt"
```

4. Kontrollen kjøres ved planlegging og rett før utsending:

```bash
python redaksjonsport/port.py kontroller sak.json --fase planlegging
```

```bash
python redaksjonsport/port.py kontroller sak.json --fase utsending --planlagt-versjon <sha256 fra planleggingen>
```

Er teksten endret etter foreleggelsen, kan svaret ikke noteres, og et ja som
er notert, slutter å gjelde. Da spørres redaktøren på nytt.

Tørrkjøring uten at noe sendes eller publiseres:

```bash
python redaksjonsport/torrkjoring.py -v
```

## Saksfil

```json
{
  "id": "slug-eller-video-id",
  "kanal": "ghost-artikkel",
  "journalist": "Maria Solbak Årnes",
  "byline": "Av Maria Solbak Årnes, journalist i MANTELEN",
  "forfatter": "Maria Solbak Årnes",
  "egen_teologisk_vurdering": false,
  "tekst": {"tittel": "", "ingress": "", "brodtekst": "", "bildetekster": []},
  "filer": {}
}
```

Kanaler: `ghost-artikkel`, `ghost-nyhetsbrev`, `nyhetsstrom`, `youtube-video`,
`youtube-shorts`, `epost`, eller et annet navn for andre flater. Video krever
`filer.video` og minst ett av tekstfeltene `manus`, `fortellerstemme`,
`undertekster`, i tillegg til `tittel`, `beskrivelse` og `skjermtekst`. E-post
har i tillegg `"epost": {"avsendernavn": "", "signatur": ""}` og brødteksten i
`tekst.brodtekst`. `egen_teologisk_vurdering` må oppgis. Mangler feltet, er
saken uavklart. Foreleggelsen og svaret lagres ved siden av saksfilen som
`<id>.foreleggelse.json` og `<id>.godkjenning.json`.

## Grenser

- Svaret noteres av den som spurte, etter at redaktøren har svart. Porten kan
  ikke selv vite at han svarte. Vernet er at svaret må gjengi hans ord og hvor
  de ble gitt, at det er bundet til versjonen, og at instruksen forbyr å notere
  et svar han ikke har gitt. Vil redaktøren ha et sterkere vern, kan han legge
  en offentlig nøkkel i `~/.mantelen/tillit/redaktor.pub.pem`. Da krever porten
  i tillegg at svaret er signert med nøkkelen hans.
- Skjermen er et gulv. Den fanger skriftsteder og åpenbare teologiske utsagn i
  redaksjonens stemme, på norsk og engelsk. Den forstår ikke teksten. Det den
  ikke fanger, er fortsatt omfattet av ordren, og den som forbereder saken, har
  plikt til å erklære `egen_teologisk_vurdering` riktig.
- Porten leser ikke lyd og bilde. For video binder svaret filen byte for byte,
  men det er den som forbereder saken, som må legge frem all tekst og tale.
- Porten virker bare der den er koblet inn. Publisering for hånd i Ghost Admin,
  YouTube Studio eller Gmail går utenom den.
- Porten sjekker at Marias navn og signatur er riktig brukt. Den kan ikke vite
  hvem som faktisk skrev teksten. Det er instruksen som forbyr en AI å tildele
  henne forfatterskap.

## Innkobling

Porten må kalles fra hvert verktøy som kan sette noe ut til publikum eller til
en kilde. Repoet er offentlig, så den konkrete listen over skript, jobber og
køer føres i den interne driftsdokumentasjonen og ikke her. Veiene som skal dekkes:

- alt som setter en sak i Ghost til planlagt eller publisert, også omskriving av
  publiserte saker
- nyhetsbrev
- kortnyheter og redaksjonelle linjer som bakgrunnsjobber legger ut
- opplasting og planlegging av video og Shorts, med tittel, beskrivelse og undertekster
- kilde-e-post
- sosiale kanaler

Mønster for et verktøy:

1. Bygg saksfilen fra den endelige kanalversjonen, ikke fra manuset den ble laget av.
2. Kjør `kontroller --fase planlegging` før planlegging. Lagre `versjon_sha256`.
3. Kjør `kontroller --fase utsending --planlagt-versjon <hash>` rett før utsending.
4. Ved avslutningskode ulik 0, eller hvis porten ikke kan kjøres: la innholdet
   ligge som utkast og meld grunnene til ansvarlig redaktør.

Arbeid for hånd eller via nettleserstyring i Ghost Admin, YouTube Studio og
e-post går utenom porten og dekkes bare av instruksen i `AGENTS.md`.

Finnes det allerede en versjonsbundet godkjenningsmekanisme i et verktøy, skal
den brukes der i stedet for en parallell ordning.
