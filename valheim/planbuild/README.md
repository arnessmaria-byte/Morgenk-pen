# Solnes-tegninger for PlanBuild

Byggetegninger til borgen i verdenen MantleOfElias (Valheim 1.0.16). De lastes inn av modden [PlanBuild](https://thunderstore.io/c/valheim/p/ShelledGhost/PlanBuild/) og plasseres som planer, altså gjennomsiktige spøkelsesdeler. Hver del bygges når du har lagt inn materialene.

| Fil | Hva | Materialer |
|---|---|---|
| `Solnes_Kongesalen.blueprint` | Storsalen, 12 × 18 m. Steinmurer med trappegavler, stråtak, hearth, Raven throne på steinpodium, seng, langbord og tre armor stands. Bakken jevnes og brolegges. | 393 Stone, 302 Wood, 32 Core wood, 64 Fine wood, 42 Iron nails, 2 Tar, 2 Iron, 8 Resin, 6 Leather scraps, bjørneteppe |
| `Solnes_Vestporten.blueprint` | Porthus med to steintårn, to jernporter, skyteplattform med murtinder, portgård og steinbro. Graver 12 m grav på hver side av broa og setter påler. | 376 Stone, 116 Wood, 40 Core wood, 10 Iron, 8 Resin |
| `Solnes_Grav22m.blueprint` | 22 m tørr vollgrav, 6 m bred og 6 m dyp, med påler langs ytterkanten. | 60 Wood, 40 Core wood |
| `Solnes_Stabburet.blueprint` | Stabbur på 4 × 4 m, løftet 1 m opp på fire steinsøyler, med fem kister, steintrinn og saltak med utstikk foran og bak. | 44 deler |
| `Solnes_Mjodstua.blueprint` | Bryggerhus på 6 × 6 m med fem fermentere, bord, stoler, tønne og bål på steinheller. Vegger i to høyder og takoverheng over døra. | 66 deler |
| `Solnes_Tingstua.blueprint` | Tingsted på 6 × 6 m til torget: steingulv, vegger på tre sider, åpen front med tømmerstolper, bål, fire stoler, banner og teppe. Jevner og brolegger bakken. | 58 deler |
| `Solnes_Lysthuset.blueprint` | Lysthus på 6 × 6 m til Kongshagen: steingulv, lave vegger på tre sider, bål, fire stoler og teppe. | 41 deler |
| `Solnes_Akerbed.blueprint` | Åkermodul på 6 × 10 m: dyrket bed på 4 × 10 m og brolagt sti på 2 m, med fakkel ved enden av stien. Jevner bakken til siktehøyden. Stemples ut side om side. | 1 del |
| `Solnes_Bigarden.blueprint` | Åtte bikuber i to rader på en brolagt flate på 12 × 6 m, med to fakler. Hver kube trenger 1 Queen bee. | 10 deler |
| `Solnes_Folden.blueprint` | Innhegning på 8 × 20 m for tamme villsvin: tremur på 2 m, dør midt på framsiden, jordgulv. | 30 deler |
| `Solnes_Kongebordet.blueprint` | Langbord på 4 m med fem stoler og hjorteteppe, til midten av Velkomsthallen. Ingen terrengendring. | 8 deler |
| `Solnes_Palerad.blueprint` | Fem påler på rad, 9 m lang, uten terrengendring. Brukes langs en grav som alt er gravd. | 30 Wood, 20 Core wood |

Stabburet, Mjødstua, Tingstua og Lysthuset hører til Nedre gård, og det gjør de fire hagetegningene også. I alle fire er framsiden +z: døra eller den åpne siden. Roter tegningen slik at framsiden vender mot veien, torget eller hageporten.

## Åkermodulen

Hver terrenglinje i en PlanBuild-tegning jevner bakken til siktehøyden og maler den etterpå. Åkerbed-modulen dyrker derfor et bed på 4 × 10 m og brolegger en sti på 2 m ved siden av, men den gjør også bakken flat. Legg bedene på tvers av bakken og sikt midt på hvert bed, så blir trinnene mellom modulene små. Vil du ikke jevne, bruker du kultivatoren som før.

## Pålerad og rydding

Grav 22 m graver grava og setter pålene i samme avtrykk. Grava graves 6 m under punktet du sikter på, og PlanBuild har ikke spillets grense på 8 m. Sikter du ned i en grav som alt finnes, blir den 6 m dypere for hvert avtrykk, og hvert avtrykk legger ti nye pålplaner i siktehøyden, også oppå de gamle. Bruk Pålerad langs en ferdig grav. Den endrer ikke terrenget, og raden er så kort at pålene ikke svever eller går i jorda der bakken heller. Sikt på bakken der pålene skal stå, med framsiden mot grava.

Slik sletter du planer med Blueprint Rune og verktøyet **Delete plans**:

- Hold Ctrl og scroll for å endre radius, fra 2 til 100 m.
- Planene som blir røde mens du holder Ctrl, er de som slettes. Hold Ctrl og venstreklikk for å slette dem.
- Uten Ctrl sletter du bare planen du peker på.
- Bygde deler blir ikke rørt.
- Materialer som er lagt i en plan, faller ut der planen sto.

Verktøyet **Terrain** i Blueprint Rune setter bakken tilbake til slik den var fra start når du holder Alt og venstreklikker. Det gjelder hele markeringen: scroll endrer radius, Ctrl + scroll roterer, og Q bytter mellom sirkel og rektangel. Bruk det bare der ingenting er bygd, for det fjerner også vanlige graveendringer, sti og dyrket jord innenfor markeringen. Et vanlig venstreklikk uten Alt jevner bakken til høyden du sikter på.

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

`bp_gen.py` lager filene på nytt: `python bp_gen.py`. `bp_nedre.py` lager de fire tegningene til Nedre gård: `python bp_nedre.py`. `bp_hage.py` lager de fire hagetegningene: `python bp_hage.py`. `bp_palerad.py` lager Pålerad: `python bp_palerad.py`.
