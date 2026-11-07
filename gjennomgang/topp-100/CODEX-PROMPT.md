# Oppdrag til Codex: kritisk gjennomgang av «Topp 100 kristne stridsspørsmål»

## Rolle

Du er en uavhengig og streng fagfellevurderer. Du skal finne kritiske feil, svakheter og mangler i et dokument som Claude har skrevet. Du skal ikke skrive om dokumentet. Rapporten din går tilbake til Claude, som skal rette dokumentet ut fra den.

Vær kritisk. Et funn som viser seg å være feil, koster lite. En feil som blir stående, koster mye.

## Bakgrunn

Dokumentet rangerer 102 kristne stridsspørsmål og tar stilling i hvert av dem. Det er skrevet for Elias Solbak Årnes, ansvarlig redaktør i Mantelen, et norsk kristent tidsskrift utgitt av Guds Sanne Menighet. Siste del sammenligner Claudes standpunkter med standpunktene til Guds Sanne Menighet og Mantelen.

Dokumentet sier selv hvordan det vekter:

- **Posisjonene:**
  - Skriften, 45 %.
  - De tidligste kristnes lære og praksis, 30 %. Vekten avtar med tiden: før 200 teller fullt, 200-325 tungt, 325-451 moderat og senere lite.
  - Logikk og indre sammenheng, 25 %.
- **Rangeringen:** sentralitet 45 %, splittelseskraft 20 %, aktualitet 20 % og utbredelse 15 %. Hver faktor har fått poeng fra 0 til 10.

Oppdraget er å prøve om dokumentet holder det det lover etter sine egne kriterier, og om faktaopplysningene stemmer.

## Filer (mappen `gjennomgang/topp-100/`)

| Fil | Hva den er |
|---|---|
| `Topp-100-Bibelen-og-tidligste-kirke.md` | **Hoveddokumentet. Dette skal du gjennomgå.** |
| `forrige-versjon-ortodoks-vekting.md` | Forrige versjon, der ortodokse kriterier var vektet 50 %. Bruk den bare til å kontrollere merkene «Endret» og «Uendret». |
| `rangering.py` | Poengsummene og beregningen av rangeringen. |
| `kilder/mantelen/*.txt` | Mantelen-artiklene dokumentet viser til, hentet fra mantelen.no 7.11.2026. |

To kilder er ikke vedlagt:

1. **Bokutkastet *Kvinnelige prester*** av Elias Solbak Årnes, som ligger på Google Drive. Dokumentet bygger på disse ordrette sitatene:
   - Endelig versjon (2026-09-06, sist endret 2026-10-05): «Uenighet om dette spørsmålet er heller ikke i seg selv grunn til å erklære en annen kristen for vantro.»
   - Endelig versjon, kapittel 10: «Han sier ikke uttrykkelig at begrensningen skal oppheves når bestemte kvinner har fått en autorisasjon eller fullført et undervisningsløp.»
   - Endelig versjon, kapittel 12: «Spørsmålet om tegnet skal videreføres uendret, fortjener en egen samvittighetsfull vurdering i menigheten.»
   - Versjonen fra 2026-09-02: «Dette er et sekundært spørsmål. Evangeliet står ikke på spill.»

   Har du ikke tilgang til manuset, skal du ikke kontrollere ordlyden. Vurder i stedet om dokumentet bruker sitatene riktig.

2. **Artikkelen «Jeg spurte en kvinnelig prest om underordning»** (Mantelen, 20.8.2026). Den ligger ikke lenger på nettstedet. Ordrett utdrag: «Hvis jeg har rett, synder de kvinnelige prestene. Da må de be Gud om tilgivelse og omvende seg. Og da må hver mannlig prest som har tiet, og som fremdeles tier, gjøre det samme. Og tar jeg feil, gjelder det samme alvoret meg.» Fra samme artikkel: «Jeg lot en kvinnelig prest døpe meg i min voksendåp, enda jeg mente det ikke var helt rett.»

Flere påstander om Mantelen bygger på en gjennomlesning av alle 294 sakene på mantelen.no og veirydderen.no. Finner du ikke belegg i de vedlagte filene, skal du sjekke nettstedene hvis du har nettilgang. Har du ikke nettilgang, merker du påstanden «ikke belagt i vedlagte kilder».

## Hva du skal kontrollere, i prioritert rekkefølge

### A. Faktafeil i kildehenvisninger

Kontroller hver henvisning til kirkefedre, konsiler, kanoner, bekjennelsesskrifter, håndskrifter og årstall:
- Finnes stedet?
- Sier det det dokumentet påstår?
- Stemmer nummereringen og dateringen?

Kontroller også at bibelhenvisningene faktisk støtter påstanden de står ved.

Disse stedene har Claude selv markert som usikre. Ta dem først:

- **1 Klem. 32,4** og ordlyden «ved gjerninger». Kontroller mot den greske teksten. Kontroller også **1 Klem. 45,3**: er det 45,2-3?
- **Justin:**
  - *Dial.* 5, 11, 65, 80-81, 82 og 95.
  - *1 Apol.* 8, 15, 43, 61, 66 og 67.
  - Påstanden om at Justin nevner rettroende kristne som ikke var chiliaster.
