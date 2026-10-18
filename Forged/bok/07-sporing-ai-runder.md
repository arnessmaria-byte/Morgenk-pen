# Sporing: hvem hadde forrige redigeringsrunde på FORGED

Sporet fra Google Drive, Gmail og filmetadata 18.10.2026. Det som ikke kan leses ut av
filene, står som «ikke belagt».

## Versjonen forfatteren leser nå

| Fil | Sted | Sist endret (UTC) | Belegg |
|---|---|---|---|
| `Forged_v5_7_Manuscript.docx` | Drive › Forged | 21.07.2026 kl. 21:56 | Generert av kode, ikke av Word: `docProps/app.xml` oppgir «Microsoft Word 12.0.0», 83 ord og 1 side for et dokument på 343 kB; `dc:creator` er tom; `created` = `modified` = 21.07.2026 12:09:27Z; `word/document.xml` er skrevet to timer etter resten av pakken (14:06Z). |
| `Forged_v5_7_Manuscript.pdf` | Drive › Forged | 21.07.2026 kl. 21:53 | Samme tekst som docx. |
| `FORGED_5x8.1_Print_Interior_KDP.pdf` | Drive › Forged | 21.07.2026 kl. 23:38 | 133 sider, 5"×8". `Producer: pypdf`, `Creator: Elias Solbak Årnes`. Tekstidentisk med 5.7-docx (kontrollert på intro + Day 1 ord for ord). |

**Konklusjon:** 5x8.1-innmaten ble satt 21.07.2026 om kvelden av et verktøy som kjører Python
(pypdf i produksjonssteget, docx generert fra mal). Det peker på en kodekjørende assistent,
ikke et tekstbehandlingsprogram. Hvilken assistent er **ikke belagt** i filene. Indisier:

- Gmail 19.–21.07.2026: supportsak hos OpenAI, «ChatGPT crash - Projects not loading».
  Forfatteren brukte ChatGPT-prosjekter aktivt de samme dagene.
- Gmail 22.07.2026 kl. 05:03 til Maria: «Nyeste utgave + skjema» med vedleggene
  «Maria Final Reader Review 20E – Full Manuscript Notes v0.1.docx» og «The Foundation of
  Knowing – Full Reader Proof v1.4.1.pdf». Samme natt, samme verktøykjede, annen bok.
- Gmail 23.07.2026 kl. 16:45 til Maria: «Kan du ta en ny gjennomlesning av Forged 5.7.doc?»
- Prosaen i introen (signposting-setningene «And one boundary stated plainly, because it
  matters», «Two final things, and the first governs everything else») har det
  mønsteret forfatteren selv merket som AI-slop. Det er stilistisk fingeravtrykk, ikke bevis.

Mest sannsynlig: en ChatGPT-chat i et Forged-prosjekt (med kodekjøring) 21.07.2026.
Chattens navn kan ikke leses fra Drive eller Gmail. Forfatteren må selv åpne
prosjektoversikten i ChatGPT og se etter en samtale datert 21.07.2026 om kvelden
(norsk tid 22.07. mellom 00 og 02).

## Rundene etter at forfatteren kommenterte PDF-en

| Runde | Tid (UTC) | Hvem | Omfang | Belegg |
|---|---|---|---|---|
| 0 | 21.07.2026 kveld | Mest sannsynlig ChatGPT (prosjekt med kodekjøring) | Hele boken, 5x8.1-innmaten | Se over. Ikke belagt utover indisier. |
| | 16.–17.10.2026 | Forfatteren | 14 kommentarer i 5x8.1-PDF-en, s. 9–21 | PDF-annotasjonene |
| 1 | 17.10.2026 kl. 07:01 | Trolig Gemini | Intro + Day 1 | Google Doc i rotmappen |
| 2 | 17.10.2026 kl. 07:50 | Trolig Gemini, samme chat | Intro + Day 1, «0 em-dash» | Google Doc i rotmappen |
| 3 | 18.10.2026 | Claude (Claude Code, denne økten, første modell) | Intro + Day 1, Ezra-løp | `arbeid/forged/kap-00-intro-og-day-1/`, commit 7440397 |
| **4** | **18.10.2026** | **Claude (Claude Code, samme økt, etter modellbytte)** | **Hele boken, KDP-sats, EPUB** | **`Forged/bok/`, denne leveransen** |

Detaljene om runde 1 og 2 står i `arbeid/forged/kap-00-intro-og-day-1/07-sporing-ai-runder.md`. Kort fortalt diktet runde 2 inn detaljer i Jake-scenariet og strøk avsnitt uten logg. Ingen av de oppdiktede detaljene er med i runde 4.

## Runde 4: hva som er gjort annerledes

- **Startet på nytt fra kilden.** Runde 4 bygger på originalteksten (5.7 + ESV-rettelsene), ikke på runde 3. Runde 3s løsninger for intro og Day 1 er tatt med der de holdt, og vurdert på nytt der de ikke gjorde det.
- **Hele boken i ett løp.** Fem faser, 40 dager, back matter, nytt forord.
- **Uavhengig kontroll.** Tre kaldlesere, én troskapsrevisor, én ESV-kontroll og én sluttleser, alle uten tilgang til redaktørens begrunnelser.
- **Sats og EPUB maskinelt fra manusfilen.** En rettelse i `manus/` gir ny PDF og EPUB med ett skript.

## Neste runde

Den som tar neste runde, bør starte fra `Forged/bok/manus/` (kildefilene) og lese `11-beslutningslogg.md` og `06-formliste.md` først. Kjør `verktoy/antitese_scan.py` og Ezra-sperren før levering.
