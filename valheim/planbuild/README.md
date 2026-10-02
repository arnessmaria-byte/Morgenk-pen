# Solnes-tegninger for PlanBuild

Byggetegninger til borgen i verdenen MantleOfElias (Valheim 1.0.16). De lastes inn av modden [PlanBuild](https://thunderstore.io/c/valheim/p/ShelledGhost/PlanBuild/) og plasseres som planer, altså gjennomsiktige spøkelsesdeler. Hver del bygges når du har lagt inn materialene.

| Fil | Hva | Materialer |
|---|---|---|
| `Solnes_Kongesalen.blueprint` | Storsalen, 12 × 18 m. Steinmurer med trappegavler, stråtak, hearth, Raven throne på steinpodium, seng, langbord og tre armor stands. Bakken jevnes og brolegges. | 393 Stone, 302 Wood, 32 Core wood, 64 Fine wood, 42 Iron nails, 2 Tar, 2 Iron, 8 Resin, 6 Leather scraps, bjørneteppe |
| `Solnes_Vestporten.blueprint` | Porthus med to steintårn, to jernporter, skyteplattform med murtinder, portgård og steinbro. Graver 12 m grav på hver side av broa og setter påler. | 376 Stone, 116 Wood, 40 Core wood, 10 Iron, 8 Resin |
| `Solnes_Grav22m.blueprint` | 22 m tørr vollgrav, 6 m bred og 6 m dyp, med påler langs ytterkanten. | 60 Wood, 40 Core wood |

## Installering

Filene legges i `<Valheim>\BepInEx\config\PlanBuild\blueprints\`. Bruk PlanBuild 0.20.0 fra MathiasDecrock. Versjon 0.18.8 fra ShelledGhost har en feil som gjør at planer på bakken står som «Not enough support». `oppdater_planbuild.ps1` bytter den ut.

`installer.ps1` gjør alt i én operasjon: lim inn `irm <rå-URL til installer.ps1> | iex` i PowerShell med Valheim lukket. `oppdater_tegninger.ps1` henter bare nye versjoner av tegningene.

## Bruk i spillet

1. Lag en **Blueprint Rune** (1 Stone) og en **Plan Hammer** (1 Wood).
2. Utstyr runen, høyreklikk og velg fanen **Solnes**.
3. Sikt på bakken der tegningen skal stå. Roter med scrollhjulet, og flytt opp og ned med Ctrl + Alt + scroll.
4. Venstreklikk for å plassere. Terrenget jevnes eller graves med en gang, og delene kommer som planer.
5. Bygg en **Plan Totem** (1 Wood, 1 Greydwarf eye) i nærheten og legg materialene i den. Den bygger planene innen 30 m. Du kan også gå bort til hver plan og trykke E, så lenge du har Plan Hammer i sekken.
6. Workbench og Stonecutter er med i tegningene. Bygg dem først, fordi planene trenger dem innen rekkevidde.

Planer som mangler støtte, er mer gjennomsiktige og kan ikke bygges ferdig. Med konsollkommandoen `bp.undo` angrer du siste plassering, også terrengendringene.

## Usikre punkter

Geometrien bygger på snappunktene og kolliderne til byggedelene, lest rett fra spillets egne prefabs (Valheim 1.0.16). Steinmurene er 1 m tykke, og hjørnesteiner (stone_pillar) fyller hjørnene der to murer møtes. Retningen på tronen, senga, langbordet og armor stands er ikke kontrollert mot spillet, så de kan stå vendt feil vei.

`bp_gen.py` lager filene på nytt: `python bp_gen.py`.
