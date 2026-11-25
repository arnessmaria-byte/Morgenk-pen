# Trinn 0: ti pilotsteder i manuskriptlaget

Grunnregistrering: Fable. Kilde- og ankerkontroll: Codex. 25. november 2026.

Captain har gitt skriftlig tillatelse til innhenting innenfor lisensmatrisen. Ingen tillatelse fra tredjepart eller faglig låsing følger av dette. Den tekniske kontrollen gjelder de ti oppgitte stedene. Se også `kilder/katalogkontroll/` for kildefakta, avgrensninger og kontrollsummer.

Rapporten viser de ti pilotstedene som manuskriptkort, slik de er tenkt i leseren når «Manuskript- og grunnkildemodus» er slått på. Kortene er laget maskinelt fra `piloter/trinn0-10-piloter.json` og registrene. Ingen fil i låst R10/R11.1 er endret.

## Status

56 av 56 fysiske vitner har en kildedato eller navngitt periode. 50 av 56 har oppbevaringssted dokumentert i registeret. De tretten øvrige registeroppføringene gjelder verk eller tradisjoner.

Oppbevaringssted som gjenstår å bekrefte for pilotfragmentet: 11QPsa, 4QDeutj, 4QDeutq, 4QIsad, 4QPsf, 5/6HevPs.

Ved Joh 1,18 er Origenes, Contra Celsum II.71, en separat parallell uten stemme. Ved Mark 1,1 er II.4 registrert fra gresk. Se verskortene og kildebelegget.

Alle ti enhetene er **utkast**. De består skjema, anker og registerkontroll, men de kan ikke låses ennå. Planen krever at hvert vitne er lest i kilden av en navngitt person, og at hver enhet er registrert av to uavhengige lesere. Det er ikke gjort.

| Kontroll | Resultat |
|---|---|
| JSON Schema | 10 av 10 pilotsteder består |
| Ordanker mot låst R10/R11.1 (ord og SHA-256) | 10 av 10 treffer |
| Sigla og patristiske referanser i `vitneregister.json` | 100 %, 0 uregistrerte |
| Dateringer skrevet inn for hånd | 0 |
| Vurdering (akse 3) | «ikke vurdert» i alle ti |
| Dobbel registrering | ikke kjørt |

Av 160 vitne- og utgaveopplysninger i de ti enhetene:

| Status | Antall | Betydning |
|---|---|---|
| lest i transkripsjon | 79 | Lesningen er funnet maskinelt i en importert transkripsjon av håndskriftet (INTF, ETCBC, WLC). |
| lest i utgavens tekst | 26 | Lesningen er funnet i utgavens egen digitale tekst. |
| R10 | 10 | Lesningen er ankerordene i låst R10. |
| oppgitt i annet datasett | 25 | Utgavens valg er hentet fra et annet fritt datasett. Utgaven selv er ikke avlest. |
| funnet i oversettelse | 15 | Fedresitatet er funnet i engelsk oversettelse. Gresk eller latinsk ordlyd er ikke avlest. |
| delvis lest | 1 | Deler av lesningen er funnet. Resten må leses i trykt utgave. |
| ikke avlest | 4 | Oppgitt i oppdraget eller håndbøkene. Ikke lest i noen kilde i Trinn 0. |

## Funn som endrer oppdraget

- **Åp 22,19 og P (025).** Oppdraget fører P som vitne for «livets tre». INTFs sideindeks viser at Codex Porphyrianus slutter med Åp 22,2–6. Stedet er ikke bevart, og håndskriftet er ført som utelukket vitne med belegg. 046 har bladet, men ingen publisert transkripsjon, og står som ikke avlest.
- **Apg 8,37 har tre greske former.** Ingen av de transkriberte håndskriftene har nøyaktig Scriveners ordlyd. Laudianus (500-tallet) har «skal du bli frelst» og «jeg tror på Kristus, Guds Sønn». Minusklene har «han sa til ham» uten Filips navn.
- **1 Tim 3,16.** Bare 01, 02, 04 og minuskel 6 har publisert transkripsjon hos INTF. D* og D² er derfor ikke avlest. Ingen før-nikensk far er funnet med et ordrett sitat. De to fedrene med «Gud» er fra 300-tallet.
- **Sal 22,17.** R10-noten gjengir ὤρυξαν med «de gravde». Kortet har derfor to gjengivelser av lesningen: «de har gravd» (ordrett) og «de har gjennomboret» (tradisjonell, tolkende), slik planen krever.
- **5 Mos 32,43 og Hebr 1,6.** Sitatet i Hebr 1,6 er likt Odae 2:43 bortsett fra artikkelen. Etter planens regel er det ikke et uavhengig vitne. Den digitale Swete-teksten til 5 Mos 32:43 har OCR-tap og kan ikke brukes uten korrektur.
- **Datering og depot.** Ordlyden i katalogen beholdes når den oppgir en periode eller et omtrentlig tidspunkt. Funnsted og utlåner registreres ikke som fysisk depot uten eget belegg. Samlebetegnelser og fedreverk har ikke én håndskriftdato eller ett depot.
- **Pilotlisten.** Oppdraget og planens vedlegg B har ulike lister. Oppdraget har Mark 1,1, Joh 1,18, Apg 8,37 og 1 Tim 3,16 der vedlegg B har 1 Sam 10,27b, Luk 23,34a, Mark 16,9–20 og 1 Joh 5,7–8. Denne leveransen følger oppdraget.
- **Tekniske funn.** R10-filene har greske aksenttegn som NFC-normalisering endrer, så ankerord må sammenlignes byte for byte. Nettstedets mellomlager gir eldre kopier av `joh.json` og `1ti.json` når versjonsparameteren mangler. TAGNT og Robinson–Pierponts variantnote er uenige om NA28 har artikkelen i Mark 1,1.

## Slik leses kortene

Øverst står R10-lesningen. Deretter kommer hver lesning med grunntekst, ordrett norsk og vitnene sortert etter alder. Utgaver står på egen linje og er ikke vitner. Vitnemønsteret er regnet ut av maskinen. Vurderingen ligger bak en egen fane og er ikke satt for noen av de ti.

---

## 1. Jes 53,11

`GT-ISA-053-011-01` · utkast

**MANTELEN (R10):** «Etter sin sjels møye skal han se og mettes. Ved sin kunnskap skal min rettferdige tjener rettferdiggjøre de mange, og deres misgjerninger skal han selv bære.»

**Ankerord:** יִרְאֶ֣ה (ord 3, id 23EFM): tillegget står etter dette ordet

### Lesning a: MT: uten objekt · MANTELEN (R10)

- Grunntekst: יִרְאֶה
- Ordrett norsk: «skal han se»
- Form: Verb, Qal, yiqtol, 3. person maskulinum entall. Verbet står uten objekt.
- Utgaver som har lesningen: MANTELEN (R10), MAM

| Håndskrift | Type | Datering | Sted | Har på stedet | Status |
|---|---|---|---|---|---|
| B19ᴬ (Codex Leningradensis) | kodeks | 1008–1010 |  | יראה ישבע | lest i transkripsjon |

### Lesning b: «lys»

- Grunntekst: יראה אור
- Ordrett norsk: «skal han se lys» (ordrett)
- Form: Samme verb med objektet אוֹר: substantiv, maskulinum entall, absolutt form.

| Håndskrift | Type | Datering | Sted | Har på stedet | Status |
|---|---|---|---|---|---|
| 1QIsaᵃ | rulle | ca. 125 BCE | ETCBC-sted 44, linje 19–20 | יראה אור | lest i transkripsjon |
| 1QIsaᵇ | rulle | Herodian | ETCBC-sted 23, linje 22–23 | יראה אור | lest i transkripsjon |
| 4QIsaᵈ | rulle | Herodian | ETCBC-sted 8, linje 20–21 | יראה או?[ר] (delvis rekonstruert) | lest i transkripsjon |

- Oversettelse: **LXX** Isa 53:11: δεῖξαι αὐτῷ φῶς, «å vise ham lys» (ordrett). Forelegg: sannsynlig. Status: lest i utgavens tekst. Gresk har en annen setningsbygning (infinitiv). Ordet φῶς svarer til אור og kan ikke avledes av MT-ordlyden.

**Vitnemønster (regnet ut):** Q = G ≠ M

