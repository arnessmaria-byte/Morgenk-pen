# Veirydderen: feil navn og Morgenkåpen i tidslinjen

Tidslinjen på veirydderen.no viste «Maria Solbak Årnes» og «Elias Solbak Årnes» på del 44 til 48,
og tok med Morgenkåpen utgave 13 som «Del 50». Rettingen er delt i to: data i Ghost og koden i appen.

## Årsak

- **Navn:** appen har en fast navneliste for del 1 til 43. Poster som ikke står der, får
  forfatteren i Ghost (`primary_author.name`) som navn. Det er alltid Maria eller Elias.
- **Morgenkåpen:** appen tar med alle poster med taggen `veirydderen`. Morgenkåpen utgave 13 har
  den taggen, men ikke `#veirydder-kvinne` eller `#veirydder-mann`. Den fikk del 50, som kolliderer
  med den planlagte del 50 (Brooks-Johnson).

## 1. Ghost (`ghost_fiks.py`)

Krever en Admin API-nøkkel fra en Custom Integration (Ghost Admin, Settings, Integrations).

```
python3 ghost_fiks.py                                  # prøvekjøring
GHOST_ADMIN_API_KEY=id:hemmelighet python3 ghost_fiks.py --apply
```

Skriptet fjerner taggen «Veirydderen» fra Morgenkåpen utgave 13, gir del 37 taggen
`#veirydder-kvinne` og bytter ut plassholderne i bylinjen på del 44 og 45 med
publiseringsdatoen.

## 2. Appen (koden for veirydderen.no og /api/series)

**a) Navn.** Bruk aldri forfatteren som navn på en stemme:

```js
const name = ROSTER[post.slug]?.name ?? NAVN[post.slug] ?? post.feature_image_alt;
```

Legg til disse i navnelista. Del 46 og 47 kan ikke hentes fra alt-teksten:

| Del | Slug | Navn |
|---|---|---|
| 44 | i-dont-have-a-paper-signed-by-jesus | Eliška Vančová |
| 45 | vad-jesus-gor-ar-viktigare-an-vad-paulus-tycker | Ilona Degermark |
| 46 | anonym-sokneprest | Anonym sokneprest |
| 47 | falsk-lara-ar-att-anklaga-gud | Sten Rydh |
| 48 | barth-hake | Hanna Barth Hake |

**b) Hvilke poster som er med.** Ta bare med poster som har en av de interne taggene
`#veirydder-kvinne` (`hash-veirydder-kvinne`) eller `#veirydder-mann` (`hash-veirydder-mann`),
ikke alle med `veirydderen`. Da kan ikke et nyhetsbrev gli inn igjen senere. Kjør
`ghost_fiks.py --apply` først, ellers faller del 37 ut.

**c) Mantelen-siden.** Skriptet på mantelen.no/veirydderen/ har allerede en tilsvarende
overstyring for del 41 (`hvis-han-kan-sa-kan-jeg-ogsa`). Den trengs ikke når a) er på plass.
