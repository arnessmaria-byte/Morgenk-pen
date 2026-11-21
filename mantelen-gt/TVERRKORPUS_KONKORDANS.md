# Tverrkorpus-konkordans (TK-01 til TK-25)

**Status: UTKAST, IKKE VEDTATT. 3 av 25 oppføringer er delvis utfylt (TK-01 bare med tittel), 22 står tomme.**

Denne filen er den menneskelesbare siden av `tk_concordance.json` og er generert fra den. Den er laget 20.11.2026 av Claude Code (skyøkten) etter oppgave 1 i arbeidsordren «Mantelen GT og tverrkorpus».

## Hvorfor registeret ikke er fylt ut

Ordren ber meg lagre «det vedtatte» registeret fra `GT-GEMINI-SAMKJORING-SVAR`. Det dokumentet finnes ikke i Drive-speilet av prosjektmappen per 20.11.2026:

- I `rapporter/gt-claude-gemini-samkjoring-2026-11-20/` ligger bare invitasjonen `SAMKJORING.md`. Det finnes ingen `DOM-MOTTATT.md` og ingen fil som begynner med linjen `GT-GEMINI-SAMKJORING-SVAR` eller `GT-GEMINI-TK-<nr>`.
- Fulltekstsøk etter `TK-01`, `TK-08`, `TK-22`, `TK-25`, «Tverrkorpus», «hilasterion» og «kapporet» gir ingen treff utenom invitasjonen.
- Ordren selv gjengir bare to oppføringer i stikkordsform: TK-08 (nådestol) og TK-22 (tabernaklet mot sammenkomstens telt).

Jeg har derfor ikke ordlyden i de 25 vedtakene, og jeg dikter dem ikke. TK-08 og TK-22 er fylt ut med det som kan belegges i kildene, og merket UBEKREFTET. De andre 23 står med status MANGLER_KILDE.

**For å fullføre:** legg svaret fra Gemini i Drive (hvilken som helst mappe), eller lim det inn i samtalen. Da fører jeg det ordrett inn som `DOM-MOTTATT.md` etter saksgangen og fyller registeret fra det.

## Tre forhold Captain bør avgjøre

1. **Parallell termtabell.** `MANTELEN_GT_OVERSETTELSESREGLER.md` sier om det felles registeret `rapporter/nt-fullkontroll-2026-09-10/MANTELEN_NT_GT_SAMORDNING.md`: «Bruk dette registeret; ikke opprett en parallell termtabell for GT.» Et TK-register med låste termer er en slik tabell. Enten må regelen endres, eller så bør `tk_concordance.json` være et maskinlesbart lag som peker inn i det felles registeret, ikke en egen norm.
2. **KR-01 til KR-20 finnes ikke.** Ordren ber om kobling til «eksisterende KR-01..KR-20 i valideringsskriptet». Ingen fil i Drive inneholder et KR-register, og ingen av prosjektets kontrollverktøy (`gt_unit_qa.py`, `gt_chapter_qa.py`, `gt_source_corpus_qa.py`, `nt_final_qa.py`) er navngitt som termlåskontroll. Verktøyene tilhører Codex og er ikke åpnet eller endret.
3. **Ordrens termer stemmer ikke med låst tekst.** Se merknadene under TK-08 og TK-22, og paritetsfilen for 2. Mosebok.

## Hva som er levert

- `tk_concordance.json`: registeret, med skjema, statuskoder og 25 plasser.
- `tools/tk_validate.py`: frittstående kontroll som leser ett eller flere registre i samme format (TK, og KR når det finnes som `kr_register.json`) og prosjektets leserdata (`gt-*.json`, NT-bøkene). Den feiler lukket: returkode 2 så lenge et register mangler eller har oppføringer uten vedtak, returkode 1 ved låsbrudd i en VEDTATT oppføring. Den er prøvd mot NT-bøkene; GT-bøkene er ikke prøvd, fordi GT-leserdata ikke var tilgjengelig i økten.
- Kontrollen er ikke koblet inn i prosjektets egne QA-skript. Det er Codex sitt arbeid, etter at Captain har avgjort punkt 1 og 2.

Kjøring:

```bash
python3 tools/tk_validate.py check --register tk_concordance.json --register kr_register.json gt-exo.json rom.json heb.json
```

```bash
python3 tools/tk_validate.py observe --strong H3727 --strong G2435 gt-exo.json rom.json heb.json
```

## Normtabell