**Variantart:** pluss (mekanisk grovsortering: pluss_minus) · **Betydningsgrad:** betydning

**Vurdering:** ikke vurdert. Egen fane i leseren.

**Filologisk notat.** Etter יִרְאֶה har tre Jesaja-ruller ordet אור, «lys», og Septuaginta har φῶς på samme sted. Den masoretiske teksten har verbet uten objekt, og R10 følger den: «skal han se». I 1QIsaᵃ og 4QIsaᵈ står det dessuten «og» foran det neste verbet, mens 1QIsaᵇ og MT ikke har det. I 4QIsaᵈ er siste bokstav i אור rekonstruert i transkripsjonen. 4QIsaᵇ (4Q56) har bare slutten av verset og er ikke vitne på dette stedet. Om «lys» er falt ut i MT eller lagt til i de andre vitnene, er en vurdering og er ikke gjort her.

**Må kontrolleres mot kilde:**

- Dateringen av de tre rullene hentes fra DJD XV og DJD XXXII av navngitt leser. Leon Levy oppgir bare periode.

---

## 2. 5 Mos 32,8

`GT-DEU-032-008-01` · utkast

**MANTELEN (R10):** «Da Den Høyeste ga folkeslagene arv, da han skilte menneskenes sønner fra hverandre, fastsatte han folkenes grenser etter tallet på Israels sønner.»

**Ankerord:** בְּנֵ֥י … יִשְׂרָאֵֽל׃ (ord 11–12, id 05K67–05hVg): lesningene gjelder disse ordene

### Lesning a: MT: «Israels sønner» · MANTELEN (R10)

- Grunntekst: בְּנֵי יִשְׂרָאֵל
- Ordrett norsk: «Israels sønner»
- Form: Substantiv, maskulinum flertall, konstruktus + egennavn.
- Utgaver som har lesningen: MANTELEN (R10), MAM

| Håndskrift | Type | Datering | Sted | Har på stedet | Status |
|---|---|---|---|---|---|
| B19ᴬ (Codex Leningradensis) | kodeks | 1008–1010 |  | בני ישראל | lest i transkripsjon |

### Lesning b: «Guds sønner»

- Grunntekst: בני אלוהים
- Ordrett norsk: «Guds sønner» (ordrett)
- Form: Substantiv, maskulinum flertall, konstruktus + אלוהים (plene skrivemåte).

| Håndskrift | Type | Datering | Sted | Har på stedet | Status |
|---|---|---|---|---|---|
| 4QDeutʲ | rulle | Herodian | ETCBC-sted 12, linje 13–14 | בני אלוהים | lest i transkripsjon |

- Oversettelse: **LXX** Deut 32:8: ἀγγέλων θεοῦ, «Guds engler» (ordrett). Forelegg: sannsynlig. Status: lest i utgavens tekst. Gresk har «engler», ikke «sønner». Ordlyden forutsetter et gudsnavn i forelegget og kan ikke avledes av «Israels sønner».

**Vitnemønster (regnet ut):** Q = G ≠ M

**Variantart:** leksikalsk (mekanisk grovsortering: leksikalsk_eller_morfologisk) · **Betydningsgrad:** betydning

**Vurdering:** ikke vurdert. Egen fane i leseren.

**Filologisk notat.** Forskjellen gjelder hvem tallet viser til. MT har «Israels sønner», og R10 følger den. 4QDeutʲ har בני אלוהים, «Guds sønner». Swetes greske tekst har ἀγγέλων θεοῦ, «Guds engler». R10-noten til verset viser til Tovs drøfting av stedet. 4QpaleoDeutʳ (4Q45) har deler av verset, men ordene det gjelder, er rekonstruert der, så rullen er ikke vitne. 4QDeutᑫ har ikke bevart verset. Vurderingen av hvilken lesning som er eldst, hører til akse 3 og er ikke gjort.

**Må kontrolleres mot kilde:**

- Greske håndskrifter med υἱῶν θεοῦ, «Guds sønner», oppgis i Wevers’ Göttingen-utgave. Sigla og datering må leses der og i Rahlfs–Fraenkel før de registreres.
- Den samaritanske Pentateuk oppgis å lese som MT. Stedet må leses i von Gall.

---

## 3. 5 Mos 32,43

`GT-DEU-032-043-01` · utkast

**MANTELEN (R10):** «Juble, folkeslag, over hans folk! For han skal hevne sine tjeneres blod og vende hevn tilbake over sine motstandere; han skal gjøre soning for sitt land og sitt folk.»»

**Ankerord:** הַרְנִ֤ינוּ … עַמּֽוֹ׃ (ord 1–13, id 05w7w–05CFi): lesningene gjelder hele verset

### Lesning a: MT: kortere tekst · MANTELEN (R10)

- Grunntekst: הַרְנִ֤ינוּ גוֹיִם֙ עַמּ֔וֹ כִּ֥י דַם־עֲבָדָ֖יו יִקּ֑וֹם וְנָקָם֙ יָשִׁ֣יב לְצָרָ֔יו וְכִפֶּ֥ר אַדְמָת֖וֹ עַמּֽוֹ׃
- Ordrett norsk: «Juble, folkeslag, over hans folk! For han skal hevne sine tjeneres blod og vende hevn tilbake over sine motstandere; han skal gjøre soning for sitt land og sitt folk.»»
- Form: Fire ledd: oppfordring til folkeslagene, hevn for tjenernes blod, gjengjeldelse, soning for land og folk.
- Utgaver som har lesningen: MANTELEN (R10), MAM

| Håndskrift | Type | Datering | Sted | Har på stedet | Status |
|---|---|---|---|---|---|
| B19ᴬ (Codex Leningradensis) | kodeks | 1008–1010 |  | … י דם עבדיו יקום ונקם ישיב לצריו וכפר אדמתו עמו | lest i transkripsjon |

### Lesning b: 4QDeutᑫ: lengre tekst

- Grunntekst: הרנינו שמים עמו והשתחוו לו כל אלהים כי דם בניו יקום ונקם ישיב לצריו ולמשנאיו ישלם ויכפר אדמת עמו
- Ordrett norsk: «Juble, himler, med ham, og tilbe ham, alle guder! For sine sønners blod skal han hevne, og hevn skal han vende tilbake over sine motstandere; dem som hater ham, skal han gjengjelde, og han skal gjøre soning for sitt folks land.» (ordrett); «Juble, himler, over hans folk …» (tolkende: עמו er uvokalisert og kan leses «med ham» (slik gresk har) eller «hans folk» (slik MT vokaliserer ordet).)
- Form: Seks ledd. Oppfordringen går til himlene, ikke folkeslagene. Leddet om tilbedelse og leddet om dem som hater ham, står ikke i MT. «Sønner» der MT har «tjenere».

| Håndskrift | Type | Datering | Sted | Har på stedet | Status |
|---|---|---|---|---|---|
| 4QDeutᑫ | rulle | Herodian | ETCBC-sted f5ii, linje 6–11 | הרנינו שמים עמ׳ו ו השתחוו ל׳ו כל אלהים כי דם בני׳ו יקום ו נקם ישיב ל צרי׳ו ו ל משנאי׳ו ישלם ו יכפר אדמת עמ׳ו | lest i transkripsjon |

### Lesning c: LXX: lengre tekst

- Grunntekst: εὐφράνθητε, οὐρανοί, ἅμα αὐτῷ, καὶ προσκυνησάτωσαν αὐτῷ πάντες οἱ ἄγγελοι θεοῦ· εὐφράνθητε, ἔθνη, μετὰ τοῦ λαοῦ αὐτοῦ, καὶ ἐνισχυσάτωσαν αὐτῷ πάντες υἱοὶ θεοῦ· ὅτι τὸ αἷμα τῶν υἱῶν αὐτοῦ ἐκδικεῖται, καὶ ἐκδικήσει, καὶ ἀνταποδώσει δίκην τοῖς ἐχθροῖς· καὶ τοῖς μισοῦσιν ἀνταποδώσει δίκην, καὶ ἐκκαθαριεῖ Κύριος τὴν γῆν τοῦ λαοῦ αὐτοῦ.
- Ordrett norsk: «Gled dere, himler, sammen med ham, og alle Guds engler skal tilbe ham. Gled dere, folkeslag, sammen med hans folk, og alle Guds sønner skal styrke seg i ham. For hans sønners blod blir hevnet, og han skal hevne og gjengjelde fiendene med dom; dem som hater, skal han gjengjelde med dom, og Herren skal rense sitt folks land.» (ordrett)
- Form: Åtte ledd. Teksten er gjengitt etter Odae 2:43 hos Swete, der den er hel. Imperativ 3. person flertall i προσκυνησάτωσαν og ἐνισχυσάτωσαν.

