# Verifiseringsrapport: FORGED, runde 4

**Dato:** 2026-10-18 · **Kontrollert fil:** `manus/FORGED_manus.md` og alt som er bygget fra den

Akseptkriteriene ble satt før redigeringen. Hvert punkt under er kontrollert på den endelige versjonen, etter sluttleserens rettelser.

## Akseptkriterier og resultat

| # | Kriterium | Metode | Resultat |
|---|---|---|---|
| 1 | Ingen sperrende AI-slop | Ezra `slop_scan.py --lang en --gate` | Exit 0. 0 harde treff, 0 grensebrudd. |
| 2 | Forfatterens antitesemønster renset | `verktoy/antitese_scan.py` med grense per dag | 0 sperrende brudd (134 før). Se slop-revisjonen. |
| 3 | Ingen tankestrek i brødtekst | Ezra-skann | 0 (143 før). En-dash bare i tallspenn. |
| 4 | Alle bibelsitater ordrett etter ESV | Maskinell sammenligning mot ESV-tekst hentet fra BibleGateway | 41 av 41 ordrett. Tabell under. |
| 5 | Ingen oppdiktede fakta eller detaljer | Troskapsrevisor, original mot redigert, linje for linje | Funn i Day 1, 2, 3, 6, 19, 25, 31 og 34 rettet tilbake til originalens mening. Ny kontroll: ingen gjenstående. |
| 6 | Ingen avsnitt borte uten begrunnelse | `diff_manuscript.py`, dekningskontroll | 31 avsnitt meldt. Alle 31 gjennomgått og ført under «Tilsiktede strykninger» i endringsloggen. |
| 7 | Struktur intakt | Telling | 40 dager, 40 «End of Day»-merker med riktig nummer, 5 faser, 3 vedlegg. |
| 8 | Alle kommentarer besvart | Kommentarkartet | 14 av 14 fra forfatteren, 11 av 11 fra Maria. |
| 9 | Teksten flyter for målgruppen | Tre kaldlesere (hver sin tredjedel) og én sluttleser på hele boken | Sluttleserens dom: «Klar med disse rettelsene». 12 av 20 punkter tatt inn av redaktøren. Seks til (fem teologiske og «sexuality») er avgjort og lagt inn av forfatteren 18.10.2026 (beslutningsloggen, 17–18). De to siste står etter vurdering: forordet (forfatterens beslutning) og «Consistency heals» i vedlegg C (beslutningsloggen, 16). |
| 10 | Typografi som de to første bøkene | Målt fra trykkfilene til *The Supervised Hours* og *The Foundation of Knowing* | EB Garamond 11,5 pt, linjeavstand 15,1 pt, 6 × 9, sperrede versaler, sentrert topptekst og folio, fasesider som Part-sidene i TFOK. |
| 11 | KDP-krav for innmat | pymupdf og pdftotext | Marger, fonter, sidestørrelse og 0 annotasjoner OK. Se KDP-sjekklisten. |
| 12 | Innholdsliste stemmer | `verktoy/sjekk_innhold.py` | 50 av 50 oppføringer på riktig side, begge formater. |
| 13 | EPUB gyldig | EPUBCheck 5.1.0 | 0 feil, 0 advarsler. |
| 14 | Visuell kontroll | Alle 118 sider sett i oversiktsark og utvalgte sider i full størrelse | Ingen løse overskrifter, delte tabeller eller tomme sider med topptekst. |
| 15 | Sporede endringer finnes | Telling i `05-forged-sporet.docx` | 3 781 innsettinger og 3 708 slettinger, forfatter «Ezra-redaktør». |
| 16 | Fem teologiske endringer og «sexuality» i alle filer | Uavhengig kontroll med pdftotext, EPUB-tekst og docx-tekst | Ny ordlyd finnes én gang i hvert format, gammel ordlyd ingen steder. |

## Det som ikke kunne verifiseres

