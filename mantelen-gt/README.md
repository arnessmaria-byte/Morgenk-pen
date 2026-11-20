# mantelen-gt: tverrkorpus og pre-flight (skyøkten)

Arbeidsfiler fra Claude Code (skyøkten) til arbeidsordren «Mantelen GT og tverrkorpus», 20.11.2026.

Dette repoet er offentlig. Her ligger derfor bare verktøy og kildeavledet materiale (WLC/OSHB, STEP/TAHOT, Swete LXX, Scrivener 1894) og ordlyd fra den publiserte MANTELEN NT. Ordrett tekst fra upublisert MANTELEN GT ligger ikke her.

| Fil | Innhold |
|---|---|
| `TVERRKORPUS_KONKORDANS.md` | TK-registeret, menneskelesbart. Utkast; 23 av 25 oppføringer mangler kilde. |
| `tk_concordance.json` | TK-registeret, maskinlesbart. |
| `02_2mosebok_PREFLIGHT.md` | Versparitet, 16 sitatankre og 20 termer for 2. Mosebok. |
| `02_2mosebok_PREFLIGHT_ORDDATA.md` | Ord for ord: OSHB-ID, morfologi og TAHOT for ankerversene. |
| `data/exodus_preflight.json` | Samme data maskinlesbart. |
| `tools/gtkilder.py` | Lesere for OSHB, VerseMap, TAHOT, Scrivener, Swete og NT-leserdata. |
| `tools/exodus_preflight.py` | Bygger pre-flight-filene. Inndata: `preflight_hode.md`, `anker_kommentar.json`, `kilder.json`. |
| `tools/tk_validate.py` | Låskontroll mot TK- og KR-register. |

Kildelisenser: OSHB og STEP/TAHOT CC BY 4.0, Swete LXX (First1KGreek) CC BY-SA 4.0, Scrivener 1894 (Robinson) fri bruk.