- Oversettelse: **LXX Odae** Odae 2:43: καὶ προσκυνησάτωσαν αὐτῷ πάντες οἱ ἄγγελοι θεοῦ, «og alle Guds engler skal tilbe ham» (ordrett). Forelegg: kan ikke avgjøres. Status: lest i utgavens tekst.
- Oversettelse: **LXX** Deut 32:43: καὶ προσκυνησάτωσαν αὐτῷ ⟨…⟩ υἱοὶ ⟨…⟩. Forelegg: sannsynlig. Status: delvis lest. Den digitale Swete-teksten har OCR-tap i dette verset. ⟨…⟩ markerer tapene. Seks ledd er funnet i teksten, resten må leses i trykt utgave.

**Vitnemønster (regnet ut):** Q ≠ G ≠ M

**Variantart:** pluss (mekanisk grovsortering: pluss_minus_og_annet_ord) · **Betydningsgrad:** betydning

**Vurdering:** ikke vurdert. Egen fane i leseren.

**Filologisk notat.** Verset finnes i tre former. MT har fire ledd, og R10 følger MT. 4QDeutᑫ har seks ledd, og den greske teksten har åtte. De to lange formene er ikke like: rullen har «alle guder» der gresk har «Guds engler» og «Guds sønner». Den greske teksten er her gjengitt etter Odae 2:43 hos Swete, fordi den digitale Swete-teksten til 5 Mos 32:43 har tap. I 5 Mos-formen står «sønner» i tilbedelsesleddet, i Odae-formen «engler». Hebr 1,6 i R10 har ordlyden «Καὶ προσκυνησάτωσαν αὐτῷ πάντες ἄγγελοι Θεοῦ». Den er lik Odae 2:43 bortsett fra artikkelen οἱ. Etter planens regel er et NT-sitat som kan avledes av kjent gresk tekst, ikke et uavhengig vitne.

**Kryssreferanse:** Hebr 1,6, NT-sitat. Uavhengig vitne: nei. Plan 2.3 og punkt 3 i planens innledning: sitatet avviker ikke fra kjent gresk tekst utover artikkelen.

**Må kontrolleres mot kilde:**

- Sal 96:7 LXX er en annen mulig kilde for ordlyden i Hebr 1,6. Stedet er ikke hentet i Trinn 0.
- Swete-teksten til 5 Mos 32:43 må leses i trykt utgave før LXX-lesningen kan låses.

---

## 4. Sal 22,17 (vestlig: Sal 22,16)

`GT-PSA-022-017-01` · utkast

**MANTELEN (R10):** «For hunder har omringet meg, en flokk av ugjerningsmenn har sluttet seg om meg; som en løve er de over mine hender og mine føtter.»

**Ankerord:** כָּ֝אֲרִ֗י (ord 7, id 19dCM): lesningene gjelder disse ordene

**Adresse:** MT `Ps.22.17` ↔ lesernes `Psa.22.16` (vestlig Sal 22,16) · gresk Ps 21:17

### Lesning a: MT: «som en løve» · MANTELEN (R10)

- Grunntekst: כָּאֲרִי
- Ordrett norsk: «som en løve»
- Form: Preposisjon כְּ med artikkel + substantiv, maskulinum entall, absolutt form.
- Utgaver som har lesningen: MANTELEN (R10), MAM

| Håndskrift | Type | Datering | Sted | Har på stedet | Status |
|---|---|---|---|---|---|
| B19ᴬ (Codex Leningradensis) | kodeks | 1008–1010 |  | כארי ידי ורגלי | lest i transkripsjon |

### Lesning b: verbform med waw

- Grunntekst: כארו
- Ordrett norsk: «de har gravd» (ordrett: Hvis formen hører til en rot for «grave». BDB drøfter rot og betydning med forbehold.); «de har gjennomboret» (tolkende: Den tradisjonelle gjengivelsen i KJV og Bibelen 1930. Den tar stilling til hva gravingen betyr.)
- Form: Sluttbokstaven er waw, ikke jod. Formen leses som verb, 3. person flertall, qatal. Rot og betydning er omstridt.

| Håndskrift | Type | Datering | Sted | Har på stedet | Status |
|---|---|---|---|---|---|
| 5/6ḤevPs | rulle | Herodian | ETCBC-sted f8_9, linje 12 | כארו | lest i transkripsjon |

- Oversettelse: **LXX** Ps 21:17: ὤρυξαν, «de gravde» (ordrett). Forelegg: sannsynlig. Status: lest i utgavens tekst. Gresk har et verb i 3. person flertall. Det forutsetter en verbform i forelegget, ikke «som en løve».

### Lesning b2: verbform uten alef (usikker)

- Grunntekst: כר[ו]
- Ordrett norsk: «de har gravd» (ordrett)
- Form: Tre bokstaver, de to første usikre og den siste rekonstruert i transkripsjonen.

| Håndskrift | Type | Datering | Sted | Har på stedet | Status |
|---|---|---|---|---|---|
| 4QPsᶠ | rulle | Hasmonean | ETCBC-sted f1_2, linje 23–25 | כ?ר?[ו] (delvis rekonstruert) | lest i transkripsjon |

**Vitnemønster (regnet ut):** Q = G ≠ M

**Variantart:** leksikalsk (mekanisk grovsortering: leksikalsk_eller_morfologisk) · **Betydningsgrad:** betydning

**Vurdering:** ikke vurdert. Egen fane i leseren.

**Filologisk notat.** Lesningen og tolkningen holdes adskilt. MT har כָּאֲרִי, «som en løve», og R10 følger MT: «som en løve er de over mine hender og mine føtter». Verbet i R10-setningen er en norsk utfylling. Salmerullen fra Nahal Hever har כארו med waw, og Swetes greske tekst har ὤρυξαν, «de gravde». Derfor har lesning b to gjengivelser: den ordrette og den tradisjonelle. 4QPsᶠ har bare usikre bokstaver på stedet. Adressen er Sal 22,17 i MT og 22,16 i vestlig nummerering. I gresk er det Sal 21,17.

---

## 5. Sal 145,13

`GT-PSA-145-013-01` · utkast

**MANTELEN (R10):** «Ditt rike er et rike for alle tider, og ditt herredømme varer fra slekt til slekt.»

**Ankerord:** וָדֽוֹר׃ (ord 8, id 19tHU): tillegget står etter dette ordet

### Lesning a: MT: uten nun-linjen · MANTELEN (R10)

- Ordrett norsk: «(linjen står ikke i teksten)»
- Form: Akrostikonet går fra mem-linjen (v. 13) rett til samek-linjen (v. 14).
- Utgaver som har lesningen: MANTELEN (R10), MAM

| Håndskrift | Type | Datering | Sted | Har på stedet | Status |
|---|---|---|---|---|---|
| B19ᴬ (Codex Leningradensis) | kodeks | 1008–1010 |  | (linjen står ikke) | lest i transkripsjon |

### Lesning b: nun-linjen

- Grunntekst: נאמן אלוהים בדבריו וחסיד בכול מעשיו
- Ordrett norsk: «Trofast er Gud i sine ord og god i alle sine gjerninger.» (ordrett)
- Form: Nominalsetning i to ledd. Første ord begynner på nun. Gudsnavnet er אלוהים.

| Håndskrift | Type | Datering | Sted | Har på stedet | Status |
|---|---|---|---|---|---|
| 11QPsᵃ | rulle | ca. 30 - 50 C.E. | ETCBC-sted 17, linje 1–4 | נאמן אלוהים ב דברי׳ו ו חסיד ב כול מעשי׳ו | lest i transkripsjon |

