# 02 Andre Mosebok: pre-flight og tverrkorpuskontroll

Status: kontrollgrunnlag til overdommer og Captain. Ingen bibelfil, note, kø eller pakke er endret. Ingen bokgodkjenning, låsing, import eller publisering.

Laget 20.11.2026 av Claude Code (skyøkten) etter arbeidsordren «Mantelen GT og tverrkorpus (parallellkø med Codex)», oppgave 3.

## Les dette først: forutsetningen i ordren stemmer ikke

Ordren ber om klargjøring «før vi starter selve oversettelsen av 2. Mosebok». Prosjektets egne filer sier noe annet:

- `MANTELEN_GT_ARBEIDSINDEKS.md`: «Andre Mosebok | 1213 vers; godkjent og låst 12.11.26 | 142 enheter/40 kapitler; ikke publisert».
- `rapporter/gt-exodus-lasing-2026-11-12/lasekvittering.json`: `state: LOCKED_NOT_PUBLISHED`, 1 213 vers, 16 714 ordposter, 3 098 noter. Låsfil `MANTELEN_ANDRE_MOSEBOK_LOCKED.md`, registrert SHA-256 `8ca89ccb44ffed1a4f625a195bd2e61e59cd7e3406e758954e368e46a20c7643`.

Boken er altså oversatt, bokgodkjent av Captain og låst. Den kan ikke «startes» på nytt uten at Captain opphever låsen. Etter saksgangen i `rapporter/gt-claude-gemini-samkjoring-2026-11-20/SAMKJORING.md` går forslag som rører en låst bok først til overdommeren, deretter til Captain.

Dette dokumentet er derfor laget som et kontrollgrunnlag mot den låste boken, ikke som forarbeid til en ny oversettelse. Kildedelen (WLC, STEP, LXX, Scrivener, NT-ordlyd) står her. Sammenstillingen mot låst GT-ordlyd, med forslag i diff-tabell, står i en egen paritetsfil som ikke legges i det offentlige repoet, fordi GT ikke er publisert.

Tre andre avvik mellom ordren og kildene:

1. Ordren kaller 3.2 «de 14 ankrene», men lister 16. Alle 16 er behandlet.
2. Ordren forutsetter «tabernaklet» og «sammenkomstens telt» (TK-22). Den låste boken bruker andre ord; se paritetsfilen. MANTELEN NT har «telt» for σκηνή alle steder.
3. Ordren knytter «nådestol» til Rom 3,25. MANTELEN NT har «soningssted» der og «nådestolen» i Heb 9,5.

## Kilder brukt i denne kjøringen

| Kilde | Fil | SHA-256 | Festet ved |
|---|---|---|---|
| OSHB / WLC | `Exod.xml` | `04868367cdacb6ccdc61488e923e20f918172042e6437842a0621f63ac5b847f` | openscriptures/morphhb, commit db6c5c9b46b8f39346f10915ddb1a70dcd429901 |
| OSHB VerseMap | `VerseMap.xml` | `6cd269ca3dccef2cb944b9d9dd8afc950f929dab53a534f1268d23affa983163` | openscriptures/morphhb, commit db6c5c9b46b8f39346f10915ddb1a70dcd429901 |
| STEP TAHOT Gen-Deu | `TAHOT Gen-Deu - Translators Amalgamated Hebrew OT - STEPBible.org CC BY.txt` | `7763ef367bb0e6e1c1a95fb9b652e1d611b2481827611433e82abbf229216d70` | STEPBible/STEPBible-Data, commit 5de0a47f35f0fc13dfe1430d104e5db8a4285f9c |
| Swete LXX Exodus | `02.Exodus.txt` | `4bb3c26c12eca623d9a046a9555b64d02ece86395e80fd0771bd6a73da544b3f` | nathans/lxx-swete, commit 26bad3eb42bba98471d154c954e36a6f30a0279d |
| Scrivener 1894 (Robinson) | `RO.SCV` | `77a46cb1299660dded4b1ba04e9d2249469f801a44e3059c939715bb52885398` | byztxt/greektext-scrivener, commit 6049a43b135ed870f843b83eb6a04764fc796678 |