- **Irenaeus:** *Mot kjetterne* IV.37, V.6.1 og V.32-36.
- **Diognetbrevet** 5 og 9. **Didache** 2,2, 4,8, 7, 8,1, 9,5, 14 og 15.
- **Ignatius:** *Ef.* 16 og 18, *Smyrn.* 7, *Magn.* 9 og *Pol.* 3.
- **Plinius,** *Brev* X.96: «ministrae» og «carmen Christo quasi deo».
- **Tertullian:**
  - *Til Scapula* 2.
  - *Om kransen* 3 og *Om engifte* 10.
  - *Om dåpen* 8.
  - *Om avgudsdyrkelse* 19.
  - *Om jomfruenes tilsløring*.
  - *Mot Praxeas* (datering rundt 213).
  - Påstanden om at Tertullian benektet Marias livslange jomfrudom.
- **Origenes:**
  - *Mot Kelsos* VIII.73 og *Om bønnen* 11.
  - Påstanden om at han kaller barnedåpen apostolisk. Romerbrevkommentaren er bevart i Rufinus' latinske oversettelse; vurder hvor pålitelig det er.
  - Prekenen han holdt som lekmann i Caesarea rundt 215.
- **Hermas,** *Bud* 4,1. **Athenagoras,** *Bønneskrift* 33 og 35. **Kyprian,** brev 64 og *Om de frafalne* 25.
- **Den apostoliske tradisjon** 16, 18 og 21: tilskrivningen til Hippolyt og dateringen.
- **Laktants,** *Guddommelige institusjoner* V.19-20 og VI.20. **Minucius Felix,** *Octavius* 34, og dateringen «ca. 200».
- **Kanon:** Melitos kanonliste og Athanasius' påskebrev 39. Påstanden «Jesus og apostlene siterer aldri de deuterokanoniske bøkene som Skrift»; vurder blant annet Jud 14-15 og hentydninger til Visdommens bok.
- **Kirkemøter og striden om gjendåp:** Elvira kanon 36 (datering), Nikea kanon 8 og 19, striden mellom Stefan og Kyprian, og Hieria 754.
- **Arkeologi:** Dura-Europos rundt 240 og innrissingene i katakombene under San Sebastiano.
- **Påske:** Polykarp og Anicetus rundt 155.
- **Nattverdbrødet:** Firenze 1439 om syret og usyret brød, og påstanden om at usyret brød ble vanlig i vest i karolingisk tid.
- **Kalenderen:** overgangen i 1924 og gammelkalendaristenes brudd.
- **Comma Johanneum:** «ikke i noe gresk håndskrift før senmiddelalderen».
- **Enebiskop:** i Lilleasia rundt 110 og i Roma rundt 150.
- **Gregor av Nyssa,** fjerde preken over Forkynneren, om slaveri.
- **Lutherske bekjennelsesskrifter:**
  - Konkordieformelen art. II om synergisme.
  - Apologien XXIV om bønn for de døde.
  - CA XXI om helgenpåkallelse.
  - Melanchthons forbehold til Schmalkaldiske artikler om paven: ordlyden.
- **Thomas Oden og «paleo-ortodoksi»:** dekker begrepet det dokumentet bruker det om?
- **Generaliseringer** som må prøves:
  - «Alle kirkefedre før Augustin lærer den frie viljen.»
  - «Evig bevisst straff er flertallssynet i den tidligste kirken.»
  - «Den tidligste kirken var overveiende premillennialistisk.»
  - «Den tidligste kirken brukte trolig vanlig brød.»

### B. Feilfremstilling av Guds Sanne Menighet og Mantelen

Kontroller hver påstand i delen «Hvor standpunktene mine skiller seg fra Guds Sanne Menighet og Mantelen» mot `kilder/mantelen/`. Prøv særlig to ting:

- **Skjevt utvalg.** Er sitatene tatt ut av sammenhengen? Det gjelder blant annet *Fundamentet* 5 om voksendåp, *Fundamentet* 6 om åndsdåp, Marias forklaring av navnet i `der-skulle-du-statt`, og Morgenkåpen 13 og 16.
- **Rettferdighet.** Er det rimelig å kalle det en forskjell eller en spenning? Det gjelder særlig punktet om pastorkallet og punktet om at Mantelen sier seg nøytral samtidig som essayene tar standpunkt.

Feilfremstilling av en virkelig person eller menighet regnes alltid som **kritisk**.

### C. Logiske feil og brudd på egne kriterier

1. **Brukes vektingen konsekvent?** Finn tilfeller der konklusjonen ser ut til å følge forfatterens forhåndssyn, ikke de oppgitte vektene. Sjekk særlig der den tidligste kirken brukes som avgjørende i ett spørsmål og overstyres i et annet:
   - nr. 6 barnedåp, nr. 22 skilsmisse og nr. 55 tusenårsriket, mot nr. 68 prevensjon og nr. 61 ikoner;
   - nr. 56 helgenpåkallelse og nr. 72 barnekommunion, mot nr. 1 *sola scriptura*.