- Oversettelse: **LXX** Ps 144:13a: πιστὸς Κύριος ἐν τοῖς λόγοις αὐτοῦ, καὶ ὅσιος ἐν πᾶσι τοῖς ἔργοις αὐτοῦ, «Trofast er Herren i sine ord, og hellig i alle sine gjerninger.» (ordrett). Forelegg: sannsynlig. Status: lest i utgavens tekst. Gresk har Κύριος der rullen har אלוהים. Det digitale datasettet fører linjen under v. 14.

**Vitnemønster (regnet ut):** Q = G ≠ M

**Variantart:** pluss (mekanisk grovsortering: pluss_minus) · **Betydningsgrad:** betydning

**Vurdering:** ikke vurdert. Egen fane i leseren.

**Filologisk notat.** Salmen følger alfabetet, og mellom mem-linjen og samek-linjen mangler nun-linjen i MT. R10 følger MT. 11QPsᵃ har en nun-linje, og Swetes greske tekst har linjen som 144:13a. De to er ikke like i gudsnavnet: rullen har «Gud», gresk «Herren». חסיד er gjengitt «god», slik R10 gjengir ordet i vers 17. R10-noten til verset omtaler de samme vitnene.

**Må kontrolleres mot kilde:**

- Et middelaldersk hebraisk håndskrift (Kennicott) og den syriske oversettelsen oppgis også å ha linjen. De er ikke avlest.

---

## 6. Mark 1,1

`NT-MRK-001-001-01` · utkast

**MANTELEN (R10):** «Begynnelsen på evangeliet om Jesus Kristus, Guds Sønn.»

**Ankerord:** υιου του θεου (ord 6–8 i verset): lesningene gjelder disse ordene

### Lesning a: υἱοῦ τοῦ θεοῦ · MANTELEN (R10)

- Grunntekst: υἱοῦ τοῦ θεοῦ
- Ordrett norsk: «Guds Sønn»
- Form: Substantiv, genitiv entall maskulinum + artikkel + substantiv, genitiv entall maskulinum.
- Utgaver som har lesningen: MANTELEN (R10), Robinson–Pierpont 2018

| Håndskrift | Type | Datering | Sted | Har på stedet | Status |
|---|---|---|---|---|---|
| A 02 | majuskel | 400–499 (V) | fol. 30r | ‾χυ ‾υυ του ‾θυ | lest i transkripsjon |
| K 017 | majuskel | 800–899 (IX) | fol. 82r | ‾χυ υιου του ‾θυ | lest i transkripsjon |
| Δ 037 | majuskel | 800–899 (IX) | INTF-side/blad 133 | ‾χυ ‾υυ του ‾θυ | lest i transkripsjon |
| Π 041 | majuskel | 800–899 (IX) | fol. 99r | ‾χυ ‾υυ του ‾θυ | lest i transkripsjon |
| 565 | minuskel | 800–899 (IX) | fol. 131r | ‾χυ υιου του ‾θυ | lest i transkripsjon |
| 892 | minuskel | 800–899 (IX) | fol. 114r | ‾χυ ‾υυ του ‾θυ | lest i transkripsjon |
| 1424 | minuskel | 800–999 (IX/X) | fol. 56r | ‾χυ ‾υυ του ‾θυ | lest i transkripsjon |
| 33 | minuskel | 900–999 (X) | fol. 114v | ‾χυ ‾υυ του ‾θυ | lest i transkripsjon |
| 700 | minuskel | 1000–1099 (XI) | fol. 092r | ‾χυ υιου του ‾θυ | lest i transkripsjon |
| 1 | minuskel | 1100–1199 (XII) | fol. 199r | ‾χυ υιου του ‾θυ | lest i transkripsjon |
| 13 | minuskel | 1100–1299 (XII/XIII) | fol. 042r | ‾χυ υιου του ‾θυ | lest i transkripsjon |

- Oversettelse: **Vulgata Clementina** Mark 1:1: Filii Dei, «Guds Sønn» (ordrett). Forelegg: kan ikke avgjøres. Status: lest i utgavens tekst. Latin har ingen artikkel og kan ikke skille mellom greske lesninger som bare avviker i artikkelen.
- Kirkefar: **Irenæus av Lyon, Adversus haereses** III.10.5 (CPG 1306, hovedvindu). sitat, latin. I oversettelse: «The beginning of the Gospel of Jesus Christ, the Son of God». Status: funnet i oversettelse. Latin har ingen artikkel og kan ikke skille mellom greske lesninger som bare avviker i artikkelen.
- Kirkefar: **Irenæus av Lyon, Adversus haereses** III.16.3 (CPG 1306, hovedvindu). sitat, latin. I oversettelse: «The beginning of the Gospel of Jesus Christ, the Son of God». Status: funnet i oversettelse. Latin har ingen artikkel og kan ikke skille mellom greske lesninger som bare avviker i artikkelen.

### Lesning b: υἱοῦ θεοῦ

- Grunntekst: υἱοῦ θεοῦ
- Ordrett norsk: «Guds Sønn» (ordrett: Norsk gjengivelse er lik lesning a.)
- Form: Samme ord uten artikkel.
- Utgaver som har lesningen: THGNT†, Tregelles†, NA28 (i hakeparentes)†

| Håndskrift | Type | Datering | Sted | Har på stedet | Status |
|---|---|---|---|---|---|
| ℵ 01 korr. 1 | majuskel | håndskriftet 300–399 (IV); korrektoren er senere og ikke datert i registeret | fol. 217v | ‾χυ ‾υυ ‾θυ | lest i transkripsjon |
| B 03 | majuskel | 300–399 (IV) | INTF-side/blad 1277 | ‾χυ υιου ‾θυ | lest i transkripsjon |
| D 05 | majuskel | 400–499 (V) | fol. 285v | ‾χρυ υιου ‾θυ | lest i transkripsjon |
| W 032 | majuskel | 400–499 (V) | INTF-side/blad 311 | ‾χυ υιου ‾θυ | lest i transkripsjon |
| L 019 | majuskel | 700–799 (VIII) | fol. 70v | ‾χυ ‾υυ ‾θυ | lest i transkripsjon |

### Lesning c: uten «Guds Sønn»

- Ordrett norsk: «(ordene står ikke)» (ordrett)
- Form: Verset slutter med Ἰησοῦ Χριστοῦ.
- Utgaver som har lesningen: Tischendorf 8, SBLGNT†, Westcott–Hort†

| Håndskrift | Type | Datering | Sted | Har på stedet | Status |
|---|---|---|---|---|---|
| ℵ 01* | majuskel | 300–399 (IV) | fol. 217v | ευαγγελιου ‾ιυ ‾χυ | lest i transkripsjon |
| Θ 038 | majuskel | 800–899 (IX) |  | ευαγγελιου ‾ιυ ‾χυ | lest i transkripsjon |
| 28 korr. | minuskel | håndskriftet 1000–1099 (XI); korrektoren er senere og ikke datert i registeret | fol. 84r | ευαγγελιου ‾ιυ ‾χυ | lest i transkripsjon |

- Kirkefar: **Irenæus av Lyon, Adversus haereses** III.11.8 (CPG 1306, hovedvindu). sitat, latin. I oversettelse: «The beginning of the Gospel of Jesus Christ, as it is written in Esaias the prophet». Status: funnet i oversettelse.
- Kirkefar: **Origenes, Contra Celsum** II.4 (CPG 1476, hovedvindu). sitat, gresk. Gresk utgavetekst: «ἀρχὴ τοῦ εὐαγγελίου Ἰησοῦ Χριστοῦ, ὡς γέγραπται». Status: lest i utgavens tekst. Navngitt Markus-sitat. Sønnsfrasen står ikke i sitatet. Et sitat er ikke et direkte vitne til ordlyden i et evangeliehåndskrift. Paul Koetschau (red.), Origenes Werke I (1899); Perseus Project / Trustees of Tufts University, CC BY-SA 4.0, https://creativecommons.org/licenses/by-sa/4.0/.
- Kirkefar: **Origenes, Commentarii in Iohannem** I.14 (ANF-inndeling) (CPG 1453, hovedvindu). sitat, gresk. I oversettelse: «The beginning of the Gospel of Jesus Christ.». Status: funnet i oversettelse.

**Vitnemønster (regnet ut):** TR = Byz; tidlige førstehender delt (a: 02; b: 03, 05, 032; c: 01)

