# Ravnebladet

Spillbladet som hører til BondeRavn: en Valheim 1.0-håndbok i Mantelens hus-stil,
med bosskrefter, bossguide, builds, utstyr, mat og mjød, mynter, sideoppdrag,
base og komfort, og dyrehold. Alle tall er verifisert mot Valheim Wiki og Iron Gates
patchnotater (versjon 1.0.20, 15. oktober 2026).

- `ravnebladet.html` er siden slik den publiseres som artefakt (uten doctype og head,
  som artefakt-tjenesten legger på selv).
- `ravnebladet.pdf` er trykkutgaven, A4.
- `lag-pdf.js` lager PDF-en med Chromium via Playwright:

```
# pakk HTML-en inn i et komplett dokument først, så:
node lag-pdf.js ravnebladet-full.html ravnebladet.pdf
```

Interaktive deler (matplanlegger og komfortkalkulator) skjules i PDF-en.
