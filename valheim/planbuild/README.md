# Solnes-tegninger for PlanBuild

Byggetegninger til borgen i verdenen MantleOfElias (Valheim 1.0.16). De lastes inn av modden [PlanBuild](https://thunderstore.io/c/valheim/p/ShelledGhost/PlanBuild/) og plasseres som planer, altså gjennomsiktige spøkelsesdeler. Hver del bygges når du har lagt inn materialene.

| Fil | Hva | Materialer |
|---|---|---|
| `Solnes_Kongesalen.blueprint` | Storsalen, 12 × 18 m. Steinmurer med trappegavler, stråtak, hearth, Raven throne på steinpodium, seng, langbord og tre armor stands. Bakken jevnes og brolegges. | 353 Stone, 298 Wood, 32 Core wood, 64 Fine wood, 42 Iron nails, 2 Tar, 2 Iron, 8 Resin, 6 Leather scraps, bjørneteppe |
| `Solnes_Vestporten.blueprint` | Porthus med to steintårn, skyteplattform med murtinder, portgård og steinbro. Graver 12 m grav på hver side av broa og setter påler. | 290 Stone, 116 Wood, 40 Core wood, 2 Iron, 8 Resin |
| `Solnes_Grav22m.blueprint` | 22 m tørr vollgrav, 6 m bred og 6 m dyp, med påler langs ytterkanten. | 60 Wood, 40 Core wood |

## Installering

Filene legges i `<Valheim>\BepInEx\config\PlanBuild\blueprints\`. PlanBuild trenger BepInExPack_Valheim, Jötunn og HookGenPatcher.

## Bruk i spillet

1. Lag en **Blueprint Rune** (1 Stone) og en **Plan Hammer** (1 Wood).
2. Utstyr runen, høyreklikk og velg fanen **Solnes**.
3. Sikt på bakken der tegningen skal stå. Roter med scrollhjulet, og flytt opp og ned med Ctrl + Alt + scroll.
4. Venstreklikk for å plassere. Terrenget jevnes eller graves med en gang, og delene kommer som planer.
5. Bygg en **Plan Totem** (1 Wood, 1 Greydwarf eye) i nærheten og legg materialene i den. Den bygger planene innen 30 m. Du kan også gå bort til hver plan og trykke E, så lenge du har Plan Hammer i sekken.
6. Workbench og Stonecutter er med i tegningene. Bygg dem først, fordi planene trenger dem innen rekkevidde.

Planer som mangler støtte, er mer gjennomsiktige og kan ikke bygges ferdig. Med konsollkommandoen `bp.undo` angrer du siste plassering, også terrengendringene.

## Usikre punkter

Geometrien er målt fra egne bygg i lagringen. Dører og jernporter er ikke med ennå, og de settes inn med vanlig hammer i åpningene (2 × 2 m). Stigen i Vestporten og mønekappene på taket er de delene det er størst sjanse for at må justeres.

`bp_gen.py` lager filene på nytt: `python bp_gen.py`.