**Variantart:** minus (mekanisk grovsortering: pluss_minus) · **Betydningsgrad:** betydning

**Vurdering:** ikke vurdert. Egen fane i leseren.

**Filologisk notat.** R10 følger Scrivener: «Guds Sønn» med artikkel foran θεοῦ. Robinson–Pierpont har det samme. Lesning b har de samme ordene uten artikkel og gir samme norske tekst. Lesning c har ikke ordene. Første hånd i Sinaiticus har ikke ordene, og en korrektor har lagt dem til uten artikkel. Irenæus er delt i oversettelsen: to steder har «Guds Sønn», ett har det ikke. Minuskel 1241 har ifølge transkripsjonen υἱοῦ τοῦ κυρίου og er ikke ført under noen av lesningene.

**Avvik mellom datasett:** TAGNT fører opp NA28 i utgavefeltet for artikkelen τοῦ, mens ordtypen i samme rad og Robinson–Pierponts variantnote sier at NA-teksten har [υἱοῦ θεοῦ] uten artikkel. NA28 er ført under lesning b etter variantnoten og må leses i utgaven.

---

## 7. Joh 1,18

`NT-JOH-001-018-01` · utkast

**MANTELEN (R10):** «Ingen har noen gang sett Gud. Den eneste Sønnen, som er i Faderens favn, han har gjort Gud kjent.»

**Ankerord:** ὁ μονογενὴς υἱός (ord 5–7 i verset): lesningene gjelder disse ordene

### Lesning a: ὁ μονογενὴς υἱός · MANTELEN (R10)

- Grunntekst: ὁ μονογενὴς υἱός
- Ordrett norsk: «Den eneste Sønnen»
- Form: Artikkel + adjektiv + substantiv, alle nominativ entall maskulinum.
- Utgaver som har lesningen: MANTELEN (R10), Robinson–Pierpont 2018, Tischendorf 8, THGNT†

| Håndskrift | Type | Datering | Sted | Har på stedet | Status |
|---|---|---|---|---|---|
| A 02 | majuskel | 400–499 (V) | fol. 66r | ο μονογενης υιος | lest i transkripsjon |
| C 04 korr. 3 | majuskel | håndskriftet 400–499 (V); korrektoren er senere og ikke datert i registeret | fol. 188r | ο μονογενης ‾υς | lest i transkripsjon |
| Δ 037 | majuskel | 800–899 (IX) | INTF-side/blad 319 | ο μονογενης ‾υς | lest i transkripsjon |
| Θ 038 | majuskel | 800–899 (IX) |  | ο μονογε νης υιος | lest i transkripsjon |

- Oversettelse: **Vulgata Clementina** John 1:18: unigenitus Filius, «den enbårne Sønn» (ordrett). Forelegg: kan ikke avgjøres. Status: lest i utgavens tekst. Latin viser «Sønn» mot «Gud», men ikke artikkelen.
- Kirkefar: **Irenæus av Lyon, Adversus haereses** III.11.6 (CPG 1306, hovedvindu). sitat, latin. I oversettelse: «the only-begotten Son of God, which is in the bosom of the Father». Status: funnet i oversettelse. Oversettelsen har «Son of God».
- Kirkefar: **Irenæus av Lyon, Adversus haereses** IV.20.6 (CPG 1306, hovedvindu). sitat, latin. I oversettelse: «the only-begotten Son, who is in the bosom of the Father». Status: funnet i oversettelse.
- Kirkefar: **Tertullian, Adversus Praxean** 15 (CPL 26, hovedvindu). sitat, latin. I oversettelse: «the only begotten Son, who is in the bosom of the Father». Status: funnet i oversettelse.
- Kirkefar: **Hippolyt av Roma, Contra Noetum** 5 (CPG 1902, hovedvindu). sitat, gresk. I oversettelse: «the only-begotten Son, which is in the bosom of the Father». Status: funnet i oversettelse.

### Lesning b: μονογενὴς θεός

- Grunntekst: μονογενὴς θεός
- Ordrett norsk: «den eneste Gud» (ordrett: Slik R10-noten gjengir lesningen formnært.); «den eneste, som er Gud» (tolkende: Forklarende gjengivelse fra R10-noten.)
- Form: Adjektiv + substantiv, nominativ entall maskulinum, uten artikkel.
- Utgaver som har lesningen: NA28†, SBLGNT†, Westcott–Hort†, Tregelles†

| Håndskrift | Type | Datering | Sted | Har på stedet | Status |
|---|---|---|---|---|---|
| 𝔓66 | papyrus | 200–225 (III (A)) | INTF-side/blad 2 | πωποται μ(ο)νογενης ‾θς (usikre bokstaver) | lest i transkripsjon |
| ℵ 01* | majuskel | 300–399 (IV) | fol. 247r | πωποτε μονογενης ‾θς | lest i transkripsjon |
| B 03* | majuskel | 300–399 (IV) | INTF-side/blad 1350 | πωποτε μονογενης ‾θς | lest i transkripsjon |
| C 04* | majuskel | 400–499 (V) | fol. 188r | πωποτε μονογενης ‾θς | lest i transkripsjon |

- Kirkefar: **Irenæus av Lyon, Adversus haereses** IV.20.11 (CPG 1306, hovedvindu). sitat, latin. I oversettelse: «The only-begotten God, which is in the bosom of the Father». Status: funnet i oversettelse. Latin har ingen artikkel og kan ikke skille mellom greske lesninger som bare avviker i artikkelen.
- Kirkefar: **Klemens av Alexandria, Stromata** V.12 (CPG 1377, hovedvindu). sitat, gresk. I oversettelse: «The only-begotten God, who is in the bosom of the Father». Status: funnet i oversettelse. Oversettelsen viser ikke om gresk har artikkel.
- Kirkefar: **Origenes, Commentarii in Iohannem** II.29 (ANF-inndeling) (CPG 1453, hovedvindu). sitat, gresk. I oversettelse: «the only-begotten God, who is in the bosom of the Father». Status: funnet i oversettelse. Oversettelsen viser ikke om gresk har artikkel.

### Lesning c: ὁ μονογενὴς θεός

- Grunntekst: ὁ μονογενὴς θεός
- Ordrett norsk: «den eneste Gud» (ordrett)
- Form: Som b, med artikkel.

| Håndskrift | Type | Datering | Sted | Har på stedet | Status |
|---|---|---|---|---|---|
| 𝔓75* | papyrus | 200–225 (III (A)) |  | ο μονογενης ‾θς | lest i transkripsjon |
| ℵ 01 korr. 2 | majuskel | håndskriftet 300–399 (IV); korrektoren er senere og ikke datert i registeret | fol. 247r | πωποτε ο μονογενης ‾θς | lest i transkripsjon |

**Vitnemønster (regnet ut):** TR = Byz; tidlige førstehender delt (a: 02; b: P66, 01, 03, 04; c: P75)

**Variantart:** leksikalsk (mekanisk grovsortering: leksikalsk_eller_morfologisk+pluss_minus_og_annet_ord) · **Betydningsgrad:** betydning

**Vurdering:** ikke vurdert. Egen fane i leseren.

**Filologisk notat.** R10 følger Scrivener: «Den eneste Sønnen». Robinson–Pierpont og Tischendorf har samme lesning, og TAGNT fører THGNT under den. De to tidligste papyrusene og første hånd i Sinaiticus, Vaticanus og Ephraemi har θεός, med eller uten artikkel. Alexandrinus har υἱός. I Ephraemi har en korrektor endret til υἱός, og i Sinaiticus har en korrektor lagt til artikkelen. Fedrene er delt, også innenfor samme verk hos Irenæus. Et latinsk eller oversatt sitat avgjør ikke den greske artikkelen. R10-noten til verset omtaler de samme hovedvitnene. Origenes, Contra Celsum II.71 (I s. 193): «μονογενής γε ὢν θεὸς». ANF har «the only-begotten Son, who is in the bosom of the Father». Denne greske parallellen har θεός med innskutte ord; den er ikke ført som støtte for a, b eller c. Paul Koetschau (red.), Origenes Werke I (1899); Perseus Project / Trustees of Tufts University, CC BY-SA 4.0, https://creativecommons.org/licenses/by-sa/4.0/. Kilde: kilder/belegg/origenes-koetschau.json#Orig-Cels@II.71.

