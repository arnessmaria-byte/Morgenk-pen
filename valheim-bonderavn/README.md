# BondeRavn

En ravn som flyr ved skulderen din i Valheim (som feen i Zelda), leser av gården din
og coacher deg underveis: temming, avl for høyest mulig stjerner, mat, plass og planter.

Modden er en BepInEx-plugin. Den **leser bare** spilltilstand og endrer ingenting i spillet,
så den fungerer også på servere der du ikke er admin, og den bruker ingen Harmony-patcher.

## Hva ravnen gjør

- **Følger deg.** En lokal kopi av spillets ravnemodell svever ved venstre skulder,
  vipper litt, og hopper når den har noe nytt å si. Ingen andre spillere ser den.
- **Leser av dyrene** innen skanneradius hvert fjerde sekund:
  stjerner, tam eller vill, sulten, urolig, temmeklokke, kjærlighetspoeng, graviditet,
  antall innenfor avlsgrensen, partnere innen pareavstand, og hvor lenge unger har igjen.
- **Gir løpende råd** i en snakkeboble, prioritert etter hva som faktisk stopper avlen:
  1. Sult (sultne dyr får verken temming eller unger)
  2. Urolige dyr (fiender i nærheten stopper paring)
  3. Temming som pågår (prosent, tid igjen, og hvorfor klokka eventuelt står)
  4. Blandet stamme (ungen arver stjernene til den som blir gravid, så skill ut de beste)
  5. Fullt hus (for mange av samme art innenfor spillets sjekkradius)
  6. Ville dyr i nærheten med flere stjerner enn du har i fjøset
  7. Ensomme dyr, gravide, kjærlighetspoeng, unger, planter
- **Roper ut hendelser** når noe skjer: et dyr blir tamt, blir gravid, en unge blir født,
  eller et vilt dyr med stjerner dukker opp. Hendelser speiles også i spillets egen meldingsstripe.
- **Tavle** (F8): oversikt over alle dyr i nærheten, gruppert per art med stjernefordeling,
  sultne, gravide, unger og kjærlighetspoeng.
- **Holder kjeft** når alt er sagt, og gjentar seg ikke før nedkjølingen er over.

## Taster (kan endres i config)

| Tast | Gjør |
|------|------|
| F7   | Slå ravnen av eller på |
| F8   | Vis eller skjul tavla |
| F9   | Be om det viktigste rådet nå |

## Installasjon

1. Installer [BepInExPack Valheim](https://thunderstore.io/c/valheim/p/denikson/BepInExPack_Valheim/).
2. Legg `BondeRavn.dll` i `<Valheim>/BepInEx/plugins/`.
3. Start spillet. Config skrives til `BepInEx/config/no.morgenkapen.bonderavn.cfg`
   og kan endres i spillet med
   [ConfigurationManager](https://thunderstore.io/c/valheim/p/Azumatt/Official_BepInEx_ConfigurationManager/).

## Bygge selv

Du trenger .NET SDK 8 og en Valheim-installasjon (for `assembly_valheim.dll`).

```
cd valheim-bonderavn
dotnet build BondeRavn/BondeRavn.csproj -c Release -p:ValheimDir="C:\Program Files (x86)\Steam\steamapps\common\Valheim"
```

Resultatet ligger i `BondeRavn/bin/Release/BondeRavn.dll`.
Du kan også sette miljøvariabelen `VALHEIM_INSTALL` i stedet for `-p:ValheimDir=`.

Uten `ValheimDir` bygges modden mot stubbene i `stubs/`. Det er bare for syntaks- og
typekontroll (det er dette CI gjør); en slik dll skal **ikke** legges i spillmappen.

### Teste hjernen uten spillet

Rådlogikken ligger i `BondeRavn/Coach/` og har ingen Unity- eller Valheim-avhengigheter.

```
dotnet run --project tests/CoachBrain.Tests/CoachBrain.Tests.csproj
```

Dette kjører noen oppdiktede gårdsscenarier og skriver ut rådene ravnen ville gitt.

## Hvordan den leser spillet

| Komponent i spillet | Hva vi leser |
|---------------------|--------------|
| `Character`         | art, nivå (1 = 0 stjerner, 3 = 2 stjerner), tam, død |
| `Tameable`          | sulten, temmetid totalt, `TameTimeLeft` fra ZDO, metningstid, kjælenavn |
| `MonsterAI`         | urolig (alarmert), hvilken mat arten spiser |
| `Procreation`       | maks antall, sjekkradius, pareavstand, sjanse, graviditetstid, `lovePoints` og `pregnant` fra ZDO |
| `Growup`            | hvor lenge ungen har igjen (`spawntime` fra ZDO) |
| `Plant`             | status (for tett, feil biom, udyrket, mangler lys) og tid til høsting via refleksjon |

Tellingen av "fullt hus" etterligner spillets egen: prefabnavnet brukes som prefiks,
så grisunger (`Boar_piggy`) teller med for villsvin (`Boar`).

## Avlsregler ravnen bygger på

- Ungen får samme stjerner som den som blir gravid (aldri flere). Avl kan bare arve, ikke øke.
- Hvem som helst i innhegningen kan bli gravid, så en blandet stamme gir blandede unger.
  Vil du ha bare 2-stjerners, må alle i innhegningen være 2-stjerners.
- 2-stjerners må finnes vilt og temmes. De er sjeldne og dukker oftere opp lenger fra kartets midte.
- Sultne eller urolige dyr parer seg ikke. Temming teller bare når dyret er mett og rolig.
- Blir det for mange av arten innenfor sjekkradiusen, stopper alt til du slakter eller flytter noen.

## Begrensninger

- Modden er skrevet mot Valheim-API-et slik det er kjent i de siste versjonene, men er ikke
  testet mot en kjørende klient i dette repoet. Første gang du starter: sjekk `BepInEx/LogOutput.log`
  for advarsler fra `BondeRavn`.
- Finner den ikke ravneprefaben i spillet, bygger den en enkel svart ravn av primitiver i stedet.
- Alt som leses fra ZDO-nøkler er pakket i feilhåndtering, så en navneendring i spillet
  gir "ukjent" i stedet for krasj.