| ID | Status | Tema | WLC-hebraisk (Strong) | LXX-bro | Scrivener 1894 (Strong) | Låst GT-term | Låst NT-term | Studiepanelkrav |
|---|---|---|---|---|---|---|---|---|
| TK-01 | UBEKREFTET | Kanonisk paritet mellom WLC (GT) og Scrivener 1894 (NT). Bare tittellinjen er mottatt (21.11.2026); regeltekst og virkeområde mangler. | | | | | | |
| TK-02 | MANGLER_KILDE | (ikke mottatt) | | | | | | |
| TK-03 | MANGLER_KILDE | (ikke mottatt) | | | | | | |
| TK-04 | MANGLER_KILDE | (ikke mottatt) | | | | | | |
| TK-05 | MANGLER_KILDE | (ikke mottatt) | | | | | | |
| TK-06 | MANGLER_KILDE | (ikke mottatt) | | | | | | |
| TK-07 | MANGLER_KILDE | (ikke mottatt) | | | | | | |
| TK-08 | UBEKREFTET | Nådestolen | כַּפֹּרֶת (H3727) | ἱλαστήριον | ἱλαστήριον (G2435) | nådestol | nådestol (Hebr 9,5); «soningssted» (Rom 3,25) | Noten ved første forekomst i 2 Mos 25,17 skal nevne LXX hilasterion og NT-stedene. Ordren forutsetter «nådestol» også for Rom 3,25; låst NT har «soningssted» der. Avviket må avgjøres uttrykkelig, ikke harmoniseres stille. |
| TK-09 | MANGLER_KILDE | (ikke mottatt) | | | | | | |
| TK-10 | MANGLER_KILDE | (ikke mottatt) | | | | | | |
| TK-11 | MANGLER_KILDE | (ikke mottatt) | | | | | | |
| TK-12 | MANGLER_KILDE | (ikke mottatt) | | | | | | |
| TK-13 | MANGLER_KILDE | (ikke mottatt) | | | | | | |
| TK-14 | MANGLER_KILDE | (ikke mottatt) | | | | | | |
| TK-15 | MANGLER_KILDE | (ikke mottatt) | | | | | | |
| TK-16 | MANGLER_KILDE | (ikke mottatt) | | | | | | |
| TK-17 | MANGLER_KILDE | (ikke mottatt) | | | | | | |
| TK-18 | MANGLER_KILDE | (ikke mottatt) | | | | | | |
| TK-19 | MANGLER_KILDE | (ikke mottatt) | | | | | | |
| TK-20 | MANGLER_KILDE | (ikke mottatt) | | | | | | |
| TK-21 | MANGLER_KILDE | (ikke mottatt) | | | | | | |
| TK-22 | UBEKREFTET | Tabernaklet og sammenkomstens telt holdes leksikalsk atskilt | מִשְׁכָּן / אֹהֶל מוֹעֵד (H4908, H168, H4150) | σκηνή / ἡ σκηνὴ τοῦ μαρτυρίου | σκηνή (G4633) | mishkan og ohel moed får hver sitt norske ord | telt / teltet (aldri «tabernakel») | Noten ved 2 Mos 25,9 og 27,21 skal si at LXX og NT bruker ett gresk ord for begge, og at NT-uttrykket «vitnesbyrdets telt» (Apg 7,44; Åp 15,5) svarer til hebraisk ohel moed, ikke til ohel ha-edut. |
| TK-23 | MANGLER_KILDE | (ikke mottatt) | | | | | | |
| TK-24 | MANGLER_KILDE | (ikke mottatt) | | | | | | |
| TK-25 | MANGLER_KILDE | (ikke mottatt) | | | | | | |

## Merknader til de to delvis utfylte oppføringene

### TK-08  Nådestolen

- Grunnlag: Arbeidsordren 20.11.2026 nevner TK-08 som «nådestol» for kapporet, jf. hilasterion i Rom 3,25 og Heb 9,5. Vedtaksteksten selv er ikke mottatt.
- LXX: LXX gjengir kapporet med hilasterion (2 Mos 25,17 med tillegget epithema).
- NT-belegg: Rom 3,25, Hebr 9,5. MANTELEN NT, revisjon nt-2026-10-13: Hebr 9,5 «nådestolen», Rom 3,25 «soningssted».
- Åpent: Skal Rom 3,25 regnes inn under låsen, eller er «soningssted» et begrunnet unntak?

### TK-22  Tabernaklet og sammenkomstens telt holdes leksikalsk atskilt

- Grunnlag: Arbeidsordren 20.11.2026 nevner TK-22: mishkan mot ohel moed, «tabernaklet» mot «sammenkomstens telt». Vedtaksteksten selv er ikke mottatt.
- LXX: LXX bruker skene for begge hebraiske ord og gjengir ohel moed med «vitnesbyrdets telt». Skillet i hebraisk kan derfor ikke leses av LXX eller NT.
- NT-belegg: Apg 7,44, Hebr 8,2, Hebr 8,5, Hebr 9,2, Hebr 9,3, Hebr 9,11, Åp 15,5. MANTELEN NT har «telt» i alle vers med G4633; Apg 7,44 «Vitnesbyrdets telt».
- Åpent: Ordren sier «tabernaklet» for mishkan; NT har «telt» for skene. Er forskjellen ønsket?