**Må kontrolleres mot kilde:**

- Tatians, Klemens’ (Excerpta ex Theodoto) og Origenes’ øvrige sitater av verset må leses i kritiske utgaver før de registreres.
- THGNT-valget er belagt med én kilde (TAGNT) og bør leses i utgaven.

---

## 8. Apg 8,37

`NT-ACT-008-037-01` · utkast

**MANTELEN (R10):** «Og Filip sa: «Hvis du tror av hele hjertet, er det tillatt.» Og han svarte og sa: «Jeg tror at Jesus Kristus er Guds Sønn.»»

**Ankerord:** εἶπε … Χριστόν (ord 1–23 i verset): lesningene gjelder hele verset

### Lesning a: verset i Scriveners form · MANTELEN (R10)

- Grunntekst: εἶπε δὲ ὁ Φίλιππος Εἰ πιστεύεις ἐξ ὅλης τῆς καρδίας ἔξεστιν ἀποκριθεὶς δὲ εἶπε Πιστεύω τὸν υἱὸν τοῦ Θεοῦ εἶναι τὸν Ἰησοῦν Χριστόν
- Ordrett norsk: «Og Filip sa: «Hvis du tror av hele hjertet, er det tillatt.» Og han svarte og sa: «Jeg tror at Jesus Kristus er Guds Sønn.»»
- Form: Hele verset. Scrivener har ὁ Φίλιππος som subjekt og ikke σου etter καρδίας.
- Utgaver som har lesningen: MANTELEN (R10)

- Oversettelse: **Vulgata Clementina** Acts 8:37: Dixit autem Philippus: Si credis ex toto corde, licet. Et respondens ait: Credo Filium Dei esse Jesum Christum., «Og Filip sa: Hvis du tror av hele hjertet, er det tillatt. Og han svarte og sa: Jeg tror at Jesus Kristus er Guds Sønn.» (ordrett). Forelegg: kan ikke avgjøres. Status: lest i utgavens tekst. Clementina har «Philippus» og ikke «tuo», som Scrivener. Den viser at verset står i den trykte Vulgata, ikke hvilke håndskrifter som har det.
- Oversettelse: **Vetus Latina**. Forelegg: kan ikke avgjøres. Status: ikke avlest. Oppdraget nevner Vetus Latina som vitne. Ingen gammellatinsk tekst er hentet i Trinn 0.

### Lesning a2: verset i minuskelform

- Grunntekst: εἶπε δὲ αὐτῷ· εἰ πιστεύεις ἐξ ὅλης τῆς καρδίας σου, ἔξεστιν· ἀποκριθεὶς δὲ εἶπε· πιστεύω τὸν υἱὸν τοῦ θεοῦ εἶναι Ἰησοῦν Χριστόν
- Ordrett norsk: «Og han sa til ham: «Hvis du tror av hele ditt hjerte, er det tillatt.» Og han svarte og sa: «Jeg tror at Jesus Kristus er Guds Sønn.»» (ordrett)
- Form: Som a, men med αὐτῷ og uten ὁ Φίλιππος. De fleste har σου. Tre av håndskriftene har ikke τῆς.

| Håndskrift | Type | Datering | Sted | Har på stedet | Status |
|---|---|---|---|---|---|
| 1739 | minuskel | 900–999 (X) | fol. 9v | ειπεν δε αυτω ει πιστευεις εξ ολης της καρδιας σου εξεστιν αποκριθεις δε ειπεν πιστευω τον ‾υν του ‾θυ ειναι ‾ιν ‾χν | lest i transkripsjon |
| 1891 | minuskel | 900–999 (X) | fol. 26v | ειπεν δε αυτωι ει πιστευεις εξ ολης της καρδιας σου εξεστιν αποκριθεις δε ειπε πιστευω τον υιον του ‾θυ ειναι ‾ιν ‾χν | lest i transkripsjon |
| 307 | minuskel | 900–999 (X) | fol. 70r | ειπεν δε αυτω ει πιστευεις εξ ολης καρδιας σου εξεστιν αποκριθεις δε ειπεν πιστευω τον υιον του ‾θυ ειναι ‾ιν ‾χν | lest i transkripsjon |
| 945 | minuskel | 1000–1099 (XI) | fol. 11v | ειπε δε αυτω· ει πιστευεις εξ ολης της καρδιας σου, εξεστιν· απο κριθεις δε ειπε· πιστευω τον υιον του ‾θυ ειναι, ‾ιν ‾χν· | lest i transkripsjon |
| 323 | minuskel | 1100–1199 (XII) | fol. 32v | ειπε δε αυτω ει πιστευεις εξ ο λης της καρδιας εξεστιν απο κριθεις δε ειπε πιστευω τον ‾υν του ‾θυ ειναι ‾ιν ‾χν | lest i transkripsjon |
| 2818 | minuskel | 1100–1199 (XII) | fol. 59r | ειπε δε αυτω ει πιστευεις εξ ολης καρδιας σου εξεστιν αποκρι θεις δε ειπε πιστευω τον υιον του ‾θυ ειναι ‾ιν ‾χν | lest i transkripsjon |
| 453 | minuskel | 1300–1399 (XIV) | fol. 88r | ειπε δε αυτω ει πιστευεις εξ ολης καρδιας σου εξε στιν αποκριθεις δε ειπε πιστευω τον υιον του ‾θυ ειναι ‾ιν ‾χν | lest i transkripsjon |

- Kirkefar: **Irenæus av Lyon, Adversus haereses** III.12.8 (CPG 1306, hovedvindu). sitat, latin. I oversettelse: «I believe Jesus Christ to be the Son of God». Status: funnet i oversettelse. Irenæus gjengir bare hoffmannens bekjennelse, ikke Filips vilkår.
- Kirkefar: **Cyprian av Karthago, Ad Quirinum (Testimoniorum libri III)** III.43 (CPL 39, hovedvindu). sitat, latin. I oversettelse: «Then said Philip, If thou believest with all thine heart, thou mayest». Status: funnet i oversettelse. Cyprian gjengir v. 36 og Filips vilkår, ikke bekjennelsen.

### Lesning a3: verset i Laudianus’ form

- Grunntekst: εἶπεν δὲ αὐτῷ ὁ Φίλιππος· ἐὰν πιστεύεις ἐξ ὅλης τῆς καρδίας σου, σωθήσει· ἀποκριθεὶς δὲ εἶπεν· πιστεύω εἰς τὸν Χριστὸν τὸν υἱὸν τοῦ θεοῦ
- Ordrett norsk: «Og Filip sa til ham: «Hvis du tror av hele ditt hjerte, skal du bli frelst.» Og han svarte og sa: «Jeg tror på Kristus, Guds Sønn.»» (ordrett)
- Form: Annen ordlyd: ἐάν, σωθήσει (futurum passiv 2. person entall) og πιστεύω εἰς.

| Håndskrift | Type | Datering | Sted | Har på stedet | Status |
|---|---|---|---|---|---|
| E 08 | majuskel | 500–599 (VI) | fol. 70v | ειπεν δε αυτω ο φιλιππος εαν πιστευεις εξ ολης της καρδιας σου σωθησει αποκριθεις δε ειπεν πιστευω εις τον ‾χν τον υιον του ‾θυ | lest i transkripsjon |

### Lesning b: uten verset

- Ordrett norsk: «(verset står ikke)» (ordrett)
- Form: Teksten går fra v. 36 rett til v. 38.
- Utgaver som har lesningen: Robinson–Pierpont 2018, Tischendorf 8, NA28†, THGNT†, SBLGNT†, Westcott–Hort†, Tregelles†