2. **Henger posisjonene sammen?** Eksempler:
   - nr. 7 (Skriften tar ikke feil) mot nr. 29 (evolusjon) og nr. 44 (den historiske Adam);
   - nr. 11 (kvinners ordinasjon), nr. 23 (hodeskap) og nr. 76 (hodeplagg): brukes skapelsesargumentet likt?
   - nr. 12 (kirkens vesen) mot punkt 4 i sammenligningen med Mantelen (kirken og kallet).
3. **Holder merkene?** Stemmer «Endret» og «Uendret» med forrige versjon? Er sikkerhetsgradene rimelige ut fra belegget som oppgis?
4. **Sirkelslutninger og stråmenn.** Er motargumentene gjengitt i sin sterkeste form?

### D. Rangeringen

1. Kjør `python3 rangering.py`, og kontroller at rekkefølgen i dokumentet stemmer med utskriften.
2. Pek ut de 10 poengsummene som ser mest vilkårlige ut. Begrunn hver av dem, og foreslå en ny verdi.
3. Gjør en følsomhetsanalyse. Hvor mye endres topp 12 og topp 30 hvis:
   - S-poengene endres med pluss eller minus 1?
   - vektene endres til 40/20/25/15?

### E. Mangler

- Viktige argumenter eller motargumenter som mangler i enkeltspørsmål. Prioriter de stedene der dokumentet ikke gjengir det sterkeste argumentet fra motsatt side.
- Stridsspørsmål av betydning som mangler i listen. Foreslå hvilke av dagens nr. 90-102 de i så fall bør erstatte.
- Tradisjoner hvis syn er fremstilt skjevt eller ikke er tatt med: katolsk, reformert, pinsekarismatisk, orientalsk-ortodoks og anabaptistisk.

### F. Form

Rapporter bare forhold som skaper uklarhet eller feil. Se ikke etter stilsaker. Dokumentet skal ikke inneholde tegnene U+2013, U+2014 eller U+2015. Flagg alle forekomster.

## Hvordan du skal klassifisere funn

- **Type:**
  - FEIL: påviselig galt.
  - SVAKHET: forsvarlig, men svakt begrunnet.
  - MANGEL: noe vesentlig er utelatt.
  - UENIGHET: du ville vurdert annerledes, men det er ikke en feil. Hold disse adskilt og korte.
- **Alvorlighet:**
  - Kritisk: endrer en posisjon eller en plassering, eller fremstiller en person eller kilde galt.
  - Vesentlig: svekker begrunnelsen merkbart.
  - Mindre: detalj som bør rettes.

## Hva du skal levere

Skriv to filer i `gjennomgang/topp-100/`:

### 1. `CODEX-RAPPORT.md`, på norsk

1. **Sammendrag**, høyst 10 linjer: antall funn per type og alvorlighet, og de fem viktigste funnene.
2. **Funn**, sortert etter alvorlighet. Hvert funn skal ha disse feltene:
   - **ID** (K-001, K-002 ...)
   - **Type og alvorlighet**
   - **Plassering:** spørsmålsnummer og tittel, eller navnet på delen
   - **Påstanden:** ordrett sitat fra dokumentet
   - **Problemet**
   - **Belegg:** kilde med nøyaktig henvisning (verk, bok, kapittel, avsnitt, utgave eller URL). Oppgi også hvordan du har kontrollert: «primærkilde», «sekundærkilde» eller «ikke kontrollerbar».
   - **Forslag til retting:** konkret ny ordlyd, eller hvilken posisjon eller plassering som bør endres
   - **Din sikkerhet:** høy, middels eller lav
3. **Rangeringen:** resultatet av kontrollkjøringen, de tvilsomme poengsummene og følsomhetsanalysen.
4. **Ikke kontrollert:** påstander du ikke fikk kontrollert, og hvorfor.
5. **Uenigheter**, adskilt fra resten.

### 2. `CODEX-RAPPORT.json`

En liste med ett objekt per funn, med feltene `id`, `type`, `alvorlighet`, `nr`, `seksjon`, `pastand`, `problem`, `belegg`, `kontrollmetode`, `forslag`, `sikkerhet`.

## Regler

- **Ikke endre hoveddokumentet** eller de andre filene. Skriv bare de to rapportfilene.
- **Ikke dikt opp kilder.** Er du usikker på en henvisning, skal du si det. Siter primærkilder ordrett på originalspråket eller i en navngitt standardoversettelse.
- **Skill mellom hva teksten sier og hva du mener om den.**
- **Ikke legg til personopplysninger** om Elias Solbak Årnes, Maria Solbak Årnes eller andre utover det som allerede står i dokumentet.
- **Ikke bruk tegnene U+2013, U+2014 eller U+2015** i rapporten. Bruk komma, kolon, parentes eller bindestrek.
- **Bruker du git,** skal du committe rapporten på en egen gren, for eksempel `codex/topp-100-gjennomgang`, og ikke på `main`.
- **Skriv slik at hvert funn kan rettes uten å lese resten av rapporten.** Claude skal gå gjennom funnene ett for ett.
