# Redaksjonsporten

Kontroll av den endelige kanalversjonen etter redaksjonsordren 25. november 2026
(se `AGENTS.md`). Porten publiserer ikke, planlegger ikke og sender ikke. Den
svarer `PASSERER` (avslutningskode 0) eller `HOLDES` (avslutningskode 1), og
verktøyet som kaller den, skal la innholdet ligge som utkast ved `HOLDES`.

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
3. **Redaktørens godkjenning.** Ved funn, ved erklært teologisk vurdering eller
   ved uavklart innhold kreves en godkjenning som er signert med ansvarlig
   redaktørs nøkkel og bundet til nøyaktig denne versjonen (SHA-256). Endres
   ett tegn eller én byte i videoen, gjelder ikke godkjenningen lenger.
   Godkjenningen må oppgi Topp 100-filens versjon og punktene den bygger på,
   eller si hva som går utover listen.
4. **Marias navn.** Når Maria er oppgitt som journalist, kreves riktig byline,
   riktig forfatter i Ghost, riktig avsendernavn og signatur i e-post, og
   hennes egen signerte bekreftelse av versjonen. Hennes navn brukt uten at hun
   er oppgitt som journalist, holdes. Byttet byline endrer ikke punkt 2 og 3.

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
  "filer": {},
  "forfatterbekreftelse": "bekreftelse.json",
  "godkjenning": "godkjenning.json"
}
```

Kanaler: `ghost-artikkel`, `ghost-nyhetsbrev`, `nyhetsstrom`, `youtube-video`,
`youtube-shorts`, `epost`, eller et annet navn for andre flater. Video krever
`filer.video` og minst ett av tekstfeltene `manus`, `fortellerstemme`,
`undertekster`, i tillegg til `tittel`, `beskrivelse` og `skjermtekst`. E-post
har i tillegg `"epost": {"avsendernavn": "", "signatur": ""}` og brødteksten i
`tekst.brodtekst`. `egen_teologisk_vurdering` må oppgis. Mangler feltet, er
saken uavklart.

## Kommandoer

```bash
python redaksjonsport/port.py kontroller sak.json --fase planlegging
```

```bash
python redaksjonsport/port.py kontroller sak.json --fase utsending --planlagt-versjon <sha256 fra planleggingen>
```

```bash
python redaksjonsport/port.py forelegg sak.json
```

```bash
python redaksjonsport/torrkjoring.py -v
```

`forelegg` skriver ut nøyaktig tekst, versjonshash, skjermens funn og en
godkjenning til utfylling. Den som forbereder saken, fyller inn Topp 100-filens
versjon, punktene, hva de faktisk behandler og hvordan vurderingen samsvarer.
Redaktøren leser, retter og signerer selv.

## Nøklene: hvorfor en AI ikke kan godkjenne

Godkjenningen er en fil pluss en Ed25519-signatur. Porten stoler bare på de
offentlige nøklene i tillitsmappen (`~/.mantelen/tillit/`, eller mappen i
miljøvariabelen `MANTELEN_TILLIT`), som ligger utenfor repoet. Uten
privatnøkkelen kan ingen lage en gyldig signatur. Finnes ingen redaktørnøkkel i
tillitsmappen, holdes alt teologisk og uavklart innhold.

Engangsoppsett, gjort av redaktøren selv (krever `openssl` 3, som følger med Git):

```bash
openssl genpkey -algorithm ed25519 -aes-256-cbc -out redaktor-privat.pem
```

```bash
openssl pkey -in redaktor-privat.pem -pubout -out ~/.mantelen/tillit/redaktor.pub.pem
```

Godkjenne én versjon:

```bash
openssl pkeyutl -sign -inkey redaktor-privat.pem -rawin -in godkjenning.json -out godkjenning.json.sig
```

Maria gjør det samme med egen nøkkel. Den offentlige delen heter
`journalist-maria.pub.pem`, og hun signerer en bekreftelse med feltene
`sak_id`, `journalist` og `versjon_sha256`.

Privatnøkkelen og passordfrasen skal aldri ligge der en AI kan lese dem, og
aldri gis til en AI. Hver kvittering fra porten oppgir fingeravtrykket til
nøklene som ble brukt, slik at et nøkkelbytte synes.

## Grenser

- Skjermen er et gulv. Den fanger skriftsteder og åpenbare teologiske utsagn i
  redaksjonens stemme, på norsk og engelsk. Den forstår ikke teksten. Det den
  ikke fanger, er fortsatt omfattet av ordren, og den som forbereder saken, har
  plikt til å erklære `egen_teologisk_vurdering` riktig.
- Porten leser ikke lyd og bilde. For video binder godkjenningen filen byte for
  byte, men det er den som forbereder saken, som må legge frem all tekst og tale.
- Porten virker bare der den er koblet inn. Publisering for hånd i Ghost Admin,
  YouTube Studio eller Gmail går utenom den.
- Den som har full skrivetilgang til maskinen, kan endre portens kode eller
  peke den mot en annen tillitsmappe. Signaturen hindrer at en godkjenning kan
  fylles ut, men ikke at verktøyet saboteres. Fingeravtrykkene i kvitteringene
  og git-historikken er kontrollen mot det.

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
- saker og videoer som allerede ligger planlagt
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
