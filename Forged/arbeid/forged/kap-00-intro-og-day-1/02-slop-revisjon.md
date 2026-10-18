# Slop-revisjon: FORGED, To the One Giving This Book + Introduction + Day 1

**Status:** REN (sperren passert, exit 0)
**Skannet:** 00-original.md → 04-intro-og-day-1-redigert.md (`slop_scan.py --lang en --gate`)

## Sammendrag

Sperrende (skal være i null / under grense før levering):

| Måling | Før | Etter | Grense | Status |
|---|---|---|---|---|
| Harde treff totalt | 0 | 0 | 0 | OK |
| Tankestrek per 1000 ord | 10,61 | 2,05 | ≤ 2,5 | OK |
| Em-dash | 15* | 0 | sparsomt | OK |
| «Ikke X, men Y» (skannerens mønster) | 1 | 1 | ≤ 1 | OK |
| «Not X. It is Y.» (manuelt talt, to setninger) | 24 | 4 | ingen formell grense; forfatterens krav: «renses» | Se under |
| Retorisk spm. + svar | 0 | 0 | 0 | OK |
| Trikolon | 2 | 1 | ≤ 2 | OK |
| Emoji | 0 | 0 | 0 | OK |

\* Skanneren telte markdown-tabellens skillelinje («---») som em-dash. Brødteksten i originalen hadde null em-dash-tegn; tankestrekene var en-dash i FORGE-listen («F – FLARE»), i overskrifter og i epigrafhenvisningen.

Rådgivende (mål, ikke krav):

| Måling | Før | Etter | Mål | Kommentar |
|---|---|---|---|---|
| Burstiness | 0,721 | 0,675 | ≥ 0,45 | God variasjon begge veier. To seksjoner ligger lavt: «Day 1 – Kindling the Flame» (0,29, sju korte setninger etter at innledningen ble strøket) og «What This Day Is Really About» (0,33). Det er forfatterens slagstil, og seksjonene er korte. Ikke jevnet ut. |
| LIX | 33,3 | 30,3 | 40–50 | Under målet, og det er riktig. Målleseren er nitten og skal lese høyt om morgenen. Shorten og Simplify language senker LIX; vi legger ikke til leddsetninger for å løfte et tall. |
| Adverb per 1000 ord | 10,17 | 5,48 | ≤ 12 | «actually» ×2, «simply», «frequently», «merely», «quietly» ute. |
| Passiv per 1000 ord | 11,5 | 7,53 | ≤ 15 | FORGE-listen skrevet aktivt («Passive faith is shaken, and you start to own it»). |

## Treff og behandling

Skanneren fant ingen harde ord i originalen. Den egentlige sloppen i dette kapitlet er
syntaktisk, og skanneren fanger bare en del av den. Manuell telling:

| Mønster | Før | Etter | Behandling |
|---|---|---|---|
| «Not X. It is Y.» / «not X, but Y» / «X; not Y» | 24 | 4 | 20 skrevet om til positive utsagn eller strøket. De fire som står: «Pressure does not ask what you believe. It reveals what you have practiced.» · «A son does not train to be adopted. He trains because of whose house he lives in.» · «the rope, not the One it is fastened to» · «It is not a book of comfort, and it will not flatter him» (negasjon uten Y-ledd). |
| Innledning som annonserer poenget | 9 | 0 | «The difference matters, and it is worth being clear about», «This book was built for that reality», «And a word about the size of the practices, so you can trust it», «You will notice, too», «One more thing, and I mean it practically», «And one boundary stated plainly, because it matters», «Two final things», «The second is this», «And here is what I have found», «Of course the picture breaks down», «And one distinction, because a careful reader will feel it», «I want to say plainly»: alle strøket. |
| Avsnitt som kommenterer bokens egen form | 2 | 0 | «the days share one frame», «This is not a challenge to complete» strøket. |
| Metafor som forklarer seg selv | 2 | 0 | «The picture is too simple, of course», «Of course the picture breaks down» strøket. |
| Anafor-rekke / slagordrekke (≥3 på rad) | 5 | 1 | «He had beliefs. He had language. He had familiarity.» → én setning. «alignment is what … ×3» → én setning. Sju slagord i «Forged, Not Polished» → to. «Growth leaves marks. Integrity is earned slowly.» slått sammen. Beholdt: «when motivation is low, when tension is high, when old patterns resurface, and when life is quiet» (forfatterens rytme, én gang). |
| Forutsigelse om at leseren svikter | 2 | 0 | «because you will», «A gap is not disqualification» ute (kommentar 5). |
| Tankestrek i brødtekst (en-dash med mellomrom) | 7 | 0 | Brødtekst: null. Tre en-dash står igjen i overskrifter («Day 1 – …», «PHASE I – FLARE», «Healing Forge – …») som bokens etablerte typografi. Epigrafhenvisningen står på egen linje uten strek. |

## Uavklarte

- **En-dash i overskrifter.** Tre forekomster gir 2,05 per 1000 ord, under grensen, men ikke null. Å fjerne dem er en typografisk avgjørelse for hele boken (40 dag-overskrifter, 5 fase-overskrifter, alle Healing Forge-overskrifter og TOC). Forfatteren avgjør. Alternativ: «Day 1: Kindling the Flame».
- **«philosophically, existentially, practically»** (trikolon, originalen). Beholdt som forfatterens formulering om egen historie. Kan strykes uten tap: «For over twenty years, I tested what could hold.»
- **«neglect, distraction, and delay»** (trikolon, originalen). Beholdt; de tre ordene er konkrete og knytter til verset.
- **«Awareness is the first act of mercy.»** Énlinjes avslutning. Kaldlesningen merket den som aforisme-closer; forfatteren kommenterte den ikke. Beholdt.
- **«Young men keep the books that someone believed they could live up to.»** Bildet «live up to a book» er skjevt, men setningen er forfatterens og gavebudskapet hviler på den. Beholdt.

## Rytmediagnose

Burstiness var over målet før og etter, så ingen metronom-kjede var sperrende. Skanneren
melder fem kjeder i den redigerte teksten, mot åtte før. De som ble arbeidet med:

- «Forged, Not Polished»: sju setninger på 5–8 ord → fire setninger, 6/17/8/13 ord. Slått sammen: «Fire, resistance, and repetition do» + «what has never been under load is still theory»; «Growth leaves marks» + «what shapes you most is what you endure honestly».
- «Before You Begin», siste avsnitt: tre anaforiske «alignment is what …» (8/7/9 ord) → én setning på 19 ord.
- «The Scenario», andre avsnitt: «He had beliefs. He had language. He had familiarity.» (3/3/3) → én setning på 9 ord + én på 10.
- «What This Day Is Really About»: tre aforismer på 5/9/9 ord → én på 20 og én på 9.

Kjeder som står med vilje: «In 2016, I was called. In 2018, I committed. The testing has not stopped.» (4/4/5) og «Jake was simply awake.» etter «No vision, no revelation.» Det er forfatterens slag.