| Håndskrift | Type | Datering | Sted | Har på stedet | Status |
|---|---|---|---|---|---|
| 𝔓45 | papyrus | 200–299 (III) | fol. 22r | (verset står ikke) (rekonstruert) | lest i transkripsjon |
| ℵ 01 | majuskel | 300–399 (IV) | fol. 304r | (verset står ikke) | lest i transkripsjon |
| B 03 | majuskel | 300–399 (IV) | INTF-side/blad 1394 | (verset står ikke) | lest i transkripsjon |
| A 02 | majuskel | 400–499 (V) | fol. 87r | (verset står ikke) | lest i transkripsjon |
| C 04 | majuskel | 400–499 (V) | fol. 182r | (verset står ikke) | lest i transkripsjon |
| 𝔓74 | papyrus | 600–699 (VII) | INTF-side/blad 55 | (verset står ikke) (delvis rekonstruert) | lest i transkripsjon |
| L 020 | majuskel | 800–899 (IX) | fol. 2r | (verset står ikke) | lest i transkripsjon |
| Ψ 044 | majuskel | 800–999 (IX/X) | fol. 116r | (verset står ikke) | lest i transkripsjon |
| 049 | majuskel | 900–999 (X) | fol. 14r | (verset står ikke) | lest i transkripsjon |
| 33 | minuskel | 900–999 (X) | fol. 80r | (verset står ikke) (delvis rekonstruert) | lest i transkripsjon |
| 1175 | minuskel | 900–999 (X) | fol. 21r | (verset står ikke) | lest i transkripsjon |
| 81 | minuskel | 1044 | fol. 14v | (verset står ikke) | lest i transkripsjon |
| 614 | minuskel | 1200–1299 (XIII) | fol. 26v | (verset står ikke) | lest i transkripsjon |
| 35 | minuskel | 1300–1399 (XIV) | fol. 170v | (verset står ikke) | lest i transkripsjon |
| 18 | minuskel | 1363–1364 (1363/4) | fol. 167v | (verset står ikke) | lest i transkripsjon |

**Vitnemønster (regnet ut):** TR ≠ Byz; Byz = tidlige førstehender

**Variantart:** pluss (mekanisk grovsortering: pluss_minus) · **Betydningsgrad:** betydning

**Vurdering:** ikke vurdert. Egen fane i leseren.

**Filologisk notat.** R10 følger Scrivener og har hele verset. Robinson–Pierpont har det ikke, og de andre utgavene har det heller ikke. Blant de transkriberte greske håndskriftene står verset i tre former, og ingen av dem har nøyaktig Scriveners ordlyd. Codex Laudianus fra 500-tallet er det eldste greske vitnet og har en egen form («skal du bli frelst»). Minusklene 1739 og 1891 fra 900-tallet har formen som ligger nærmest Scrivener. Irenæus og Cyprian gjengir hver sin del av verset. Begge er bare funnet i engelsk oversettelse, og begge skrev eller er overlevert på latin. Papyrus 45 er svært fragmentarisk her, så utelatelsen der bygger på utgiverens linjeberegning. Bezae mangler denne delen av Apostlenes gjerninger.

**Må kontrolleres mot kilde:**

- Minuskel 2816, som Erasmus brukte, har ingen publisert transkripsjon hos INTF. Margen der bør leses, fordi Scriveners ordlyd går tilbake til Erasmus.
- Vetus Latina-håndskriftene og Vulgata-håndskriftene må leses i utgavene før de registreres.

---

## 9. 1 Tim 3,16

`NT-1TI-003-016-01` · utkast

**MANTELEN (R10):** «Og uimotsigelig stort er gudsfryktens mysterium: Gud ble åpenbart i kjød, rettferdiggjort i ånd, sett av engler, forkynt blant folkeslagene, trodd i verden, tatt opp i herlighet.»

**Ankerord:** Θεὸς (ord 9 i verset): lesningene gjelder disse ordene

### Lesning a: Θεός · MANTELEN (R10)

- Grunntekst: Θεός
- Ordrett norsk: «Gud»
- Form: Substantiv, nominativ entall maskulinum. I majuskelskrift ΘΣ med strek over.
- Utgaver som har lesningen: MANTELEN (R10), Robinson–Pierpont 2018

| Håndskrift | Type | Datering | Sted | Har på stedet | Status |
|---|---|---|---|---|---|
| ℵ 01 korr. 3 | majuskel | håndskriftet 300–399 (IV); korrektoren er senere og ikke datert i registeret | fol. 294v | θεος | lest i transkripsjon |
| A 02 korr. | majuskel | håndskriftet 400–499 (V); korrektoren er senere og ikke datert i registeret | fol. 145r | ‾θς | lest i transkripsjon |
| C 04 korr. 3 | majuskel | håndskriftet 400–499 (V); korrektoren er senere og ikke datert i registeret | fol. 119r | ‾θς | lest i transkripsjon |
| D 06 korr. 2 | majuskel | håndskriftet 500–599 (VI); korrektoren er senere og ikke datert i registeret |  |  (ikke avlest) | ikke avlest |
| 6 | minuskel | 1200–1299 (XIII) | fol. 178r | ‾θς | lest i transkripsjon |

- Kirkefar: **Johannes Krysostomos, In epistulam I ad Timotheum homiliae** Hom. XI (CPG 4436, utenfor hovedvinduet). sitat, gresk. I oversettelse: «God was manifest in the flesh». Status: funnet i oversettelse.
- Kirkefar: **Gregor av Nyssa, Contra Eunomium** bok XI (NPNF-inndeling) (CPG 3135, utenfor hovedvinduet). sitat, gresk. I oversettelse: «God was manifest in the flesh, justified in the spirit». Status: funnet i oversettelse.

### Lesning b: ὅς

- Grunntekst: ὅς
- Ordrett norsk: «han som» (ordrett)
- Form: Relativpronomen, nominativ entall maskulinum. I majuskelskrift ΟΣ.
- Utgaver som har lesningen: Tischendorf 8, NA28†, THGNT†, SBLGNT†, Westcott–Hort†, Tregelles†

| Håndskrift | Type | Datering | Sted | Har på stedet | Status |
|---|---|---|---|---|---|
| ℵ 01* | majuskel | 300–399 (IV) | fol. 294v | ος | lest i transkripsjon |
| A 02* | majuskel | 400–499 (V) | fol. 145r | ος | lest i transkripsjon |
| C 04* | majuskel | 400–499 (V) | fol. 119r | ος | lest i transkripsjon |

### Lesning c: ὅ

- Grunntekst: ὅ
- Ordrett norsk: «det som» (ordrett)
- Form: Relativpronomen, nominativ entall nøytrum, som viser til μυστήριον.

| Håndskrift | Type | Datering | Sted | Har på stedet | Status |
|---|---|---|---|---|---|
| D 06* | majuskel | 500–599 (VI) |  |  (ikke avlest) | ikke avlest |

- Oversettelse: **Vulgata Clementina** I Timothy 3:16: quod manifestatum est, «det som ble åpenbart» (ordrett). Forelegg: kan ikke avgjøres. Status: lest i utgavens tekst. Latin har relativpronomen i nøytrum, som viser til sacramentum. Det utelukker «Gud», men viser ikke sikkert om forelegget hadde ὅ eller ὅς.

**Vitnemønster (regnet ut):** TR = Byz; tidlige førstehender har lesning b mot TR og Byz

**Variantart:** leksikalsk (mekanisk grovsortering: leksikalsk_eller_morfologisk) · **Betydningsgrad:** betydning

**Vurdering:** ikke vurdert. Egen fane i leseren.

**Filologisk notat.** R10 følger Scrivener: «Gud ble åpenbart i kjød». Robinson–Pierpont har samme lesning. I Sinaiticus, Alexandrinus og Ephraemi har første hånd ὅς, «han som», og en korrektor har endret til θεός i alle tre. I majuskelskrift skiller ΘΣ med strek seg fra ΟΣ med to streker. Minuskel 6 fra 1200-tallet er det eneste transkriberte håndskriftet med θεός i første hånd. De bysantinske majusklene har ingen publisert transkripsjon hos INTF. De to fedrene som er funnet med «Gud», er fra 300-tallet og ligger utenfor hovedvinduet. Ingen før-nikensk far er funnet med et ordrett sitat av stedet.

**Må kontrolleres mot kilde:**

- Oppdraget bruker betegnelsene ℵᵉ, A², C² og D². INTF-transkripsjonene kaller hendene korrektor 3 (01), korrektor (02) og korrektor 3 (04). Samsvaret mellom Tischendorfs, NA28s og INTFs korrektorbetegnelser må leses i utgavene.
- De bysantinske majusklene K 018, L 020, P 025 og Ψ 044 har ingen publisert transkripsjon av verset hos INTF og er derfor ikke registrert.
- Fedre som oppgis for ὅς i håndbøkene, må leses i kritiske utgaver før de registreres.
- Papyrus 133 har verset, men stedet er rekonstruert i transkripsjonen.