MANTELEN NT er lest fra offentlig leserdata (https://www.mantelen.no/assets/data/bibelen/, utgave MANTELEN NT 2026, revisjon nt-2026-10-13-velbehag-public210, hentet 20.11.2026).

## 3.1 Vers- og kapittelparitet

Maskinelt resultat: OSHB/WLC har 40 kapitler, 1213 vers og 16713 ordposter i 2. Mosebok. STEP/TAHOT har 1213 vers og 16713 ordrader. Ordantallet stemmer i alle vers (avvik: 0). TAHOTs engelske adresse stemmer med OSHB VerseMap i alle vers (avvik: 0).

### 3.1.1 Kapitler der verstallet avviker

| Kapittel | WLC (OSHB) | Vestlig (KJV, VerseMap) | Swete LXX (denne digitale utgaven) |
|---|---|---|---|
| 7 | 29 | 25 | 25 |
| 8 | 28 | 32 | 32 |
| 21 | 37 | 36 | 36 |
| 22 | 30 | 31 | 31 |
| Sum hele boken | 1213 | 1213 | 1160 |

Kapittel 20 har 26 vers i WLC og 26 i vestlig nummerering; det er ingen forskyvning i dekalogen i denne kilden.

### 3.1.2 Alle 63 forskjøvne vers

| WLC | Vestlig | Forskyvning | Første ord i WLC |
|---|---|---|---|
| 7,26-29 | 8,1-4 | kapittelgrense: 4 vers flyttet | וַיֹּ֤אמֶר יְהוָה֙ אֶל |
| 8,1-28 | 8,5-32 | versnummer +4 | וַיֹּ֣אמֶר יְהוָה֮ אֶל |
| 21,37-37 | 22,1-1 | kapittelgrense: 1 vers flyttet | כִּ֤י יִגְנֹֽב אִישׁ֙ |
| 22,1-30 | 22,2-31 | versnummer +1 | אִם בַּמַּחְתֶּ֛רֶת יִמָּצֵ֥א |

**Forslag til merkeregel** (til overdommer og Captain; ikke innført noe sted):

1. WLC-adressen er primær i alle GT-filer, slik den låste boken allerede gjør.
2. For de 63 versene i tabellen skrives enhver kryssreferanse, i GT-noter og i NT-noter, med begge adresser: «2 Mos 22,27 [22,28]». Hakeparentesen er alltid den vestlige adressen (KJV, Bibelen 1930 og de fleste norske og engelske utgaver).
3. Maskinlesbart føres to felt, `wlc` og `vestlig`. Validatoren bør avvise en henvisning til 2 Mos 7,26-29; 8,1-28; 21,37 eller 22,1-30 som bare har én adresse. Grunnen er at 8,1-28 og 22,1-30 finnes i begge systemer med ulikt innhold, så en enkel adresse kan ikke tolkes sikkert av verken leser eller verktøy.
4. LXX: Swete-utgaven som er brukt her, følger den vestlige inndelingen i kapittel 7-8 og 21-22. Rahlfs følger etter min kunnskap den hebraiske inndelingen på disse stedene; det er ikke kontrollert maskinelt i denne kjøringen og må festes mot utgaven før LXX-adresser skrives i noter. I kapittel 35-40 har LXX annen rekkefølge og annet omfang enn MT (denne Swete-filen har 1 160 vers mot 1 213), så LXX-adresser der kan aldri regnes ut; de må slås opp.

### 3.1.3 Hva MANTELEN NT gjør i dag i forskyvningssonene

NT-notene har 42 henvisninger til 2. Mosebok (skilletegn: «:» 42). Av disse faller 2 i kapitlene som er forskjøvet:

| NT-note | Henvisning slik den står | Sammenheng |
|---|---|---|
| Apg 23,1-5 | `2 Mos 22:28` | » og begrunner det med et skriftord om folkets hersker, fra 2 Mos 22:28. Svaret gjengis med den kunnskapen og begrunnelsen han selv oppgir. K |
| Luk 11,14-26 | `2 Mosebok 8:15` | nere i setningen. «Guds finger» minner om magikernes ord i 2 Mosebok 8:15 etter den hebraiske versinndelingen; KJV har samme sted i 8:19. Når J |

**Funn.** De to notene bruker hver sin nummerering. Noten ved Apg 23,5 skriver 22:28 (vestlig) uten merking; sitatet står i WLC 22,27, så henvisningen bommer med ett vers mot GT-leseren. Noten ved Luk 11,20 skriver 8:15, sier uttrykkelig at det er hebraisk inndeling, og gir KJV 8:19 ved siden av. Den siste er mønsteret merkeregelen over bygger på. NT er låst; dette føres som revisjonsforslag, ikke som rettelse. NT-notene bruker dessuten kolon (22:28), mens siteringsmønsteret i NT-indeksen bruker komma (Joh 3,16). Det hører til overdommerens oppgave 3 (henvisningsformat).

### 3.1.4 Dekalogen 2 Mos 20,1-17: vers, petucha (פ) og setuma (ס)

| Vers | Ord | Avsnittsmerke etter verset | Alternativ aksentuering (OSHB-noter) | Innledning |
|---|---|---|---|---|
| 20,1 | 7 | ס | 0 | וַיְדַבֵּ֣ר אֱלֹהִ֔ים אֵ֛ת |
| 20,2 | 9 | ingen | 4 | אָֽנֹכִ֖י יְהוָ֣ה אֱלֹהֶ֑יךָ |
| 20,3 | 7 | ingen | 4 | לֹֽ֣א יִהְיֶֽה לְךָ֛ |
| 20,4 | 16 | ingen | 13 | לֹֽ֣א תַֽעֲשֶׂ֨ה לְךָ֥ |
| 20,5 | 21 | ingen | 4 | לֹֽא תִשְׁתַּחֲוֶ֥ה לָהֶ֖ם |
| 20,6 | 6 | ס | 3 | וְעֹ֥שֶׂה חֶ֖סֶד לַאֲלָפִ֑ים |
| 20,7 | 17 | פ | 0 | לֹ֥א תִשָּׂ֛א אֶת |
| 20,8 | 5 | ingen | 4 | זָכ֛וֹר אֶת י֥וֹם |
| 20,9 | 6 | ingen | 5 | שֵׁ֤שֶׁת יָמִים֙ תַּֽעֲבֹ֔ד |
| 20,10 | 18 | ingen | 12 | וְי֨וֹם֙ הַשְּׁבִיעִ֔י שַׁבָּ֖ת |
| 20,11 | 26 | ס | 0 | כִּ֣י שֵֽׁשֶׁת יָמִים֩ |
| 20,12 | 15 | ס | 0 | כַּבֵּ֥ד אֶת אָבִ֖יךָ |
| 20,13 | 2 | ס | 2 | לֹ֖א תִּרְצָֽח |
| 20,14 | 2 | ס | 2 | לֹ֖א תִּנְאָֽף |
| 20,15 | 2 | ס | 2 | לֹ֖א תִּגְנֹֽב |
| 20,16 | 5 | ס | 0 | לֹֽא תַעֲנֶ֥ה בְרֵעֲךָ֖ |
| 20,17 | 15 | פ | 0 | לֹ֥א תַחְמֹ֖ד בֵּ֣ית |

### 3.1.5 Budrekkefølgen i NT (Scrivener 1894) mot WLC og LXX

Rekkefølgen er lest maskinelt av den greske teksten ved verbstammene. F = far og mor, D = drap, E = ekteskapsbrudd, S = stjele, V = falskt vitne, B = begjære, A = «snyt ikke» (μὴ ἀποστερήσῃς), N = elske nesten.

| Sted | Rekkefølge | MANTELEN NT (ordrett) |
|---|---|---|
| 2 Mos 20,12-17 WLC | F D E S V B | (GT, se paritetsfilen) |
| 2 Mos 20,12-17 LXX (Swete) | F E S D V B | Swete 20,13-15: ekteskapsbrudd, tyveri, drap. Vers 20,13 er skadet i den digitale kilden. |
| Matt 19,18-19 | D E S V F N | Mannen sier til ham: «Hvilke?» Men Jesus sa: «‘Du skal ikke drepe.’ ‘Du skal ikke begå ekteskapsbrudd.’ ‘Du skal ikke stjele.’ ‘Du skal ikke vitne falskt.’ ‘Hedre din far og mor.’ Og: ‘Du skal elske din neste som deg selv.’» |
| Mark 10,19 | E D S V A F | Du kjenner budene: Du skal ikke begå ekteskapsbrudd. Du skal ikke drepe. Du skal ikke stjele. Du skal ikke vitne falskt. Du skal ikke snyte noen. Hedre din far og mor.» |
| Luk 18,20 | E D S V F | Du kjenner budene: Du skal ikke begå ekteskapsbrudd. Du skal ikke drepe. Du skal ikke stjele. Du skal ikke vitne falskt. Hedre faren din og moren din.» |
| Rom 13,9 | E D S V B N | For dette: «Du skal ikke begå ekteskapsbrudd, du skal ikke drepe, du skal ikke stjele, du skal ikke vitne falskt, du skal ikke begjære», og om det finnes noe annet bud, sammenfattes det i dette ordet: «Du skal elske din neste som deg selv.» |
| Jak 2,11 | E D | For han som sa: «Du skal ikke begå ekteskapsbrudd», sa også: «Du skal ikke drepe.» Men hvis du ikke begår ekteskapsbrudd, men dreper, er du blitt en lovbryter. |

**Lesning.** WLC slik OSHB fører den, har 26 vers i kapittel 20. Budene i 20,13-16 står som fire egne vers, hvert avsluttet med setuma. Petucha står etter 20,7 og 20,17. OSHB har 55 noter om alternativ aksentuering i hele 2. Mosebok, og alle 55 står i 20,2-17. De gjenspeiler den doble kantillasjonen av dekalogen (øvre og nedre aksentrekke), ikke en annen ordlyd.

Bare Matt 19,18 har rekkefølgen drap, ekteskapsbrudd, tyveri, som WLC. Mark 10,19, Luk 18,20, Rom 13,9 og Jak 2,11 har ekteskapsbrudd før drap i Scrivener 1894. LXX (Swete) har ekteskapsbrudd, tyveri, drap. NT-rekkefølgen kan derfor ikke brukes til å kontrollere versrekkefølgen i 2 Mos 20, og GT skal ikke omordnes etter NT. Mark 10,19 har et ledd («snyt ikke») som ikke er et dekalogbud. Rom 13,9 har «du skal ikke vitne falskt» i Scrivener; leddet mangler i kritiske utgaver, så sammenligning mot andre norske oversettelser vil vise avvik der.

## 3.2 Direkte NT-sitatankre i 2. Mosebok

Hebraisk er OSHB/WLC. Den løpende glossen er STEP/TAHOTs engelske ordglosser satt etter hverandre; den er et kontrollgrunnlag, ikke en oversettelse. LXX er Swete etter First1KGreek. Den teksten er maskinlest og har synlige skannefeil. Den viser hvilken gresk ordlyd NT bygger på, men skal ikke siteres videre uten kontroll mot en kritisk utgave. Scrivener 1894 er Robinsons utgave, uten aksenter. MANTELEN NT er ordrett fra offentlig leserdata. Orddata (ord-ID, morfologi, TAHOT) står i vedlegget `02_2mosebok_PREFLIGHT_ORDDATA.md`.

### SK-01  Tornebusken: fedrenes Gud

| WLC | Hebraisk (OSHB) | STEP/TAHOT, løpende glosse | LXX (Swete) |
|---|---|---|---|
| 2 Mos 3,6 | וַיֹּ֗אמֶר אָנֹכִי֙ אֱלֹהֵ֣י אָבִ֔יךָ אֱלֹהֵ֧י אַבְרָהָ֛ם אֱלֹהֵ֥י יִצְחָ֖ק וֵאלֹהֵ֣י יַעֲקֹ֑ב וַיַּסְתֵּ֤ר מֹשֶׁה֙ פָּנָ֔יו כִּ֣י יָרֵ֔א מֵהַבִּ֖יט אֶל־הָאֱלֹהִֽים׃ | and he said I [am] [the] God of father your [the] God of Abraham [the] God of Isaac and [the] God of Jacob and he hid Moses face his for he was afraid from looking to <the> God | καὶ εἶπεν Ἐγώ εἰμι ὁ θεὸς τοῦ πατρός σου, θεὸς Ἀβραὰμ καὶ θεὸς Ἰσαὰκ καὶ θεὸς Ἰακώβ. ἀπέστρεψεν δὲ Μωυσῆς τὸ πρόσωπον αὐτοῦ. εὐλαβεῖτο γὰρ κατεμβλέψαι ἐνώπιον τοῦ θεοῦ. |

| NT-sted | Scrivener 1894 (uten aksenter) | MANTELEN NT (ordrett) |
|---|---|---|
| Matt 22,32 | εγω ειμι ο θεος αβρααμ και ο θεος ισαακ και ο θεος ιακωβ ουκ εστιν ο θεος θεος νεκρων αλλα ζωντων | ‘Jeg er Abrahams Gud og Isaks Gud og Jakobs Gud’? Gud er ikke de dødes Gud, men de levendes.» |
| Mark 12,26 | περι δε των νεκρων οτι εγειρονται ουκ ανεγνωτε εν τη βιβλω μωσεως επι της βατου ως ειπεν αυτω ο θεος λεγων εγω ο θεος αβρααμ και ο θεος ισαακ και ο θεος ιακωβ | Men om de døde, at de reises opp: Har dere ikke lest i Mose bok, i avsnittet om tornebusken, hvordan Gud talte til ham og sa: 'Jeg er Abrahams Gud og Isaks Gud og Jakobs Gud'? |
| Luk 20,37 | οτι δε εγειρονται οι νεκροι και μωσης εμηνυσεν επι της βατου ως λεγει κυριον τον θεον αβρααμ και τον θεον ισαακ και τον θεον ιακωβ | Men at de døde blir reist opp, kunngjorde også Moses i avsnittet om tornebusken, der han kaller Herren Abrahams Gud og Isaks Gud og Jakobs Gud. |
| Apg 3,13 | ο θεος αβρααμ και ισαακ και ιακωβ ο θεος των πατερων ημων εδοξασεν τον παιδα αυτου ιησουν ον υμεις παρεδωκατε και ηρνησασθε αυτον κατα προσωπον πιλατου κριναντος εκεινου απολυειν | Abrahams og Isaks og Jakobs Gud, våre fedres Gud, herliggjorde sin tjener Jesus. Ham overga dere og fornektet overfor Pilatus, enda Pilatus hadde besluttet å løslate ham. |
| Apg 7,32 | εγω ο θεος των πατερων σου ο θεος αβρααμ και ο θεος ισαακ και ο θεος ιακωβ εντρομος δε γενομενος μωσης ουκ ετολμα κατανοησαι | 'Jeg er dine fedres Gud, Abrahams Gud og Isaks Gud og Jakobs Gud.' Men Moses begynte å skjelve og våget ikke å se nærmere. |

**Kildeforhold.** MT har ikke «og» foran Isak; LXX og NT har καί foran både Isak og Jakob. MT har «din fars Gud» i entall; Apg 7,32 har «dine fedres Gud» og Apg 3,13 «våre fedres Gud». Matt 22,32 har ἐγώ εἰμι, Mark 12,26 og Apg 7,32 bare ἐγώ. Dette er tekstforskjeller og skal stå. NT-internt varierer anførselstegnene mellom ‘...’ (Matt) og '...' (Mark, Apg).

### SK-02  Navnet: «Jeg er»

| WLC | Hebraisk (OSHB) | STEP/TAHOT, løpende glosse | LXX (Swete) |
|---|---|---|---|
| 2 Mos 3,14 | וַיֹּ֤אמֶר אֱלֹהִים֙ אֶל־מֹשֶׁ֔ה אֶֽהְיֶ֖ה אֲשֶׁ֣ר אֶֽהְיֶ֑ה וַיֹּ֗אמֶר כֹּ֤ה תֹאמַר֙ לִבְנֵ֣י יִשְׂרָאֵ֔ל אֶֽהְיֶ֖ה שְׁלָחַ֥נִי אֲלֵיכֶֽם׃ | and he said God to Moses I am [that] which I am and he said thus you will say to [the] people of Israel I am he has sent me to you | καὶ εἶπεν ὁ θεὸς πρὸς Μωυσῆν λέγων Ἐγώ εἰμι ὁ ὤν· καὶ εἶπεν Οὕτως ἐρεῖς τοῖς υἱοῖς Ἰσραήλ Ὁ ὢν ἀπέσταλκέν με πρὸς ὑμᾶς. |

| NT-sted | Scrivener 1894 (uten aksenter) | MANTELEN NT (ordrett) |
|---|---|---|
| Joh 8,58 | ειπεν αυτοις ο ιησους αμην αμην λεγω υμιν πριν αβρααμ γενεσθαι εγω ειμι | Jesus sa til dem: «Sannelig, sannelig sier jeg dere: Før Abraham ble til, er jeg.» |
| Åp 1,4 | ιωαννης ταις επτα εκκλησιαις ταις εν τη ασια χαρις υμιν και ειρηνη απο του ο ων και ο ην και ο ερχομενος και απο των επτα πνευματων α εστιν ενωπιον του θρονου αυτου | Johannes til de syv menighetene i Asia: Nåde være med dere og fred fra ham som er og som var og som kommer, og fra de syv åndene som er foran hans trone, |
| Åp 1,8 | εγω ειμι το α και το ω αρχη και τελος λεγει ο κυριος ο ων και ο ην και ο ερχομενος ο παντοκρατωρ | «Jeg er Alfa og Omega, begynnelsen og enden», sier Herren, han som er og som var og som kommer, Den Allmektige. |

**Kildeforhold.** MT אֶהְיֶה אֲשֶׁר אֶהְיֶה er qal imperfektum, 1. person. LXX har Ἐγώ εἰμι ὁ ὤν og bruker ὁ ὤν alene i siste ledd. Joh 8,58 har ἐγώ εἰμι uten predikat. Åp 1,4.8 har ὁ ὢν καὶ ὁ ἦν καὶ ὁ ἐρχόμενος, som bygger på LXX-formen ὁ ὤν. Dette er en allusjonskjede, ikke et ordrett sitat, og NT-ordlyden kan ikke styre gjengivelsen av אֶהְיֶה. Kontrollpunkt for studiepanelet: Joh 8,58 og Åp 1,4.8 bør nevnes sammen med LXX-formen.

### SK-03  Farao reist opp

| WLC | Hebraisk (OSHB) | STEP/TAHOT, løpende glosse | LXX (Swete) |
|---|---|---|---|
| 2 Mos 9,16 | וְאוּלָ֗ם בַּעֲב֥וּר זֹאת֙ הֶעֱמַדְתִּ֔יךָ בַּעֲב֖וּר הַרְאֹתְךָ֣ אֶת־כֹּחִ֑י וּלְמַ֛עַן סַפֵּ֥ר שְׁמִ֖י בְּכָל־הָאָֽרֶץ׃ | and but for sake of this I have caused to stand you in order to see you <obj.> power my and so as to recount name my in all the earth | καὶ ἕνεκεν τούτου διετηρήθης ἵνα ἐνδείξωμαι ἐν σοὶ τὴν ἰσχύν μου, καὶ ὅπως διαγγελῇ τὸ ὄνομά μου ἐν πάσῃ τῇ γῇ. |

| NT-sted | Scrivener 1894 (uten aksenter) | MANTELEN NT (ordrett) |
|---|---|---|
| Rom 9,17 | λεγει γαρ η γραφη τω φαραω οτι εις αυτο τουτο εξηγειρα σε οπως ενδειξωμαι εν σοι την δυναμιν μου και οπως διαγγελη το ονομα μου εν παση τη γη | For Skriften sier til farao: «Til nettopp dette reiste jeg deg opp, for at jeg skulle vise min kraft i deg, og for at mitt navn skulle bli forkynt over hele jorden.» |

**Kildeforhold.** MT הֶעֱמַדְתִּיךָ er hifil av עמד, «latt deg stå». LXX har passiv διετηρήθης, «du ble spart». Rom 9,17 har aktiv ἐξήγειρά σε, «jeg reiste deg opp», og δύναμιν der LXX har ἰσχύν. Paulus følger altså verken MT eller LXX ordrett i første ledd. MT הַרְאֹתְךָ er «la deg se»; LXX og Paulus har ἐνδείξωμαι ἐν σοί, «vise i deg». Felles ledd som kan samstemmes: «for at mitt navn skal bli forkynt over hele jorden».

### SK-04  Påskelammets bein

| WLC | Hebraisk (OSHB) | STEP/TAHOT, løpende glosse | LXX (Swete) |
|---|---|---|---|
| 2 Mos 12,46 | בְּבַ֤יִת אֶחָד֙ יֵאָכֵ֔ל לֹא־תוֹצִ֧יא מִן־הַבַּ֛יִת מִן־הַבָּשָׂ֖ר ח֑וּצָה וְעֶ֖צֶם לֹ֥א תִשְׁבְּרוּ־בֽוֹ׃ | in a house one it will be eaten not you will bring out from the house any of the meat [the] outside towards and a bone not you will break in <the> it | ἐν οἰκίᾳ μιᾷ βρωθήσεται, καὶ οὐκ ἐξοίσετε ἐκ τῆς οἰκίας τῶν κρεῶν ἵξω, καὶ ὀστοῦν οὐ συντρίψετε ἀπ’ αὐτοῦ. |

| NT-sted | Scrivener 1894 (uten aksenter) | MANTELEN NT (ordrett) |
|---|---|---|
| Joh 19,36 | εγενετο γαρ ταυτα ινα η γραφη πληρωθη οστουν ου συντριβησεται αυτου | For dette skjedde for at Skriften skulle bli oppfylt: «Ikke en knokkel på ham skal bli knust.» |

**Kildeforhold.** MT har aktiv 2. person flertall, «dere skal ikke bryte». Joh 19,36 har passiv 3. person συντριβήσεται med αὐτοῦ, i formen nærmere Sal 34,21. Parallellsted: 4 Mos 9,12. Substantivet (עֶצֶם, ὀστοῦν) og verbet (שׁבר, συντρίβω) er felles og bør ha samme norske ord i begge korpus.

### SK-05  Den førstefødte helliges

| WLC | Hebraisk (OSHB) | STEP/TAHOT, løpende glosse | LXX (Swete) |
|---|---|---|---|
| 2 Mos 13,2 | קַדֶּשׁ־לִ֨י כָל־בְּכ֜וֹר פֶּ֤טֶר כָּל־רֶ֨חֶם֙ בִּבְנֵ֣י יִשְׂרָאֵ֔ל בָּאָדָ֖ם וּבַבְּהֵמָ֑ה לִ֖י הֽוּא׃ | consecrate to me every firstborn [the] firstborn of every womb among [the] people of Israel among <the> humankind and among the livestock [belongs] to me it | Ἁγίασόν μοι πᾶν πρωτότοκον πρωτογενὲς διανοῖγον πᾶσαν μήτραν ἐν τοῖς υἱοῖς Ἰσραὴλ ἀπὸ ἀνθρώπου ἕως κτήνους· ἐμοί ἐστιν. |
| 2 Mos 13,12 | וְהַעֲבַרְתָּ֥ כָל־פֶּֽטֶר־רֶ֖חֶם לַֽיהֹוָ֑ה וְכָל־פֶּ֣טֶר ׀ שֶׁ֣גֶר בְּהֵמָ֗ה אֲשֶׁ֨ר יִהְיֶ֥ה לְךָ֛ הַזְּכָרִ֖ים לַיהוָֽה׃ | and you will dedicate every firstborn of a womb to Yahweh and every firstborn of [the] offspring of cattle which it will be[long] to you the males [will belong] to Yahweh | καὶ ἀφελεῖς πᾶν διανοῖγον μήτραν, τὰ ἀρσενικά, τῷ κυρίῳ· πᾶν διανοῖγον μήτραν ἐκ τῶν βουκολίων ἢ ἐν τοῖς κτήνεσίν σου ὅσα ἐὰν γένηται σοι, τὰ ἀρσενικὰ ἁγιάσεις τῷ κυρίῳ. |

| NT-sted | Scrivener 1894 (uten aksenter) | MANTELEN NT (ordrett) |
|---|---|---|
| Luk 2,23 | καθως γεγραπται εν νομω κυριου οτι παν αρσεν διανοιγον μητραν αγιον τω κυριω κληθησεται | slik det er skrevet i Herrens lov: «Alt mannkjønn som åpner morslivet, skal kalles hellig for Herren», |

**Kildeforhold.** Luk 2,23 er et sammensatt sitat. πᾶν ἄρσεν διανοῖγον μήτραν svarer til 13,12 (הַזְּכָרִים) og 13,2 (פֶּטֶר כָּל־רֶחֶם). «Skal kalles hellig for Herren» står ikke ordrett noe sted i 2. Mosebok. Felles ledd som kan samstemmes: «åpner morslivet».

### SK-06  Brød fra himmelen

| WLC | Hebraisk (OSHB) | STEP/TAHOT, løpende glosse | LXX (Swete) |
|---|---|---|---|
| 2 Mos 16,4 | וַיֹּ֤אמֶר יְהוָה֙ אֶל־מֹשֶׁ֔ה הִנְנִ֨י מַמְטִ֥יר לָכֶ֛ם לֶ֖חֶם מִן־הַשָּׁמָ֑יִם וְיָצָ֨א הָעָ֤ם וְלָֽקְטוּ֙ דְּבַר־י֣וֹם בְּיוֹמ֔וֹ לְמַ֧עַן אֲנַסֶּ֛נּוּ הֲיֵלֵ֥ךְ בְּתוֹרָתִ֖י אִם־לֹֽא׃ | and he said Yahweh to Moses here I [am] about to rain down for <the> you bread from the heavens and it will go out the people and they will gather a matter of a day in day its so that I should put to [the] test it ¿ will it walk in law my or? not | εἶπεν δὲ κύριος πρὸς Μωυσῆν ἰδοὺ ἐγὼ ὕω ὑμῖν ἄρτους ἐκ τοῦ οὐρανοῦ, καὶ ἐξελεύσεται ὁ λαὸς καὶ συλλέξουσιν τὸ τῆς ἡμέραν εἰς ἡμέραν, ὅπως πειράσω αὐτοὺς εἰ πορεύσονται τῷ νόμῳ μου ἢ οὔ· |
| 2 Mos 16,15 | וַיִּרְא֣וּ בְנֵֽי־יִשְׂרָאֵ֗ל וַיֹּ֨אמְר֜וּ אִ֤ישׁ אֶל־אָחִיו֙ מָ֣ן ה֔וּא כִּ֛י לֹ֥א יָדְע֖וּ מַה־ה֑וּא וַיֹּ֤אמֶר מֹשֶׁה֙ אֲלֵהֶ֔ם ה֣וּא הַלֶּ֔חֶם אֲשֶׁ֨ר נָתַ֧ן יְהוָ֛ה לָכֶ֖ם לְאָכְלָֽה׃ | and they saw [the] people of Israel and they said each to brother his what? [is] it for not they knew what? [was] it and he said Moses to them it [is] the bread which he has given Yahweh to <the> you to food | ἰδόντες δὲ αὐτὸ οἱ υἱοὶ Ἰσραὴλ εἶπαν ἕτερος τῷ ἑτέρῳ Τί ἐστιν τοῦτο; οὐ γὰρ ᾔδε’ ἴσαν τί ἦν. εἶπεν δὲ Μωυσῆς αὐτοῖς οὗτος ὁ ἄρτος ὃν ἕδωκεν κύριος ὑμῖν Φαγεῖν. |

| NT-sted | Scrivener 1894 (uten aksenter) | MANTELEN NT (ordrett) |
|---|---|---|
| Joh 6,31 | οι πατερες ημων το μαννα εφαγον εν τη ερημω καθως εστιν γεγραμμενον αρτον εκ του ουρανου εδωκεν αυτοις φαγειν | Fedrene våre spiste manna i ørkenen, slik det står skrevet: 'Brød fra himmelen ga han dem å spise.'» |

**Kildeforhold.** Joh 6,31 ligger i ordlyd nærmest Sal 78,24 (jf. Neh 9,15). 2 Mos 16,4 har לֶחֶם מִן־הַשָּׁמָיִם, og 16,15 «brødet som HERREN har gitt dere å spise». Felles ledd: «brød fra himmelen».

### SK-07  Manna: ikke for mye, ikke for lite

| WLC | Hebraisk (OSHB) | STEP/TAHOT, løpende glosse | LXX (Swete) |
|---|---|---|---|
| 2 Mos 16,18 | וַיָּמֹ֣דּוּ בָעֹ֔מֶר וְלֹ֤א הֶעְדִּיף֙ הַמַּרְבֶּ֔ה וְהַמַּמְעִ֖יט לֹ֣א הֶחְסִ֑יר אִ֥ישׁ לְפִֽי־אָכְל֖וֹ לָקָֽטוּ׃ | and they measured [it] by the omer and not he had a surplus the [one who] made much and the [one who] made little not he had a lack everyone to [the] mouth of food his they had gathered | καὶ μετρήσαντες τῷ γόμορ, οὐκ ἐπλεόνασεν ὁ τὸ πολύ, καὶ ὁ τὸ ἔλαττον οὐκ ἠλαττόνησεν· ἕκαστος εἰς τοὺς καθήκοντας παρ’ ἑαυτῷ συνέλεξαν. |

| NT-sted | Scrivener 1894 (uten aksenter) | MANTELEN NT (ordrett) |
|---|---|---|
| 2 Kor 8,15 | καθως γεγραπται ο το πολυ ουκ επλεονασεν και ο το ολιγον ουκ ηλαττονησεν | som det står skrevet: «Den som samlet mye, fikk ikke for mye, og den som samlet lite, fikk ikke for lite.» |

**Kildeforhold.** 2 Kor 8,15 følger LXX nesten ordrett (NT τὸ ὀλίγον, LXX τὸ ἔλαττον). MT har partisippene הַמַּרְבֶּה og הַמַּמְעִיט. Her er ordrett samsvar mellom GT og NT mulig.

### SK-08  Kongerike av prester

| WLC | Hebraisk (OSHB) | STEP/TAHOT, løpende glosse | LXX (Swete) |
|---|---|---|---|
| 2 Mos 19,5 | וְעַתָּ֗ה אִם־שָׁמ֤וֹעַ תִּשְׁמְעוּ֙ בְּקֹלִ֔י וּשְׁמַרְתֶּ֖ם אֶת־בְּרִיתִ֑י וִהְיִ֨יתֶם לִ֤י סְגֻלָּה֙ מִכָּל־הָ֣עַמִּ֔ים כִּי־לִ֖י כָּל־הָאָֽרֶץ׃ | and therefore <if> certainly [if] <to listen> you will listen to voice my and you will keep <obj.> covenant my and you will be of me a possession from all the peoples for [belongs] to <the> me all the earth | καὶ νῦν ἐὰν ἀκοῇ ἀκούσητε τῆς ἐμῆς φωνῆς καὶ φυλάξητε τὴν διαθήκην μου, ἔσεσθέ μοι λαὸς περιούσιος ἀπὸ πάντων τῶν ἐθνῶν· ἐμὴ γάρ ἐστιν πᾶσα ἡ γῆ, |
| 2 Mos 19,6 | וְאַתֶּ֧ם תִּהְיוּ־לִ֛י מַמְלֶ֥כֶת כֹּהֲנִ֖ים וְג֣וֹי קָד֑וֹשׁ אֵ֚לֶּה הַדְּבָרִ֔ים אֲשֶׁ֥ר תְּדַבֵּ֖ר אֶל־בְּנֵ֥י יִשְׂרָאֵֽל׃ | and you you will be for <the> me a kingdom of priests and a nation holy these [are] the words which you will speak to [the] people of Israel | ὑμεῖς δὲ ἔσεσθέ μοι βασίλειον ἱεράτευμα καὶ ἔθνος ἅγιον. ταῦτα τὰ ῥήματα ἐρεῖς τοῖς υἱοῖς Ἰσραήλ. |

| NT-sted | Scrivener 1894 (uten aksenter) | MANTELEN NT (ordrett) |
|---|---|---|
| 1 Pet 2,9 | υμεις δε γενος εκλεκτον βασιλειον ιερατευμα εθνος αγιον λαος εις περιποιησιν οπως τας αρετας εξαγγειλητε του εκ σκοτους υμας καλεσαντος εις το θαυμαστον αυτου φως | Men dere er en utvalgt slekt, et kongelig presteskap, et hellig folkeslag, et folk til Guds eiendom, for at dere skal forkynne hans storverk, han som kalte dere ut av mørket til sitt underfulle lys; |
| Åp 1,6 | και εποιησεν ημας βασιλεις και ιερεις τω θεω και πατρι αυτου αυτω η δοξα και το κρατος εις τους αιωνας των αιωνων αμην | og gjorde oss til konger og prester for sin Gud og Far, ham tilhører herligheten og veldet i evighetenes evigheter. Amen. |
| Åp 5,10 | και εποιησας ημας τω θεω ημων βασιλεις και ιερεις και βασιλευσομεν επι της γης | og gjorde oss til konger og prester for vår Gud; og vi skal regjere på jorden.» |

**Kildeforhold.** MT מַמְלֶכֶת כֹּהֲנִים er en konstruktforbindelse, «kongerike av prester». LXX har βασίλειον ἱεράτευμα, som 1 Pet 2,9 gjentar ordrett. Scrivener har βασιλεῖς καὶ ἱερεῖς i Åp 1,6 og 5,10, der kritiske utgaver har βασιλείαν. סְגֻלָּה (19,5) er i LXX λαὸς περιούσιος; 1 Pet 2,9 har λαὸς εἰς περιποίησιν. Det ordrette fellesleddet er גּוֹי קָדוֹשׁ = ἔθνος ἅγιον.

### SK-09  Fjellet som ikke må røres

| WLC | Hebraisk (OSHB) | STEP/TAHOT, løpende glosse | LXX (Swete) |
|---|---|---|---|
| 2 Mos 19,12 | וְהִגְבַּלְתָּ֤ אֶת־הָעָם֙ סָבִ֣יב לֵאמֹ֔ר הִשָּׁמְר֥וּ לָכֶ֛ם עֲל֥וֹת בָּהָ֖ר וּנְגֹ֣עַ בְּקָצֵ֑הוּ כָּל־הַנֹּגֵ֥עַ בָּהָ֖ר מ֥וֹת יוּמָֽת׃ | and you will set a boundary for <obj.> the people all around <to> saying take heed to <the> yourselves to go up on the mountain and to touch <in> edge its every <the> [one who] touches <in> the mountain certainly <to die> he will be put to death | καὶ ἀφοριεῖς τὸν λαὸν κύκλῳ λέγων Προσέχετε ἑαυτοῖς τοῦ ἀναβῆναι εἰς τὸ ὄρος καὶ θιγεῖν τι αὐτοῦ· πᾶς ὁ ἁψάμενος τοῦ ὄρους θανάτῳ τελευτήσει. |
| 2 Mos 19,13 | לֹא־תִגַּ֨ע בּ֜וֹ יָ֗ד כִּֽי־סָק֤וֹל יִסָּקֵל֙ אוֹ־יָרֹ֣ה יִיָּרֶ֔ה אִם־בְּהֵמָ֥ה אִם־אִ֖ישׁ לֹ֣א יִחְיֶ֑ה בִּמְשֹׁךְ֙ הַיֹּבֵ֔ל הֵ֖מָּה יַעֲל֥וּ בָהָֽר׃ | not it will touch <in> <the> him a hand for certainly <to stone> he will be stoned to death or certainly <to shot> he will be shot whether an animal or a human not it will live when sounds the ram's horn they they will go up on the mountain | οὐχ ἅψεται αὐτοῦ χείρ· ἐν γὰρ λίθοις λιθοβοληθήσεται ἢ βολίδι κατατοξευθήσεται· ἐάν τε κτῆνος ἐάν τε ἄνθρωπος, οὐ ζήσεται ὅταν αἱ φωναὶ καὶ αἱ σάλπιγγες καὶ ἡ νεφέλη ἀπέλθῃ ἀπὸ τοῦ ὄρους, ἐκεῖνοι ἀναβήσονται ἐπὶ τὸ ὄρος. |

| NT-sted | Scrivener 1894 (uten aksenter) | MANTELEN NT (ordrett) |
|---|---|---|
| Heb 12,20 | ουκ εφερον γαρ το διαστελλομενον καν θηριον θιγη του ορους λιθοβοληθησεται η βολιδι κατατοξευθησεται | for de kunne ikke bære det som ble befalt: «Om selv et dyr berører fjellet, skal det steines eller skytes gjennom med pil.» |

**Kildeforhold.** Heb 12,20 forkorter 19,12-13. Leddet ἢ βολίδι κατατοξευθήσεται står i Scrivener og i LXX, men mangler i kritiske NT-utgaver. For MANTELEN betyr det at NT og GT begge har leddet (MT יָרֹה יִיָּרֶה). θηρίον svarer til בְּהֵמָה.

### SK-10  Dekalogen, annen tavle

| WLC | Hebraisk (OSHB) | STEP/TAHOT, løpende glosse | LXX (Swete) |
|---|---|---|---|
| 2 Mos 20,12 | כַּבֵּ֥ד אֶת־אָבִ֖יךָ וְאֶת־אִמֶּ֑ךָ לְמַ֨עַן֙ יַאֲרִכ֣וּן יָמֶ֔יךָ עַ֚ל הָאֲדָמָ֔ה אֲשֶׁר־יְהוָ֥ה אֱלֹהֶ֖יךָ נֹתֵ֥ן לָֽךְ׃ ס | honor <obj.> father your and <obj.> mother your so that they may be long ! days your on the land which Yahweh God your [is] about to give to <the> you | Τίμα τὸν πατέρα σου καὶ τὴν μητέρα, ἴνα εὖ σοι γένηται, καὶ ἵνα μακροχρόνιος γένῃ ἐπὶ τῆς γῆς τῆς ἀγαθῆς ἧς κύριος ὁ θεός σου δίδωσίν σοι. |
| 2 Mos 20,13 | לֹ֖א תִּרְצָֽח׃ ס | not you must murder | Οὐ σεῖς. |
| 2 Mos 20,14 | לֹ֖א תִּנְאָֽף׃ ס | not you must commit adultery | Οὐ κλέψεις. (13) |
| 2 Mos 20,15 | לֹ֖א תִּגְנֹֽב׃ ס | not you must steal | Οὐ φονεύσεις. |
| 2 Mos 20,16 | לֹֽא־תַעֲנֶ֥ה בְרֵעֲךָ֖ עֵ֥ד שָֽׁקֶר׃ ס | not you must testify against neighbor your testimony of falsehood | Οὐ ψευδομαρτυρήσεις κατὰ τοῦ πλησίον σου μαρτυρίαν ψευδῆ. |
| 2 Mos 20,17 | לֹ֥א תַחְמֹ֖ד בֵּ֣ית רֵעֶ֑ךָ לֹֽא־תַחְמֹ֞ד אֵ֣שֶׁת רֵעֶ֗ךָ וְעַבְדּ֤וֹ וַאֲמָתוֹ֙ וְשׁוֹר֣וֹ וַחֲמֹר֔וֹ וְכֹ֖ל אֲשֶׁ֥ר לְרֵעֶֽךָ׃ פ | not you must covet [the] house of neighbor your not you must covet [the] wife of neighbor your and [male] servant his and female servant his and ox his and donkey his and all that [belongs] to neighbor your | Oὐκ ἔπι· θυμήσεις τὴν γυναῖκα τοῦ πλησίον σου· οὐκ ἐπιθυμήσεις τὴν οἰκίαν τοῦ πλησίον σου οὔτε τὸν ἀγρὸν αὐτοῦ, οὔτε τὸν παῖδα αὐτοῦ ούτε τὴν παιδίσκην αὐτοῦ, οὔτε τοῦ βοὸς αὐτοῦ οὔτε τοῦ ὑποζυγίου αὐτοῦ οὔτε παντὸς κτήνους αὐτοῦ, οὔτε ὅσα τῷ πλησίον σού ἐστιν. |

| NT-sted | Scrivener 1894 (uten aksenter) | MANTELEN NT (ordrett) |
|---|---|---|
| Matt 5,21 | ηκουσατε οτι ερρεθη τοις αρχαιοις ου φονευσεις ος δ αν φονευση ενοχος εσται τη κρισει | «Dere har hørt at det ble sagt til forfedrene: ‘Du skal ikke myrde’, og: ‘Den som myrder, skal stå til ansvar for domstolen.’ |
| Matt 5,27 | ηκουσατε οτι ερρεθη τοις αρχαιοις ου μοιχευσεις | «Dere har hørt at det ble sagt til forfedrene: ‘Du skal ikke begå ekteskapsbrudd.’ |
| Matt 15,4 | ο γαρ θεος ενετειλατο λεγων τιμα τον πατερα σου και την μητερα και ο κακολογων πατερα η μητερα θανατω τελευτατω | For Gud befalte og sa: ‘Hedre din far og din mor’, og: ‘Den som forbanner far eller mor, skal straffes med døden.’ |
| Matt 19,18 | λεγει αυτω ποιας ο δε ιησους ειπεν το ου φονευσεις ου μοιχευσεις ου κλεψεις ου ψευδομαρτυρησεις | Mannen sier til ham: «Hvilke?» Men Jesus sa: «‘Du skal ikke drepe.’ ‘Du skal ikke begå ekteskapsbrudd.’ ‘Du skal ikke stjele.’ ‘Du skal ikke vitne falskt.’ |
| Matt 19,19 | τιμα τον πατερα σου και την μητερα και αγαπησεις τον πλησιον σου ως σεαυτον | ‘Hedre din far og mor.’ Og: ‘Du skal elske din neste som deg selv.’» |
| Mark 10,19 | τας εντολας οιδας μη μοιχευσης μη φονευσης μη κλεψης μη ψευδομαρτυρησης μη αποστερησης τιμα τον πατερα σου και την μητερα | Du kjenner budene: Du skal ikke begå ekteskapsbrudd. Du skal ikke drepe. Du skal ikke stjele. Du skal ikke vitne falskt. Du skal ikke snyte noen. Hedre din far og mor.» |
| Luk 18,20 | τας εντολας οιδας μη μοιχευσης μη φονευσης μη κλεψης μη ψευδομαρτυρησης τιμα τον πατερα σου και την μητερα σου | Du kjenner budene: Du skal ikke begå ekteskapsbrudd. Du skal ikke drepe. Du skal ikke stjele. Du skal ikke vitne falskt. Hedre faren din og moren din.» |
| Rom 7,7 | τι ουν ερουμεν ο νομος αμαρτια μη γενοιτο αλλα την αμαρτιαν ουκ εγνων ει μη δια νομου την τε γαρ επιθυμιαν ουκ ηδειν ει μη ο νομος ελεγεν ουκ επιθυμησεις | Hva skal vi da si? Er loven synd? Må det aldri skje! Men det var bare gjennom loven jeg lærte synden å kjenne. For jeg ville heller ikke ha kjent begjæret dersom loven ikke hadde sagt: «Du skal ikke begjære.» |
| Rom 13,9 | το γαρ ου μοιχευσεις ου φονευσεις ου κλεψεις ου ψευδομαρτυρησεις ουκ επιθυμησεις και ει τις ετερα εντολη εν τουτω τω λογω ανακεφαλαιουται εν τω αγαπησεις τον πλησιον σου ως εαυτον | For dette: «Du skal ikke begå ekteskapsbrudd, du skal ikke drepe, du skal ikke stjele, du skal ikke vitne falskt, du skal ikke begjære», og om det finnes noe annet bud, sammenfattes det i dette ordet: «Du skal elske din neste som deg selv.» |
| Ef 6,2 | τιμα τον πατερα σου και την μητερα ητις εστιν εντολη πρωτη εν επαγγελια | «Ær din far og mor» (det er det første budet med løfte) |
| Ef 6,3 | ινα ευ σοι γενηται και εση μακροχρονιος επι της γης | «for at det skal gå deg godt, og du skal leve lenge på jorden.» |
| Jak 2,11 | ο γαρ ειπων μη μοιχευσης ειπεν και μη φονευσης ει δε ου μοιχευσεις φονευσεις δε γεγονας παραβατης νομου | For han som sa: «Du skal ikke begå ekteskapsbrudd», sa også: «Du skal ikke drepe.» Men hvis du ikke begår ekteskapsbrudd, men dreper, er du blitt en lovbryter. |

**Kildeforhold.** Rekkefølgen står i 3.1.5. Nøkkelord: τίμα (כַּבֵּד), οὐ φονεύσεις (לֹא תִרְצָח), οὐ μοιχεύσεις (לֹא תִנְאָף), οὐ κλέψεις (לֹא תִגְנֹב), οὐ ψευδομαρτυρήσεις (לֹא תַעֲנֶה ... עֵד שָׁקֶר), οὐκ ἐπιθυμήσεις (לֹא תַחְמֹד). Ef 6,3 siterer løftet etter LXX, med «for at det skal gå deg godt», som ikke står i 2 Mos 20,12 MT, men i 5 Mos 5,16.

**NT-internt funn.** Samme greske οὐ φονεύσεις er «Du skal ikke myrde» i Matt 5,21, men «Du skal ikke drepe» i Matt 19,18 og Rom 13,9; μὴ φονεύσῃς er «drepe» i Mark 10,19, Luk 18,20 og Jak 2,11. Samme greske τίμα er «Hedre» i evangeliene og «Ær» i Ef 6,2. Luk 18,20 har «faren din og moren din» der Matt 15,4 og Mark 7,10 har «din far og din mor» for samme greske ordlyd.

### SK-11  Den som forbanner far eller mor

| WLC | Hebraisk (OSHB) | STEP/TAHOT, løpende glosse | LXX (Swete) |
|---|---|---|---|
| 2 Mos 21,17 | וּמְקַלֵּ֥ל אָבִ֛יו וְאִמּ֖וֹ מ֥וֹת יוּמָֽת׃ ס | and [one who] will curse father his and mother his certainly <to die> he will be put to death | Ὁ κακολογῶν πατέρα αὐτοῦ ἢ μητέρα αὐτοῦ τελευτήσει θανάτῳ. (Swete 21,16) |

| NT-sted | Scrivener 1894 (uten aksenter) | MANTELEN NT (ordrett) |
|---|---|---|
| Matt 15,4 | ο γαρ θεος ενετειλατο λεγων τιμα τον πατερα σου και την μητερα και ο κακολογων πατερα η μητερα θανατω τελευτατω | For Gud befalte og sa: ‘Hedre din far og din mor’, og: ‘Den som forbanner far eller mor, skal straffes med døden.’ |
| Mark 7,10 | μωσης γαρ ειπεν τιμα τον πατερα σου και την μητερα σου και ο κακολογων πατερα η μητερα θανατω τελευτατω | For Moses sa: 'Hedre din far og din mor', og: 'Den som forbanner far eller mor, skal straffes med døden.' |

**Kildeforhold.** Swete har verset som 21,16, fordi LXX bytter om MT 21,16 og 21,17. מְקַלֵּל er i LXX og NT ὁ κακολογῶν. מוֹת יוּמָת (infinitiv absolutt + hofal) er θανάτῳ τελευτάτω i Matt 15,4 og Mark 7,10. Bokregel 19 låser hofal av מות til «drepes» i GT; NT-formen er en annen gresk vending og kan ikke kreves lik.

### SK-12  Høvdingen i folket

| WLC | Hebraisk (OSHB) | STEP/TAHOT, løpende glosse | LXX (Swete) |
|---|---|---|---|
| 2 Mos 22,27 [22,28] | אֱלֹהִ֖ים לֹ֣א תְקַלֵּ֑ל וְנָשִׂ֥יא בְעַמְּךָ֖ לֹ֥א תָאֹֽר׃ | God not you must curse and a leader among people your not you must curse | Θεοὺς οὐ κακολογήσεις, καὶ ἄρχοντας τοῦ λαοῦ σου οὐ κακῶς ἐρεῖς. (Swete 22,28) |

| NT-sted | Scrivener 1894 (uten aksenter) | MANTELEN NT (ordrett) |
|---|---|---|
| Apg 23,5 | εφη τε ο παυλος ουκ ηδειν αδελφοι οτι εστιν αρχιερευς γεγραπται γαρ αρχοντα του λαου σου ουκ ερεις κακως | Og Paulus sa: «Jeg visste ikke, brødre, at han er yppersteprest; for det står skrevet: ‘En hersker over ditt folk skal du ikke tale ondt om.’» |

**Kildeforhold.** WLC 22,27 er vestlig 22,28 og Swete 22,28. MT har entall נָשִׂיא; LXX har flertall ἄρχοντας; Apg 23,5 har entall ἄρχοντα, som MT. MT תָאֹר er «forbanne»; LXX og NT har κακῶς ἐρεῖς, «tale ondt». Ordren gjengir verset som «Du skal ikke tale ondt om en høvding i ditt folk». Den ordlyden står ikke i låst NT (se tabellen).

### SK-13  Paktens blod

| WLC | Hebraisk (OSHB) | STEP/TAHOT, løpende glosse | LXX (Swete) |
|---|---|---|---|
| 2 Mos 24,8 | וַיִּקַּ֤ח מֹשֶׁה֙ אֶת־הַדָּ֔ם וַיִּזְרֹ֖ק עַל־הָעָ֑ם וַיֹּ֗אמֶר הִנֵּ֤ה דַֽם־הַבְּרִית֙ אֲשֶׁ֨ר כָּרַ֤ת יְהוָה֙ עִמָּכֶ֔ם עַ֥ל כָּל־הַדְּבָרִ֖ים הָאֵֽלֶּה׃ | and he took Moses <obj.> the blood and he sprinkled [it] on the people and he said here! [the] blood of the covenant which he has made Yahweh with you on all the words <the> these | λαβὼν δὲ Μωυσῆς τὸ αἷμα κατεσκέδασεν τοῦ λαοῦ καὶ εἶπεν Ἴδου τὸ αἷμα τῆς διαθήκης ἧς διέθετο κύριος πρὸς ὑμᾶς περὶ πάντων τῶν λόγων τούτων. |

| NT-sted | Scrivener 1894 (uten aksenter) | MANTELEN NT (ordrett) |
|---|---|---|
| Heb 9,20 | λεγων τουτο το αιμα της διαθηκης ης ενετειλατο προς υμας ο θεος | og sa: «Dette er paktens blod, den pakten Gud påla dere.» |
| Matt 26,28 | τουτο γαρ εστιν το αιμα μου το της καινης διαθηκης το περι πολλων εκχυνομενον εις αφεσιν αμαρτιων | For dette er blodet mitt, den nye pakts blod, som blir utøst for mange til tilgivelse for syndene. |
| Mark 14,24 | και ειπεν αυτοις τουτο εστιν το αιμα μου το της καινης διαθηκης το περι πολλων εκχυνομενον | Og han sa til dem: «Dette er blodet mitt, den nye pakts blod, som blir utøst for mange. |
| Luk 22,20 | ωσαυτως και το ποτηριον μετα το δειπνησαι λεγων τουτο το ποτηριον η καινη διαθηκη εν τω αιματι μου το υπερ υμων εκχυνομενον | Likeså tok han også begeret etter måltidet og sa: «Dette begeret er den nye pakten i mitt blod, som blir utøst for dere. |
| 1 Kor 11,25 | ωσαυτως και το ποτηριον μετα το δειπνησαι λεγων τουτο το ποτηριον η καινη διαθηκη εστιν εν τω εμω αιματι τουτο ποιειτε οσακις αν πινητε εις την εμην αναμνησιν | Likeså tok han også begeret etter måltidet og sa: «Dette begeret er den nye pakten i mitt blod. Gjør dette, så ofte som dere drikker det, til minne om meg.» |

**Kildeforhold.** MT הִנֵּה דַם־הַבְּרִית er «se, paktens blod». Heb 9,20 har τοῦτο τὸ αἷμα, «dette er», som i nattverdordene. MT כָּרַת er LXX διέθετο; Heb 9,20 har ἐνετείλατο, «påla». MT יְהוָה er ὁ θεός i Heb 9,20. Matt 26,28 og Mark 14,24 har «den nye pakt» i Scrivener, der kritiske utgaver mangler «nye».

### SK-14  Mønsteret på fjellet

| WLC | Hebraisk (OSHB) | STEP/TAHOT, løpende glosse | LXX (Swete) |
|---|---|---|---|
| 2 Mos 25,40 | וּרְאֵ֖ה וַעֲשֵׂ֑ה בְּתַ֨בְנִיתָ֔ם אֲשֶׁר־אַתָּ֥ה מָרְאֶ֖ה בָּהָֽר׃ ס | and see and make [them] in pattern their which you [are] being shown on the mountain | πάντα τὰ σκεύη ταῦτα τάλαντον χρυσίου καθαροῦ. φόρα κατὰ τὸν τύπον τὸν δεδειγμένον σοι ἐν τῷ ὄρει. (Swete 25,39) |

| NT-sted | Scrivener 1894 (uten aksenter) | MANTELEN NT (ordrett) |
|---|---|---|
| Apg 7,44 | η σκηνη του μαρτυριου ην τοις πατρασιν ημων εν τη ερημω καθως διεταξατο ο λαλων τω μωση ποιησαι αυτην κατα τον τυπον ον εωρακει | Vitnesbyrdets telt var hos våre fedre i ødemarken, slik han som talte til Moses, befalte ham å lage det etter mønsteret han hadde sett. |
| Heb 8,5 | οιτινες υποδειγματι και σκια λατρευουσιν των επουρανιων καθως κεχρηματισται μωσης μελλων επιτελειν την σκηνην ορα γαρ φησιν ποιησης παντα κατα τον τυπον τον δειχθεντα σοι εν τω ορει | De gjør tjeneste ved et avbilde og en skygge av de himmelske tingene, slik Moses fikk guddommelig pålegg da han skulle fullføre teltet. For han sier: «Se til at du gjør alt etter det forbildet som ble vist deg på fjellet.» |

**Kildeforhold.** MT בְּתַבְנִיתָם er «etter mønsteret deres», med flertallssuffiks om gjenstandene. LXX og Heb 8,5 har κατὰ τὸν τύπον, og Heb 8,5 legger til πάντα. Swete har verset som 25,39, og den digitale teksten er skadet der.

**NT-internt funn.** τύπος er «forbildet» i Heb 8,5 og «mønsteret» i Apg 7,44.

### SK-15  Gullkalven

| WLC | Hebraisk (OSHB) | STEP/TAHOT, løpende glosse | LXX (Swete) |
|---|---|---|---|
| 2 Mos 32,1 | וַיַּ֣רְא הָעָ֔ם כִּֽי־בֹשֵׁ֥שׁ מֹשֶׁ֖ה לָרֶ֣דֶת מִן־הָהָ֑ר וַיִּקָּהֵ֨ל הָעָ֜ם עַֽל־אַהֲרֹ֗ן וַיֹּאמְר֤וּ אֵלָיו֙ ק֣וּם ׀ עֲשֵׂה־לָ֣נוּ אֱלֹהִ֗ים אֲשֶׁ֤ר יֵֽלְכוּ֙ לְפָנֵ֔ינוּ כִּי־זֶ֣ה ׀ מֹשֶׁ֣ה הָאִ֗ישׁ אֲשֶׁ֤ר הֶֽעֱלָ֨נוּ֙ מֵאֶ֣רֶץ מִצְרַ֔יִם לֹ֥א יָדַ֖עְנוּ מֶה־הָ֥יָה לֽוֹ׃ | and it saw the people that he delayed Moses to come down from the mountain and it assembled the people to Aaron and they said to him arise make for <the> us gods which they will go <to> before us for this Moses the man who he brought up us from [the] land of Egypt not we know what? has it happened to <the> him | Καὶ ἰδὼν ὁ λαὸς ὅτι κεχρόνικεν Μωυσῆς καταβῆναι ἐκ τοῦ ὄρους, συνέστη ὁ λαὸς ἐπὶ Ἀαρὼν καὶ λέγουσιν αὐτῷ Ἀνάστηθι καὶ ποίησον ἡμῖν θεοὺς οἳ προπορεύσονται ἡμῶν· ὁ γὰρ Μωσῆς οὗτος ὁ ἄνθρωπος ὅς ἐξήγαγεν ἡμᾶς ἐξ Αἰγύπτου, οὐκ οἴδαμεν τί γέγονεν αὐτῷ. |
| 2 Mos 32,6 | וַיַּשְׁכִּ֨ימוּ֙ מִֽמָּחֳרָ֔ת וַיַּעֲל֣וּ עֹלֹ֔ת וַיַּגִּ֖שׁוּ שְׁלָמִ֑ים וַיֵּ֤שֶׁב הָעָם֙ לֶֽאֱכֹ֣ל וְשָׁת֔וֹ וַיָּקֻ֖מוּ לְצַחֵֽק׃ פ | and they rose early from [the] next day and they offered up burnt offerings and they brought near peace offerings and it sat down the people to eat and to drink and they arose to play | καὶ ὀρθρίσας τῇ ἐπαύριον ἀνεβίβασεν ὁλοκαυτώματα, καὶ προσήνεγκεν θυσίαν σωτηρίου· καὶ ἐκάθισεν ὁ λαὸς Φαγεῖν καὶ πιεῖν, καὶ ἀνέστησαν παίζειν. |
| 2 Mos 32,23 | וַיֹּ֣אמְרוּ לִ֔י עֲשֵׂה־לָ֣נוּ אֱלֹהִ֔ים אֲשֶׁ֥ר יֵלְכ֖וּ לְפָנֵ֑ינוּ כִּי־זֶ֣ה ׀ מֹשֶׁ֣ה הָאִ֗ישׁ אֲשֶׁ֤ר הֶֽעֱלָ֨נוּ֙ מֵאֶ֣רֶץ מִצְרַ֔יִם לֹ֥א יָדַ֖עְנוּ מֶה־הָ֥יָה לֽוֹ׃ | and they said to <the> me make for <the> us gods which they will go <to> before us for this Moses the man who he brought up us from [the] land of Egypt not we know what? has it happened to <the> him | λέγουσιν γάρ γοι Ποίησον ἡμῖν θεοὺς οἵ προπορεύσονται ἡμῶν· ὁ γὰρ Μωυσῆς οὗτος ὁ ἄνθρωπος ὃς ἐξήγαγεν ἡμᾶς ἐξ Αἰγύπτου, οὐκ οἴδαμεν τί γέγονεν αὐτῷ. |

| NT-sted | Scrivener 1894 (uten aksenter) | MANTELEN NT (ordrett) |
|---|---|---|
| Apg 7,40 | ειποντες τω ααρων ποιησον ημιν θεους οι προπορευσονται ημων ο γαρ μωσης ουτος ος εξηγαγεν ημας εκ γης αιγυπτου ουκ οιδαμεν τι γεγονεν αυτω | og sa til Aron: 'Lag guder for oss som skal gå foran oss; for denne Moses, som førte oss ut av Egypts land, vet vi ikke hva som har skjedd med ham.' |
| 1 Kor 10,7 | μηδε ειδωλολατραι γινεσθε καθως τινες αυτων ως γεγραπται εκαθισεν ο λαος φαγειν και πιειν και ανεστησαν παιζειν | Bli heller ikke avgudsdyrkere, slik noen av dem ble. Som det er skrevet: «Folket satte seg ned for å spise og drikke, og de stod opp for å more seg.» |

**Kildeforhold.** Apg 7,40 følger LXX 32,1 og 32,23 tett. 1 Kor 10,7 gjengir LXX 32,6b ordrett. MT לְצַחֵק (piel av צחק) er LXX παίζειν. MT הֶעֱלָנוּ er «førte oss opp»; LXX og Apg har ἐξήγαγεν, «førte ut».

### SK-16  Nåde og barmhjertighet

| WLC | Hebraisk (OSHB) | STEP/TAHOT, løpende glosse | LXX (Swete) |
|---|---|---|---|
| 2 Mos 33,19 | וַיֹּ֗אמֶר אֲנִ֨י אַעֲבִ֤יר כָּל־טוּבִי֙ עַל־פָּנֶ֔יךָ וְקָרָ֧אתִֽי בְשֵׁ֛ם יְהוָ֖ה לְפָנֶ֑יךָ וְחַנֹּתִי֙ אֶת־אֲשֶׁ֣ר אָחֹ֔ן וְרִחַמְתִּ֖י אֶת־אֲשֶׁ֥ר אֲרַחֵֽם׃ | and he said I I will cause to pass by all goodness my on face your and I will proclaim <in> [the] name of Yahweh <to> before you and I will show favor to <obj.> [those] whom I will show favor and I will have compassion on <obj.> [those] whom I will have compassion | καὶ εἶπεν Ἐγὼ παρελεύσομαι πρότερός σου τῇ δόξῃ μου, καὶ λαλήσω ἐπὶ τῷ ὀνόματί μου κύριος ἐναντίον σου· καὶ ἐλεήσω ὅν ἄν ἐλεῶ, καὶ ὃν ἀν’ οἰκτείρω. |

| NT-sted | Scrivener 1894 (uten aksenter) | MANTELEN NT (ordrett) |
|---|---|---|
| Rom 9,15 | τω γαρ μωση λεγει ελεησω ον αν ελεω και οικτειρησω ον αν οικτειρω | For til Moses sier han: «Jeg skal forbarme meg over den jeg forbarmer meg over, og jeg skal ha medynk med den jeg har medynk med.» |

**Kildeforhold.** Rom 9,15 gjengir LXX ordrett. MT har to ulike røtter, חנן (være nådig) og רחם (vise barmhjertighet). LXX og Paulus har ἐλεέω og οἰκτείρω. Rekkefølgen og formen «den jeg ... , den jeg ...» er felles.

## 3.3 Kult-, tabernakel- og paktsterminologi (EX-TERM-01 til EX-TERM-20)

Tallene er lemmatreff i OSHB (Strong-nummer i lemmafeltet). Sammensatte uttrykk regnes som treff når leddene står i rekkefølge innen tre ord. EX-TERM-01 til 15 dekker de åtte punktene i ordren, med ett uttrykk per rad. EX-TERM-16 til 20 er mine tillegg for å fylle rekken til 20; de er merket «tillegg», og overdommeren kan bytte dem ut. Kolonnen «arbeidsetikett» er bare en merkelapp for raden, ikke låst ordlyd. Hvordan den låste boken faktisk gjengir termene, står i paritetsfilen.

| ID | Hebraisk | Strong | Treff | Vers | Kapitler (treff) | NT-gresk | Arbeidsetikett | Opphav |
|---|---|---|---|---|---|---|---|---|
| EX-TERM-01 | פֶּסַח (pesach) | H6453 | 6 | 6 | 12 (5), 34 (1) | τὸ πάσχα (G3957) | påske / påskeoffer | ordre |
| EX-TERM-02 | מַצָּה / מַצּוֹת (matsot) | H4682 | 16 | 12 | 12 (6), 13 (2), 23 (2), 29 (4), 34 (2) | τὰ ἄζυμα (G0106) | usyret brød | ordre |
| EX-TERM-03 | כַּפֹּרֶת (kapporet) | H3727 | 18 | 16 | 25 (7), 26 (1), 30 (1), 31 (1), 35 (1), 37 (5), 39 (1), 40 (1) | ἱλαστήριον (G2435) | nådestol (TK-08 ifølge ordren) | ordre |
| EX-TERM-04 | מִשְׁכָּן (mishkan) | H4908 | 58 | 55 | 25 (1), 26 (16), 27 (2), 35 (3), 36 (12), 38 (4), 39 (3), 40 (17) | σκηνή (G4633) | tabernakel / bolig (TK-22 ifølge ordren) | ordre |
| EX-TERM-05 | אֹהֶל מוֹעֵד (ohel moed) | H0168 + H4150 | 34 | 33 | 27 (1), 28 (1), 29 (7), 30 (5), 31 (1), 33 (2), 35 (1), 38 (2), 39 (2), 40 (12) | ἡ σκηνὴ τοῦ μαρτυρίου (G4633 + G3142) | sammenkomstens telt (TK-22 ifølge ordren) | ordre |
| EX-TERM-06 | עֵדוּת (edut) | H5715 | 21 | 20 | 16 (1), 25 (3), 26 (2), 27 (1), 30 (4), 31 (2), 32 (1), 34 (1), 38 (1), 39 (1), 40 (4) | τὸ μαρτύριον (G3142) | vitnesbyrdet (alle forekomster) | ordre |
| EX-TERM-07 | אֲרוֹן הָעֵדוּת (aron ha-edut) | H0727 + H5715 | 12 | 12 | 25 (3), 26 (2), 30 (2), 31 (1), 39 (1), 40 (3) | ἡ κιβωτὸς τοῦ μαρτυρίου | vitnesbyrdets ark | ordre |
| EX-TERM-08 | לֻחֹת הָעֵדוּת (luchot ha-edut) | H3871 + H5715 | 3 | 3 | 31 (1), 32 (1), 34 (1) | αἱ πλάκες τοῦ μαρτυρίου | vitnesbyrdets tavler | ordre |
| EX-TERM-09 | מִשְׁכַּן הָעֵדוּת (mishkan ha-edut) | H4908 + H5715 | 2 | 1 | 38 (2) | ἡ σκηνὴ τοῦ μαρτυρίου | vitnesbyrdets tabernakel | ordre |
| EX-TERM-10 | אֹהֶל הָעֵדוּת (ohel ha-edut) | H0168 + H5715 | 0 | 0 | ingen | ἡ σκηνὴ τοῦ μαρτυρίου | vitnesbyrdets telt | ordre |
| EX-TERM-11 | פָּרֹכֶת (parokhet) | H6532 | 15 | 13 | 26 (5), 27 (1), 30 (1), 35 (1), 36 (1), 38 (1), 39 (1), 40 (4) | τὸ καταπέτασμα (G2665) | forhenget (det indre) | ordre |
| EX-TERM-12 | מָסָךְ (masakh) | H4539 | 16 | 16 | 26 (2), 27 (1), 35 (3), 36 (1), 38 (1), 39 (3), 40 (5) | LXX: ἐπίσπαστρον / καταπέτασμα | teppet / forhenget ved inngangen | ordre |
| EX-TERM-13 | מִזְבַּח הָעֹלָה (mizbach ha-olah) | H4196 + H5930 | 9 | 9 | 29 (2), 30 (1), 31 (1), 35 (1), 38 (1), 40 (3) | τὸ θυσιαστήριον (G2379) | brennofferalteret | ordre |
| EX-TERM-14 | מִזְבַּח (מִקְטַר) הַקְּטֹרֶת (mizbach ha-qetoret) | H4196 + H7004 | 6 | 6 | 30 (2), 31 (1), 35 (1), 37 (1), 40 (1) | τὸ θυσιαστήριον τοῦ θυμιάματος (Luk 1,11) | røkelsesalteret | ordre |
| EX-TERM-15 | לֶחֶם (הַ)פָּנִים (lechem ha-panim) | H3899 + H6440 | 4 | 4 | 25 (1), 35 (1), 39 (1), 40 (1) | οἱ ἄρτοι τῆς προθέσεως (G0740 + G4286) | skuebrødene | ordre |
| EX-TERM-16 | מִזְבֵּחַ (mizbeach) | H4196 | 59 | 51 | 17 (1), 20 (3), 21 (1), 24 (2), 27 (6), 28 (1), 29 (14), 30 (5), 31 (2), 32 (1), 34 (1), 35 (2), 37 (1), 38 (6), 39 (2), 40 (11) | θυσιαστήριον (G2379) | alter (alle forekomster, kontrolltall) | tillegg |
| EX-TERM-17 | אֲרוֹן (aron) | H0727 | 26 | 19 | 25 (8), 26 (2), 30 (2), 31 (1), 35 (1), 37 (3), 39 (1), 40 (8) | ἡ κιβωτός (G2787) | ark (alle forekomster) | tillegg |
| EX-TERM-18 | בְּרִית (berit) | H1285 | 13 | 13 | 2 (1), 6 (2), 19 (1), 23 (1), 24 (2), 31 (1), 34 (5) | ἡ διαθήκη (G1242) | pakt | tillegg |
| EX-TERM-19 | תַּבְנִית (tavnit) | H8403 | 3 | 2 | 25 (3) | τύπος (G5179), παράδειγμα | mønster / forbilde | tillegg |
| EX-TERM-20 | קֹדֶשׁ הַקֳּדָשִׁים (qodesh ha-qodashim) | H6944 + H6944 | 11 | 10 | 26 (3), 29 (1), 30 (4), 35 (1), 39 (1), 40 (1) | ἅγια ἁγίων (G0039, Heb 9,3) | Det aller helligste | tillegg |

### 3.3.1 Versliste per term (WLC-adresse, vestlig i klammer der den avviker)

- **EX-TERM-01 פֶּסַח**: 12,11.21.27.43.48; 34,25
- **EX-TERM-02 מַצָּה / מַצּוֹת**: 12,8.15.17.18.20.39; 13,6.7; 23,15 (x2); 29,2 (x3).23; 34,18 (x2)
- **EX-TERM-03 כַּפֹּרֶת**: 25,17.18.19.20 (x2).21.22; 26,34; 30,6; 31,7; 35,12; 37,6.7.8.9 (x2); 39,35; 40,20
- **EX-TERM-04 מִשְׁכָּן**: 25,9; 26,1.6.7.12.13.15.17.18.20.22.23.26.27 (x2).30.35; 27,9.19; 35,11.15.18; 36,8.13.14.20.22.23.25.27.28.31.32 (x2); 38,20.21 (x2).31; 39,32.33.40; 40,2.5.6.9.17.18.19.21.22.24.28.29.33.34.35.36.38
- **EX-TERM-05 אֹהֶל מוֹעֵד**: 27,21; 28,43; 29,4.10.11.30.32.42.44; 30,16.18.20.26.36; 31,7; 33,7 (x2); 35,21; 38,8.30; 39,32.40; 40,2.6.7.12.22.24.26.29.30.32.34.35
- **EX-TERM-06 עֵדוּת**: 16,34; 25,16.21.22; 26,33.34; 27,21; 30,6 (x2).26.36; 31,7.18; 32,15; 34,29; 38,21; 39,35; 40,3.5.20.21
- **EX-TERM-07 אֲרוֹן הָעֵדוּת**: 25,16.21.22; 26,33.34; 30,6.26; 31,7; 39,35; 40,3.5.21
- **EX-TERM-08 לֻחֹת הָעֵדוּת**: 31,18; 32,15; 34,29
- **EX-TERM-09 מִשְׁכַּן הָעֵדוּת**: 38,21 (x2)
- **EX-TERM-10 אֹהֶל הָעֵדוּת**: ingen forekomst i 2. Mosebok
- **EX-TERM-11 פָּרֹכֶת**: 26,31.33 (x3).35; 27,21; 30,6; 35,12; 36,35; 38,27; 39,34; 40,3.21.22.26
- **EX-TERM-12 מָסָךְ**: 26,36.37; 27,16; 35,12.15.17; 36,37; 38,18; 39,34.38.40; 40,5.8.21.28.33
- **EX-TERM-13 מִזְבַּח הָעֹלָה**: 29,18.25; 30,28; 31,9; 35,16; 38,1; 40,6.10.29
- **EX-TERM-14 מִזְבַּח (מִקְטַר) הַקְּטֹרֶת**: 30,1.27; 31,8; 35,15; 37,25; 40,5
- **EX-TERM-15 לֶחֶם (הַ)פָּנִים**: 25,30; 35,13; 39,36; 40,23
- **EX-TERM-16 מִזְבֵּחַ**: 17,15; 20,24.25.26; 21,14; 24,4.6; 27,1 (x2).5 (x2).6.7; 28,43; 29,12 (x2).13.16.18.20.21.25.36.37 (x3).38.44; 30,1.18.20.27.28; 31,8.9; 32,5; 34,13; 35,15.16; 37,25; 38,1.3.4.7.30 (x2); 39,38.39; 40,5.6.7.10 (x3).26.29.30.32.33
- **EX-TERM-17 אֲרוֹן**: 25,10.14 (x2).15.16.21 (x2).22; 26,33.34; 30,6.26; 31,7; 35,12; 37,1.5 (x2); 39,35; 40,3 (x2).5.20 (x3).21 (x2)
- **EX-TERM-18 בְּרִית**: 2,24; 6,4.5; 19,5; 23,32; 24,7.8; 31,16; 34,10.12.15.27.28
- **EX-TERM-19 תַּבְנִית**: 25,9 (x2).40
- **EX-TERM-20 קֹדֶשׁ הַקֳּדָשִׁים**: 26,33 (x2).34; 29,37; 30,10.29.32.36; 35,19; 39,41; 40,10

### 3.3.2 Kontrollpunkt TK-22: מִשְׁכָּן og אֹהֶל מוֹעֵד

- מִשְׁכָּן står i 55 vers, אֹהֶל מוֹעֵד i 33 vers. Begge står i samme vers 9 steder: 39,32.40; 40,2.6.22.24.29.34.35.
- אֹהֶל uten מוֹעֵד (innen tre ord) står i 21 vers: 16,16; 18,7; 26,7.9.11.12.13.14.36; 33,8.9.10.11; 35,11; 36,14.18.19.37; 39,33.38; 40,19.
- Sammensetningen מִשְׁכַּן אֹהֶל מוֹעֵד («sammenkomstteltets bolig») og nærstilling av de to ordene: הַ֨מִּשְׁכָּ֔ן אֶֽת אָהֳל֖וֹ (1); מִשְׁכַּ֖ן אֹ֣הֶל (1); הַמִּשְׁכָּ֖ן לְאֹ֥הֶל (1); מִשְׁכַּ֖ן אֹ֥הֶל (1); מִשְׁכַּ֥ן אֹֽהֶל (1); מִשְׁכַּ֣ן אֹֽהֶל (1).

**Lesning.** De to uttrykkene er ikke synonymer i teksten. מִשְׁכָּן dominerer i byggebeskrivelsen (kap. 26 og 36) og betegner selve boligen av duker og planker. אֹהֶל מוֹעֵד dominerer der tjeneste og møte er tema (kap. 29, 30 og 40). I ni vers står begge, og i 39,32; 40,2.6.29 står de i konstruktforbindelse. En oversettelse som bruker samme norske ord for begge, kan ikke gjengi disse versene.

אֹהֶל הָעֵדוּת, som ordren fører opp som «vitnesbyrdets telt», forekommer ikke i 2. Mosebok. Det nærmeste er מִשְׁכַּן הָעֵדוּת i 38,21. «Vitnesbyrdets telt» hører til 4. Mosebok og til NT (Apg 7,44; Åp 15,5). I NT gjengir det LXX ἡ σκηνὴ τοῦ μαρτυρίου, som er LXX sin faste gjengivelse av אֹהֶל מוֹעֵד. NT-termen og GT-termen for samme gjenstand vil derfor se ulike ut på norsk. Det må forklares i studiepanelet og ikke jevnes ut.

- פָּרֹכֶת (EX-TERM-11), de vanligste ordgruppene: פָּרֹ֥כֶת הַמָּסָֽךְ (2); הַפָּרֹֽכֶת (2); פָרֹ֗כֶת תְּכֵ֧לֶת וְאַרְגָּמָ֛ן (1); הַפָּרֹכֶת֮ תַּ֣חַת הַקְּרָסִים֒ (1); לַפָּרֹ֔כֶת אֵ֖ת אֲר֣וֹן (1); הַפָּרֹ֨כֶת֙ לָכֶ֔ם בֵּ֣ין (1).
- מָסָךְ (EX-TERM-12), de vanligste ordgruppene: מָסָךְ֙ לְפֶ֣תַח הָאֹ֔הֶל (2); הַמָּסָֽךְ (2); מָסַ֖ךְ שַׁ֥עַר הֶחָצֵֽר (2); מָסַ֥ךְ הַפֶּ֖תַח לַמִּשְׁכָּֽן (2); לַמָּסָ֗ךְ חֲמִשָּׁה֙ עַמּוּדֵ֣י (1); מָסָ֣ךְ עֶשְׂרִ֣ים אַמָּ֗ה (1).

- פָּרֹכֶת הַמָּסָךְ (begge ord i ett uttrykk): 3 treff: 35,12; 39,34; 40,21.
- מִזְבַּח הַזָּהָב (gullalteret): 3 treff: 39,38; 40,5.26.
- מִזְבַּח הַנְּחֹשֶׁת (bronsealteret): 2 treff: 38,30; 39,39.

**Lesning.** פָּרֹכֶת og מָסָךְ står sammen i ett uttrykk tre steder. De må ha hvert sitt norske ord om uttrykket skal kunne gjengis uten omskrivning. NT har καταπέτασμα for det indre forhenget, og MANTELEN NT har «forhenget» i alle seks vers (Matt 27,51; Mark 15,38; Luk 23,45; Heb 6,19; 9,3; 10,20).

Gullalteret og bronsealteret er omskrivninger for røkelsesalteret og brennofferalteret. De fanges ikke av EX-TERM-13 og 14 og må kontrolleres sammen med dem.

לֶחֶם הַפָּנִים: MANTELEN NT har «skuebrødene» i Matt 12,4, Mark 2,26 og Luk 6,4, men «brødene som legges fram» i Heb 9,2, der gresk har ἡ πρόθεσις τῶν ἄρτων.

ἱλαστήριον: MANTELEN NT har «nådestolen» i Heb 9,5 og «soningssted» i Rom 3,25.

## Hva som ikke er gjort

- Kildene er hentet ferskt fra de offentlige arkivene 20.11.2026. De er ikke avstemt mot prosjektets festede kildehasher (`sourceHash` i bokfilene), fordi de festede filene ikke var tilgjengelige i denne økten. Ordantallet i OSHB her er 16 713; låsekvitteringen har 16 714 ordposter. Forskjellen på én post er ikke undersøkt.
- LXX er ikke kontrollert mot Rahlfs eller Göttingen.
- Termfrekvensene er kildetall. Om den låste boken gjengir hvert av de 58 + 34 + 15 + 16 stedene konsekvent, er bare stikkprøvd (se paritetsfilen), fordi bokens leserdata (flere MB) ikke kunne leses inn i denne økten.
- Ingen oversettelse er laget, og ingen fil i `tmp/gt/` er rørt.
