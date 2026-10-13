# Voffgenics

En liten Mewgenics-aktig spill-MVP med hunder: avl med arv og mutasjoner i kennelen, taktiske rutenettkamper mot rotter, måker og katter, permanent død, og veteraner som pensjoneres til avl.

## Spill

Åpne `index.html` i en nettleser. Alt ligger i én fil, og spillet lagres i nettleseren.

## Bygg og test

Kildekoden ligger i `src/`. `build.mjs` setter den sammen til `index.html` (frittstående side) og `voffgenics.html` (samme innhold uten doctype, for publisering som Artifact).

```sh
node voffgenics/build.mjs
NODE_PATH=$(npm root -g) node voffgenics/tests/playtest.mjs
```

Testene følger akseptansekriteriene i `SPEC.md`: genetikk over 2000 parringer, 300 autospilte kamper, 100 hele turer med balansesjekk, en kamp spilt med ekte museklikk, lagring etter omlasting, og skjermbilder i PC- og mobilbredde (lagres i `tests/shots/`).
