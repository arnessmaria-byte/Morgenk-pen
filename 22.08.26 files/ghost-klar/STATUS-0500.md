# Morgenkåpen utgave 1 — Ghost-status

## Mål
- **Schedule:** lørdag 22. august 2026 kl. **05:00** Europe/Oslo  
  (`published_at`: `2026-08-22T03:00:00.000Z`)
- Status: **scheduled** (ikke Publish now)
- Emne: Selbekk svarte. Første del står i dette brevet
- Preheader: Del én av Dagen-serien i fulltekst, et essay skrevet for brevet alene, tre navn å be for, og et ord til kaffen.
- Newsletter: Mantelen (`default-newsletter`)

## Ghost
- **Post-ID:** `6a8769989c9ccc0001bcf3c7`
- **Editor:** https://mantelen.ghost.io/ghost/#/editor/post/6a8769989c9ccc0001bcf3c7
- **Sist bekreftet i Ghost:** scheduled med `published_at` **06:30 Oslo** (`2026-08-22T04:30:00.000Z`) og kort plassholdertekst
- **Omplanlegging til 05:00 + full body/bilde:** **IKKE utført** — Cursor browser MCP er nede (faner forsvinner; `browser_navigate` feiler med «No browser tab available»)

## Blokkering (2026-08-20 ~23:37)
Agenten kan ikke nå den innloggede Ghost-sesjonen uten fungerende Cursor-nettleser. Admin API utenfor nettleser blokkeres (Cloudflare 403). Ingen Custom Integration-nøkkel er satt opp.

## Lokalt klart
- `body-for-api.html` — full HTML-tekst
- `body-plain.txt` — plain tekst for liming
- `../bilder/22.08.26.jpeg` — KI-illustrasjon (merkelinje: KI-generert bilde)
- `reschedule-0500.js` — CDP/API-uttrykk for å sette 05:00
- `schedule-meta.txt` — oppdatert til 05:00

## Manuelt i Ghost (1–2 min) ELLER «åpne Cursor-browser + klar»
1. Åpne editor-lenken over (innlogget som Maria)
2. Publish → Schedule → **22.08.2026 05:00**
3. Lim inn full tekst fra `body-plain.txt` (eller HTML-kort fra `body-for-api.html`)
4. Last opp `bilder/22.08.26.jpeg` ved frukt-avsnittet med bildetekst **KI-generert bilde**
5. Settings: e-postemne + preheader som over; send med nyhetsbrevet Mantelen
6. Bekreft status **Scheduled** (ikke Published)
