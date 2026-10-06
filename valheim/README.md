# Valheim: Bossrush (seed HHcLC5acQt)

To ferdige, helt nye Valheim 1.0-verdener på samme seed, klare til å legges rett i spillet.

## Hvorfor denne seeden

`HHcLC5acQt` er den seeden som går igjen på nesten alle "beste seed"-lister. Den ble lagt ut på r/valheim av InfernoFPS under tittelen "We did it boys, we found the best seed", og er siden omtalt av blant andre GamesRadar, Dexerto, Sportskeeda, Mein-MMO og BisectHosting (som også har den med på sin 1.0-liste).

Det som gjør den til et så godt utgangspunkt for challenges:

- Fire av bossene ligger på startkontinentet, innen gangavstand.
- Den femte bossen ligger på naboøya, en kort tur med flåte.
- Haldor (handelsmannen) ligger like ved spawn.
- Alle de tidlige biomene finnes på startøya.

Kort sagt: kartet fjerner letingen, så det eneste som gjenstår er selve utfordringen.

## Hva som ligger her

| Mappe | Innstillinger | Til hva |
| --- | --- | --- |
| `worlds_local/Bossrush` | Normal (standard) | Speedrun, boss rush og egne regler |
| `worlds_local/BossrushViking` | Spillets Hardcore-preset | "True Viking": veldig hard kamp, ingen kart, alt mistes ved død, bosselementer kan ikke tas gjennom portaler |

Begge inneholder bare metadatafilen `_main.0.fwl2`. Resten av verdenen bygges av spillet første gang du laster den, akkurat som når du lager en ny verden i menyen.

## Installering

Enklest på Windows: dobbeltklikk `Installer-Bossrush.bat`. Den legger begge verdenene på riktig sted og hopper over dem som allerede finnes.

Manuelt:

1. Lukk Valheim.
2. Kopier mappen eller mappene fra `worlds_local/` inn i:
   - Windows: `%USERPROFILE%\AppData\LocalLow\IronGate\Valheim\worlds_local\`
   - Linux: `~/.config/unity3d/IronGate/Valheim/worlds_local/`
3. Start spillet, velg (eller lag) en ny karakter, og velg `Bossrush` eller `BossrushViking` i verdenslisten.

Bruk gjerne en helt ny karakter, ellers ødelegger utstyret fra en gammel karakter de fleste challenges.

Vil du se nøyaktig hvor bossene ligger før du starter, skriv inn seeden `HHcLC5acQt` på https://valheim-map.world.

## Konkrete challenges

Forslag som passer kartet. Nummer 3 bruker spillets egne Hardcore-regler, resten er regler du holder selv.

1. **Boss rush på tid.** Start en timer når du spawner, stopp den når Yagluth er død. Ingen kart-juks og ingen konsollkommandoer.
2. **Ingen båt.** Kun det du når til fots på startkontinentet, pluss én flåtetur til den siste bossen.
3. **Én død og du er ute.** Spill `BossrushViking` og slett karakteren hvis du dør.
4. **Ingen portaler.** Alt skal fraktes fysisk. Krever ingen innstilling, bare disiplin.
5. **Naken til The Elder.** Ingen rustning før de to første bossene er døde, bare våpen og skjold.

## Lage verdenene på nytt

`lag_verden.py` lager mappene fra bunnen av (Python 3, ingen avhengigheter):

```
python3 lag_verden.py [utmappe]
```

Filformatet følger `World.SaveWorldMetaData` slik det er dokumentert i [MakeFwl](https://github.com/CrystalFerrai/MakeFwl). Seed-hashen (298112588) er kontrollert mot et uavhengig bibliotek ([corgonia/fwl](https://pkg.go.dev/github.com/corgonia/fwl)).