---

## 10. Åp 22,19

`NT-REV-022-019-01` · utkast

**MANTELEN (R10):** «Og hvis noen tar noe bort fra ordene i denne profetiens bok, skal Gud ta bort hans del fra livets bok og fra den hellige byen og fra de tingene som er skrevet i denne boken.»

**Ankerord:** βιβλου της ζωης (ord 19–21 i verset): lesningene gjelder disse ordene

### Lesning a: βίβλου τῆς ζωῆς · MANTELEN (R10)

- Grunntekst: βίβλου τῆς ζωῆς
- Ordrett norsk: «livets bok»
- Form: Substantiv, genitiv entall femininum + artikkel + substantiv, genitiv entall femininum.
- Utgaver som har lesningen: MANTELEN (R10)

- Oversettelse: **Vulgata Clementina** Revelation of John 22:19: de libro vitæ, «fra livets bok» (ordrett). Forelegg: kan ikke avgjøres. Status: lest i utgavens tekst. Latin har liber, «bok». Det latinske ordet for «tre» er lignum, og de to ordene ligner hverandre i genitiv og ablativ (libro, ligno).

### Lesning b: τοῦ ξύλου τῆς ζωῆς

- Grunntekst: τοῦ ξύλου τῆς ζωῆς
- Ordrett norsk: «livets tre» (ordrett)
- Form: Artikkel + substantiv, genitiv entall nøytrum + artikkel + substantiv, genitiv entall femininum.
- Utgaver som har lesningen: Robinson–Pierpont 2018, Tischendorf 8, NA28†, THGNT†, SBLGNT†, Westcott–Hort†, Tregelles†

| Håndskrift | Type | Datering | Sted | Har på stedet | Status |
|---|---|---|---|---|---|
| ℵ 01 | majuskel | 300–399 (IV) | fol. 333v | απο του ξυλου της ζωης | lest i transkripsjon |
| A 02 | majuskel | 400–499 (V) | fol. 158v | απο του ξυλου της ζωης | lest i transkripsjon |
| 1854 | minuskel | 900–999 (XI) | fol. 319v | απο του ξυλου της ζωης | lest i transkripsjon |
| 046 | majuskel | 900–999 (X) |  |  (ikke avlest) | ikke avlest |
| 1006 | minuskel | 1000–1099 (XI) | fol. 216v | απο του ξυλου της ζωης | lest i transkripsjon |
| 2050 | minuskel | 1107 | fol. 241r | απο του ξυλου της ζωης | lest i transkripsjon |
| 469 | minuskel | 1200–1299 (XIII) | fol. 229r | απο του ξυλου της ζωης | lest i transkripsjon |
| 35 | minuskel | 1300–1399 (XIV) | fol. 325v | απο του ξυλου της ζωης | lest i transkripsjon |

**Vitnemønster (regnet ut):** TR ≠ Byz; Byz = tidlige førstehender

**Variantart:** leksikalsk (mekanisk grovsortering: pluss_minus_og_annet_ord) · **Betydningsgrad:** betydning

**Vurdering:** ikke vurdert. Egen fane i leseren.

**Filologisk notat.** R10 følger Scrivener: «livets bok». Alle de transkriberte greske håndskriftene har «livets tre», også de to eldste, og Robinson–Pierpont har samme lesning. Scriveners lesning er her belagt i den latinske Clementina. Ingen gresk håndskrift med βίβλου er bekreftet i Trinn 0. Oppdraget nevner P (025) som vitne for «livets tre». INTFs sideindeks viser at håndskriftet slutter med Åp 22,2–6, så stedet er ikke bevart der. Ephraemi slutter i Åp 19,5.

**Utelukket vitne:** P 025. Lakune: siste indekserte side med Åpenbaringen er fol. 120v (Rev 22:2-6).

**Utelukket vitne:** C 04. Lakune: siste indekserte side med Åpenbaringen er fol. 123v (Rev 18:15-24; Rev 19:1-5).

**Må kontrolleres mot kilde:**

- Minusklene 296 og 2049 oppgis å ha βίβλου og å være avskrifter av trykte utgaver. Ingen av dem har publisert transkripsjon av stedet hos INTF.
- Latinske fedre som oppgis for «libro» (Ambrosius, De paradiso, CPL 124; Primasius, kommentaren til Åpenbaringen, CPL 873), er ikke avlest. Clavis-numrene er slått opp.
- Hvilke Vulgata-håndskrifter som har libro og hvilke som har ligno, leses i Stuttgart-utgavens apparat.

---

## Før enhetene kan låses

1. Begrensningene for hver kilde gjelder også etter Captains skriftlige godkjenning. Publisering av manuskriptlaget er ikke godkjent.
1. En navngitt leser leser de 45 opplysningene som ikke er lest i kilden: fedresitatene i kritisk utgave, NA28 og THGNT i utgavene, D 06 og 046 på bilde eller i utgave, Swete 5 Mos 32:43 i trykt utgave.
1. Uavklarte katalogfelt står åpne. Skill det fysiske håndskriftet fra verk, teksttradisjon og korrekturhånd.
1. Andre leser registrerer de ti enhetene uavhengig (plan 7.4), og samsvaret måles.
1. Pilotlisten følger Captains uttrykkelige bestilling. Overdommeren kan sette vurderinger i akse 3 etter dokumentert faglig gjennomgang.

† Utgavevalg merket med † er hentet fra et annet fritt datasett (TAGNT eller Robinson–Pierponts variantnoter). Utgaven selv er ikke avlest.

## Utskrift fra validatoren

```text
BESTÅTT  0. Bestilte pilotsteder, kildetillatelser og katalogfakta: 1 / 1
MANTELEN fase 2, Trinn 0: validering av 10 pilotsteder
R10-kilde: C:/Users/elias/Documents/ChatGPT/BIBELAPPLIKASJON/android/app/src/main/assets/r10

BESTÅTT     Uendret R10/R11.1-kildemanifest: 1 / 1
BESTÅTT  1. JSON Schema, pilotsteder: 10 / 10
BESTÅTT     JSON Schema, hele filen: 1 / 1
BESTÅTT  2. Ordankre mot låst R10/R11.1 (ord og SHA-256): 10 / 10
         GT: 5 ankre med w[].id, toveis adresse mtRef ↔ stepPublicationRef prøvd for 5. NT: 5 ankre med wordIndex + g + bookSha256.
BESTÅTT     Råanker i 1 Tim 3,16 (ord 9, Θεὸς, G2316): 1 / 1
BESTÅTT  3. Manuskriptsigla i vitneregister.json: 96 / 96
BESTÅTT     Patristiske referanser med Clavis-nummer i registeret: 16 / 16
BESTÅTT     Utgaver i kildelisenser.json: 61 / 61
         Uregistrerte sigla: 0. Andel registrert: 100 %.
BESTÅTT  4. Dateringer hentet fra register med SHA-256 (av 56 daterte oppslag): 56 / 56
BESTÅTT     Oppslag uten datering har merknad om hvor den skal hentes: 13 / 13
BESTÅTT     Dateringsfelt i pilotenhetene (skal være 0): 1 / 1
BESTÅTT  5. Belegg bak bekreftede vitner og utgaver: 141 / 141
BESTÅTT     Begge Origenes-steder; Joh 1,18 teller ikke som lesningsstøtte: 1 / 1
BESTÅTT  6. Vitnemønster og mekanisk variantart regnet ut på nytt: 10 / 10

Status for bekreftelsene (alle vitner og utgavefelt i de ti enhetene):
  BEKREFTET_ANKER             10
  BEKREFTET_I_OVERSETTELSE    15
  BEKREFTET_SEKUNDAERT        25
  BEKREFTET_TRANSKRIPSJON     79
  BEKREFTET_UTGAVETEKST       26
  DELVIS_BEKREFTET             1
  IKKE_AVLEST                  4
Vurdering (akse 3): 10 av 10 enheter står som «ikke vurdert». Dobbel registrering: ikke kjørt.
Åpne punkter før låsing: 45 opplysninger må leses i kilden av navngitt leser (ikke avlest, bare i oversettelse, delvis eller sekundært belagt).

RESULTAT: ALLE KONTROLLER BESTÅTT
```