- **Hammarskjöld-sitatet i forordet.** «It is easy to be good when one is not put to the test…» finnes ikke i noen kilde vi kunne søke i, verken engelsk eller svensk. Forfatteren har avgjort at forordet står uendret.
- **Forordets engelske ordlyd** er ikke godkjent av Sverre Johannes.
- **Royalty- og trykksatser** er KDPs kjente satser og må bekreftes i KDP på opplastingsdagen.
- **Hvilken AI som laget 5x8.1-PDF-en** er ikke belagt i filene. Se sporingsrapporten.

## Skriftkontroll mot ESV

Sitater funnet: 41, ordrett i ESV: 41

| Henvisning | ESV | Sitat (begynnelse) |
|---|---|---|
| 1 Thessalonians 5:19 | OK | Do not quench the Spirit. |
| 2 Corinthians 6:17 | OK | Go out from their midst, and be separate from them, says the Lord. |
| 1 Thessalonians 5:21 | OK | Test everything; hold fast what is good. |
| Mark 2:27 | OK | The Sabbath was made for man, not man for the Sabbath. |
| Matthew 5:6 | OK | Blessed are those who hunger and thirst for righteousness, for they sh… |
| Luke 12:48 | OK | Everyone to whom much was given, of him much will be required. |
| Proverbs 4:25 | OK | Let your eyes look directly forward, and your gaze be straight before … |
| 1 Corinthians 12:31 | OK | Earnestly desire the higher gifts. |
| James 1:12 | OK | Blessed is the man who remains steadfast under trial, for when he has … |
| Ephesians 5:15 | OK | Look carefully then how you walk, not as unwise but as wise. |
| Proverbs 19:11 | OK | Good sense makes one slow to anger. |
| Luke 6:26 | OK | Woe to you, when all people speak well of you. |
| Matthew 10:37 | OK | Whoever loves father or mother more than me is not worthy of me. |
| Matthew 6:21 | OK | For where your treasure is, there your heart will be also. |
| Ephesians 4:26 | OK | Be angry and do not sin; do not let the sun go down on your anger. |
| Luke 16:10 | OK | One who is faithful in a very little is also faithful in much. |
| James 1:22 | OK | But be doers of the word, and not hearers only. |
| Proverbs 24:16 | OK | The righteous falls seven times and rises again. |
| Hebrews 4:12 | OK | For the word of God is living and active… discerning the thoughts and … |
| Proverbs 27:17 | OK | Iron sharpens iron, and one man sharpens another. |
| 1 Timothy 6:12 | OK | Fight the good fight of the faith. |
| 2 Corinthians 3:6 | OK | The letter kills, but the Spirit gives life. |
| Matthew 7:24 | OK | Everyone then who hears these words of mine and does them will be like… |
| 1 Thessalonians 5:23 | OK | May the God of peace himself sanctify you completely. |
| Luke 21:19 | OK | By your endurance you will gain your lives. |
| Psalm 5:3 | OK | O LORD, in the morning you hear my voice. |
| 1 Thessalonians 5:6 | OK | So then let us not sleep, as others do, but let us keep awake and be s… |
| Romans 12:2 | OK | Do not be conformed to this world, but be transformed by the renewal o… |
| Proverbs 18:12 | OK | Before destruction a man’s heart is haughty, but humility comes before… |
| Psalm 22:1 | OK | My God, my God, why have you forsaken me? |
| 1 Corinthians 6:19 | OK | Do you not know that your body is a temple of the Holy Spirit…? |
| Galatians 6:9 | OK | Let us not grow weary of doing good, for in due season we will reap, i… |
| Mark 10:43 | OK | Whoever would be great among you must be your servant. |
| Acts 1:8 | OK | You will be my witnesses… |
| Proverbs 15:1 | OK | A soft answer turns away wrath, but a harsh word stirs up anger. |
| James 1:19 | OK | Let every person be quick to hear, slow to speak, slow to anger. |
| 2 Corinthians 4:18 | OK | We look not to the things that are seen but to the things that are uns… |
| Matthew 5:16 | OK | Let your light shine before others, so that they may see your good wor… |
| Matthew 25:21 | OK | Well done, good and faithful servant. You have been faithful over a li… |
| Philippians 3:13–14 | OK | Forgetting what lies behind and straining forward to what lies ahead, … |
| Ephesians 4:14 | OK | so that we may no longer be children, tossed to and fro by the waves a… |
