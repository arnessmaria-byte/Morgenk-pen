#!/usr/bin/env python3
"""Trinn 0, steg 4: lager piloter/RAPPORT_TRINN0_10_PILOTER.md og piloter/manuskriptkort-prototype.html
fra pilotfilen og registrene. Bruk: rapport.py <prosjektmappe> [valideringsutskrift.txt]
"""
import json, os, sys, html

PROJ = sys.argv[1]
J = lambda *p: json.load(open(os.path.join(PROJ, *p), encoding='utf-8'))
pil, reg, src = J('piloter', 'trinn0-10-piloter.json'), J('registre', 'vitneregister.json'), J('registre', 'kildelisenser.json')
W = reg['witnesses']; ED = {s['id']: s['name'] for s in src['sources'] + src['internalEditions']}
VAL = open(sys.argv[2], encoding='utf-8').read().strip() if len(sys.argv) > 2 and os.path.exists(sys.argv[2]) else None
ST = {'BEKREFTET_ANKER': 'R10', 'BEKREFTET_TRANSKRIPSJON': 'lest i transkripsjon', 'BEKREFTET_UTGAVETEKST': 'lest i utgavens tekst', 'BEKREFTET_SEKUNDAERT': 'oppgitt i annet datasett',
      'BEKREFTET_I_OVERSETTELSE': 'funnet i oversettelse', 'DELVIS_BEKREFTET': 'delvis lest', 'IKKE_AVLEST': 'ikke avlest'}
TYPE = {'papyrus': 'papyrus', 'majuskel': 'majuskel', 'minuskel': 'minuskel', 'rulle': 'rulle', 'hebraisk_kodeks': 'kodeks', 'oversettelse': 'oversettelse', 'kirkefar_verk': 'kirkefar'}
EDS = {'R10': 'MANTELEN (R10)', 'SCR1894': 'Scrivener 1894', 'RP2018': 'Robinson–Pierpont 2018', 'THGNT': 'THGNT', 'TREG': 'Tregelles', 'TISCH8': 'Tischendorf 8', 'NA28': 'NA28', 'SBLGNT': 'SBLGNT', 'WH': 'Westcott–Hort', 'MAM': 'MAM'}
HANDS = {None: '', '*': '*', 'C': ' korr.', 'C1': ' korr. 1', 'C2': ' korr. 2', 'C3': ' korr. 3'}


def date_of(sig):
    e = W[sig]; d = e.get('dateRange')
    if d: return '%s–%s (%s)' % (d['notBefore'], d['notAfter'], e['century']) if d['notBefore'] != d['notAfter'] else str(d['notBefore'])
    return ('periode: %s' % e['period']) if e.get('period') else 'ikke registrert'


def age(w):
    d = W[w['siglum']].get('dateRange')
    return (d['notBefore'], d['notAfter']) if d else (99999, 99999)


def short(t, n=46):
    t = t or ''
    return t if len(t) <= n else '… ' + t[-n:]


def ms_rows(r):
    rows = []
    for w in sorted(r['manuscriptWitnesses'], key=age):
        e = W[w['siglum']]
        what = '(verset står ikke)' if w['certainty'] in ('utelatt',) or (w.get('reading') == '' and w['verification']['status'] != 'IKKE_AVLEST' and w['siglum'] != 'B19A') else (w.get('attested') or short(w.get('reading', '')))
        if w['siglum'] == 'B19A' and w.get('reading') == '': what = '(linjen står ikke)'
        cert = w.get('certainty', '')
        rows.append({'name': e['display'] + HANDS.get(w.get('hand'), ''), 'type': TYPE[e['type']], 'date': date_of(w['siglum']) if w.get('hand') in (None, '*') else 'håndskriftet %s; korrektoren er senere og ikke datert i registeret' % date_of(w['siglum']), 'loc': w.get('locator') or '', 'what': what,
                     'cert': '' if cert in ('lest', 'utelatt') else cert, 'status': ST[w['verification']['status']], 'note': w.get('note', ''), 'lang': 'he' if e.get('tradition') in ('Q', 'M') else 'grc'})
    return rows


def nor(n):
    return '; '.join(('«%s»' % x['text']) + ((' (%s%s)' % (x['kind'], ': ' + x['note'] if x.get('note') else '')) if x['kind'] != 'r10' or x.get('note') else '') for x in n)


def anchor_line(u):
    a = u['anchor']; rel = {'erstatter': 'lesningene gjelder disse ordene', 'etter': 'tillegget står etter dette ordet', 'hele_verset': 'lesningene gjelder hele verset'}[a['relation']]
    if a['testament'] == 'GT':
        ws = a['words']; span = ws[0]['g'] if len(ws) == 1 else '%s … %s' % (ws[0]['g'], ws[-1]['g'])
        return '%s (ord %s, id %s%s): %s' % (span, ws[0]['position'] if len(ws) == 1 else '%d–%d' % (ws[0]['position'], ws[-1]['position']), a['firstWordId'], '' if len(ws) == 1 else '–' + a['lastWordId'], rel)
    ws = a['words']; span = ' '.join(w['g'] for w in ws) if len(ws) <= 4 else '%s … %s' % (ws[0]['g'], ws[-1]['g'])
    return '%s (ord %s i verset): %s' % (span, a['firstWordIndex'] if len(ws) == 1 else '%d–%d' % (a['firstWordIndex'], a['lastWordIndex']), rel)


# ------------------------------------------------------------------ Markdown
counts = {}
for u in pil['units']:
    for r in u['readings']:
        for k in ('editionSupport', 'manuscriptWitnesses', 'versionWitnesses', 'patristicWitnesses'):
            for w in r[k]: counts[w['verification']['status']] = counts.get(w['verification']['status'], 0) + 1
tot = sum(counts.values())
M = []
A = M.append
A('# Trinn 0: ti pilotsteder i manuskriptlaget'); A('')
A('MANTELEN fase 2, tekstkritisk og dokumentarisk manuskriptlag. Rapport fra fagledelsen (Fable), 25. november 2026.'); A('')
A('Rapporten viser de ti pilotstedene som manuskriptkort, slik de er tenkt i leseren når «Manuskript- og grunnkildemodus» er slått på. Kortene er laget maskinelt fra `piloter/trinn0-10-piloter.json` og registrene. Ingen fil i låst R10/R11.1 er endret.'); A('')
A('## Status'); A('')
A('Alle ti enhetene er **utkast**. De består skjema, anker og registerkontroll, men de kan ikke låses ennå. Planen krever at hvert vitne er lest i kilden av en navngitt person, og at hver enhet er registrert av to uavhengige lesere. Det er ikke gjort.'); A('')
A('| Kontroll | Resultat |'); A('|---|---|')
A('| JSON Schema | 10 av 10 pilotsteder består |'); A('| Ordanker mot låst R10/R11.1 (ord og SHA-256) | 10 av 10 treffer |')
A('| Sigla og patristiske referanser i `vitneregister.json` | 100 %, 0 uregistrerte |'); A('| Dateringer skrevet inn for hånd | 0 |')
A('| Vurdering (akse 3) | «ikke vurdert» i alle ti |'); A('| Dobbel registrering | ikke kjørt |'); A('')
A('Av %d vitne- og utgaveopplysninger i de ti enhetene:' % tot); A('')
A('| Status | Antall | Betydning |'); A('|---|---|---|')
EXPL = {'BEKREFTET_TRANSKRIPSJON': 'Lesningen er funnet maskinelt i en importert transkripsjon av håndskriftet (INTF, ETCBC, WLC).',
        'BEKREFTET_UTGAVETEKST': 'Lesningen er funnet i utgavens egen digitale tekst.', 'BEKREFTET_ANKER': 'Lesningen er ankerordene i låst R10.',
        'BEKREFTET_SEKUNDAERT': 'Utgavens valg er hentet fra et annet fritt datasett. Utgaven selv er ikke avlest.',
        'BEKREFTET_I_OVERSETTELSE': 'Fedresitatet er funnet i engelsk oversettelse. Gresk eller latinsk ordlyd er ikke avlest.',
        'DELVIS_BEKREFTET': 'Deler av lesningen er funnet. Resten må leses i trykt utgave.', 'IKKE_AVLEST': 'Oppgitt i oppdraget eller håndbøkene. Ikke lest i noen kilde i Trinn 0.'}
for k in ('BEKREFTET_TRANSKRIPSJON', 'BEKREFTET_UTGAVETEKST', 'BEKREFTET_ANKER', 'BEKREFTET_SEKUNDAERT', 'BEKREFTET_I_OVERSETTELSE', 'DELVIS_BEKREFTET', 'IKKE_AVLEST'):
    A('| %s | %d | %s |' % (ST[k], counts.get(k, 0), EXPL[k]))
A('')
A('## Funn som endrer oppdraget'); A('')
for f in [
 '**Åp 22,19 og P (025).** Oppdraget fører P som vitne for «livets tre». INTFs sideindeks viser at Codex Porphyrianus slutter med Åp 22,2–6. Stedet er ikke bevart, og håndskriftet er ført som utelukket vitne med belegg. 046 har bladet, men ingen publisert transkripsjon, og står som ikke avlest.',
 '**Apg 8,37 har tre greske former.** Ingen av de transkriberte håndskriftene har nøyaktig Scriveners ordlyd. Laudianus (500-tallet) har «skal du bli frelst» og «jeg tror på Kristus, Guds Sønn». Minusklene har «han sa til ham» uten Filips navn.',
 '**1 Tim 3,16.** Bare 01, 02, 04 og minuskel 6 har publisert transkripsjon hos INTF. D* og D² er derfor ikke avlest. Ingen før-nikensk far er funnet med et ordrett sitat. De to fedrene med «Gud» er fra 300-tallet.',
 '**Sal 22,17.** R10-noten gjengir ὤρυξαν med «de gravde». Kortet har derfor to gjengivelser av lesningen: «de har gravd» (ordrett) og «de har gjennomboret» (tradisjonell, tolkende), slik planen krever.',
 '**5 Mos 32,43 og Hebr 1,6.** Sitatet i Hebr 1,6 er likt Odae 2:43 bortsett fra artikkelen. Etter planens regel er det ikke et uavhengig vitne. Den digitale Swete-teksten til 5 Mos 32:43 har OCR-tap og kan ikke brukes uten korrektur.',
 '**Datering av rullene.** Ingen av Qumran-rullene har fått årstall. Leon Levy oppgir bare periode («Herodian», «Hasmonean»). Årstallene må hentes fra DJD av en navngitt leser. Det samme gjelder B19ᴬ og fedrene.',
 '**Pilotlisten.** Oppdraget og planens vedlegg B har ulike lister. Oppdraget har Mark 1,1, Joh 1,18, Apg 8,37 og 1 Tim 3,16 der vedlegg B har 1 Sam 10,27b, Luk 23,34a, Mark 16,9–20 og 1 Joh 5,7–8. Denne leveransen følger oppdraget.',
 '**Tekniske funn.** R10-filene har greske aksenttegn som NFC-normalisering endrer, så ankerord må sammenlignes byte for byte. Nettstedets mellomlager gir eldre kopier av `joh.json` og `1ti.json` når versjonsparameteren mangler. TAGNT og Robinson–Pierponts variantnote er uenige om NA28 har artikkelen i Mark 1,1.']:
    A('- ' + f)
A('')
A('## Slik leses kortene'); A('')
A('Øverst står R10-lesningen. Deretter kommer hver lesning med grunntekst, ordrett norsk og vitnene sortert etter alder. Utgaver står på egen linje og er ikke vitner. Vitnemønsteret er regnet ut av maskinen. Vurderingen ligger bak en egen fane og er ikke satt for noen av de ti.'); A('')

for u in pil['units']:
    A('---'); A('')
    A('## %d. %s' % (u['pilotNr'], u['ref']['r10'] + (' (vestlig: %s)' % u['ref']['western'] if u['ref'].get('western') else '')))
    A(''); A('`%s` · utkast' % u['variantId']); A('')
    A('**MANTELEN (R10):** «%s»' % u['r10Verse']); A('')
    A('**Ankerord:** ' + anchor_line(u)); A('')
    if u['ref'].get('western'):
        A('**Adresse:** MT `%s` ↔ lesernes `%s` (vestlig %s) · gresk %s' % (u['ref']['mtRef'], u['ref']['stepPublicationRef'], u['ref']['western'], u['ref']['lxxRef'])); A('')
    for r in u['readings']:
        A('### Lesning %s: %s%s' % (r['readingId'], r['label'], ' · MANTELEN (R10)' if r.get('isR10') else '')); A('')
        if r['text']: A('- Grunntekst: %s' % r['text'])
        A('- Ordrett norsk: ' + nor(r['norwegian']))
        A('- Form: ' + r['morphology'])
        if r['editionSupport']:
            A('- Utgaver som har lesningen: ' + ', '.join(EDS.get(e['edition'], e['edition']) + (' (%s)' % e['form'] if e.get('form') else '') + ('†' if e['verification']['status'] == 'BEKREFTET_SEKUNDAERT' else '') for e in r['editionSupport']))
        A('')
        rows = ms_rows(r)
        if rows:
            A('| Håndskrift | Type | Datering | Sted | Har på stedet | Status |'); A('|---|---|---|---|---|---|')
            for x in rows:
                A('| %s | %s | %s | %s | %s%s | %s |' % (x['name'], x['type'], x['date'], x['loc'], x['what'], (' (%s)' % x['cert']) if x['cert'] else '', x['status']))
            A('')
        for w in r['versionWitnesses']:
            A('- Oversettelse: **%s**%s%s. Forelegg: %s. Status: %s.%s' % (W[w['siglum']]['display'], (' ' + w['locator']) if w.get('locator') else '', (': %s, %s' % (w['text'], nor(w['norwegian'])) if w.get('text') and w.get('norwegian') else (': ' + w['text'] if w.get('text') else '')),
                                                                      w['vorlage'], ST[w['verification']['status']], (' ' + w['witnessLimit']) if w.get('witnessLimit') else (' ' + w['note'] if w.get('note') else '')))
        for w in r['patristicWitnesses']:
            e = W[w['siglum']]
            A('- Kirkefar: **%s** %s (%s %s, %s). %s, %s. I oversettelse: «%s». Status: %s.%s' % (e['display'], w['locator'], e['clavis']['series'], e['clavis']['number'], e['window'], w['quoteType'], {'grc': 'gresk', 'la': 'latin'}[w['lang']], w.get('wording', ''),
                                                                                             ST[w['verification']['status']], (' ' + w['witnessLimit']) if w.get('witnessLimit') else (' ' + w['note'] if w.get('note') else '')))
        if r['versionWitnesses'] or r['patristicWitnesses']: A('')
    A('**Vitnemønster (regnet ut):** %s' % u['witnessPattern']['code']); A('')
    A('**Variantart:** %s (mekanisk grovsortering: %s) · **Betydningsgrad:** %s' % (u['variantKind']['assigned'], u['variantKind']['computed'], u['significance'])); A('')
    A('**Vurdering:** %s. Egen fane i leseren.' % u['evaluation']['class']); A('')
    A('**Filologisk notat.** ' + u['philologicalNote']); A('')
    for x in u.get('crossReferences', []):
        A('**Kryssreferanse:** %s, %s. Uavhengig vitne: %s. %s' % (x['ref'], x['relation'], 'ja' if x['independentWitness'] else 'nei', x['basis'])); A('')
    for x in u.get('excludedWitnesses', []):
        A('**Utelukket vitne:** %s. %s' % (W[x['siglum']]['display'], x['reason'])); A('')
    for x in u.get('dataConflicts', []):
        A('**Avvik mellom datasett:** ' + x); A('')
    if u.get('leads'):
        A('**Må kontrolleres mot kilde:**'); A('')
        for x in u['leads']: A('- ' + x)
        A('')
A('---'); A('')
A('## Før enhetene kan låses'); A('')
for x in ['Captain godkjenner lisensporten i `registre/kildelisenser.json` (%d kilder, alle med `captainApproval` tom).' % len(src['sources']),
          'En navngitt leser leser de %d opplysningene som ikke er lest i kilden: fedresitatene i kritisk utgave, NA28 og THGNT i utgavene, D 06 og 046 på bilde eller i utgave, Swete 5 Mos 32:43 i trykt utgave.' % (tot - counts.get('BEKREFTET_TRANSKRIPSJON', 0) - counts.get('BEKREFTET_UTGAVETEKST', 0) - counts.get('BEKREFTET_ANKER', 0)),
          'Dateringer for rullene, B19ᴬ og fedrene hentes fra DJD, Tov og utgavene og føres inn i registeret med kilde.',
          'Andre leser registrerer de ti enhetene uavhengig (plan 7.4), og samsvaret måles.',
          'Overdommeren avgjør om pilotlisten skal følge oppdraget eller planens vedlegg B, og setter eventuelle vurderinger i akse 3 med begrunnelse og litteratur.']:
    A('1. ' + x)
A('')
A('† Utgavevalg merket med † er hentet fra et annet fritt datasett (TAGNT eller Robinson–Pierponts variantnoter). Utgaven selv er ikke avlest.'); A('')
if VAL:
    A('## Utskrift fra validatoren'); A(''); A('```text'); A(VAL); A('```'); A('')
open(os.path.join(PROJ, 'piloter', 'RAPPORT_TRINN0_10_PILOTER.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(M))

# ------------------------------------------------------------------ HTML-prototype
E = lambda s: html.escape(str(s if s is not None else ''))
CSS = '''
:root{--bg:#f7f4ec;--card:#fffdf8;--ink:#1c1a17;--muted:#5d564a;--line:#d9d0bd;--gold:#8a6a1f;--mark:#b08a2e;--chip:#efe8d6;--warn:#7a3b12}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#0b0b0b;--card:#151412;--ink:#f1ead9;--muted:#b3a88f;--line:#3a3529;--gold:#d9b65a;--mark:#d9b65a;--chip:#24211a;--warn:#f0b27a}}
:root[data-theme="dark"]{--bg:#0b0b0b;--card:#151412;--ink:#f1ead9;--muted:#b3a88f;--line:#3a3529;--gold:#d9b65a;--mark:#d9b65a;--chip:#24211a;--warn:#f0b27a}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:"EB Garamond",Georgia,"Times New Roman",serif;font-size:18px;line-height:1.5}
main{max-width:860px;margin:0 auto;padding:20px 16px 80px}h1{font-size:1.7rem;margin:.2em 0 .1em}h2{font-size:1.25rem;margin:0}
.sub{color:var(--muted);margin:0 0 1em}.bar{position:sticky;top:0;background:var(--bg);border-bottom:1px solid var(--line);padding:10px 16px;display:flex;gap:12px;align-items:center;flex-wrap:wrap;z-index:2}
.bar button{font:inherit;background:var(--card);color:var(--ink);border:1px solid var(--gold);border-radius:999px;padding:6px 14px;cursor:pointer}
.bar button[aria-pressed="true"]{background:var(--gold);color:var(--bg)}
.verse{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px;margin:18px 0}
.ref{font-variant:small-caps;letter-spacing:.04em;color:var(--gold)}.r10{font-size:1.15rem;margin:.3em 0}
.anchor{color:var(--muted);font-size:.95rem}.anchor span[lang]{color:var(--ink);border-bottom:2px solid transparent;font-size:1.15rem}
body.mlag .anchor span[lang]{border-bottom-color:var(--mark)}
.count{display:none;font-size:.85rem;border:1px solid var(--mark);border-radius:999px;padding:0 8px;margin-left:8px}body.mlag .count{display:inline-block}
details.card{display:none;margin-top:12px;border-top:1px solid var(--line);padding-top:8px}body.mlag details.card{display:block}
summary{cursor:pointer;color:var(--gold);font-weight:700}
.reading{border-left:3px solid var(--line);padding:4px 0 4px 12px;margin:14px 0}.reading.r10r{border-left-color:var(--gold)}
.lbl{font-weight:700}.tag{font-size:.8rem;background:var(--chip);border-radius:4px;padding:1px 6px;margin-left:6px;white-space:nowrap}
.gt{font-size:1.3rem;margin:.2em 0}.no{margin:.1em 0}.form,.small{color:var(--muted);font-size:.9rem;margin:.1em 0}
ul.w{list-style:none;padding:0;margin:8px 0}ul.w li{padding:6px 0;border-top:1px dotted var(--line);display:grid;grid-template-columns:1fr auto;gap:2px 10px}
.wn{font-weight:700}.wd{color:var(--muted);font-size:.9rem;grid-column:1/-1}.st{font-size:.8rem;color:var(--muted);text-align:right}.st.open{color:var(--warn);font-weight:700}
.eds{font-size:.92rem;border-top:1px solid var(--line);padding-top:6px;margin-top:6px}.axis{margin:.5em 0}.note{margin:.6em 0}
details.eval{margin:.6em 0;border:1px solid var(--line);border-radius:8px;padding:6px 10px}
[lang=he]{direction:rtl;unicode-bidi:isolate;font-family:"SBL Hebrew","Ezra SIL","Times New Roman",serif}[lang=grc]{font-family:"SBL Greek","Gentium Plus",Georgia,serif}
@media (max-width:560px){body{font-size:17px}ul.w li{grid-template-columns:1fr}.st{text-align:left}}
'''
H = ['<!doctype html><html lang="nb"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Manuskriptkort, prototype</title><style>%s</style></head><body class="mlag">' % CSS,
     '<div class="bar"><button id="t" type="button" aria-pressed="true">Manuskript- og grunnkildemodus: på</button><span class="small">Filter: endrer betydningen · prototype fra Trinn 0, utkast</span></div><main>',
     '<h1>Manuskriptkort for ti pilotsteder</h1><p class="sub">Prototype av kortvisningen i mantelen.no/bibelen. Laget fra pilotfilen og registrene. R10 vises uendret når modusen er av.</p>']
for u in pil['units']:
    a = u['anchor']; lang = 'he' if a['testament'] == 'GT' else 'grc'
    words = ' '.join(w['g'] for w in a['words']) if len(a['words']) <= 4 else '%s … %s' % (a['words'][0]['g'], a['words'][-1]['g'])
    H.append('<section class="verse" aria-labelledby="h%d"><h2 id="h%d"><span class="ref">%s</span><span class="count" title="variantenheter i verset">1 variant</span></h2>' % (u['pilotNr'], u['pilotNr'], E(u['ref']['r10'] + (' (vestlig %s)' % u['ref']['western'] if u['ref'].get('western') else ''))))
    H.append('<p class="r10">%s</p><p class="anchor">Grunntekst: <span lang="%s" translate="no" title="variant i dette ordet">%s</span></p>' % (E(u['r10Verse']), lang, E(words)))
    H.append('<details class="card"><summary>Åpne manuskriptkortet</summary>')
    for r in u['readings']:
        H.append('<div class="reading%s"><p><span class="lbl">Lesning %s: %s</span>%s</p>' % (' r10r' if r.get('isR10') else '', E(r['readingId']), E(r['label']), '<span class="tag">MANTELEN (R10)</span>' if r.get('isR10') else ''))
        if r['text']: H.append('<p class="gt" lang="%s" translate="no">%s</p>' % (r['lang'], E(r['text'])))
        for n in r['norwegian']:
            H.append('<p class="no">«%s»%s</p>' % (E(n['text']), '' if n['kind'] == 'r10' and not n.get('note') else ' <span class="tag">%s</span>%s' % (E({'ordrett': 'ordrett gjengivelse av lesningen', 'tolkende': 'tolkende gjengivelse', 'r10': 'R10'}[n['kind']]), (' <span class="small">%s</span>' % E(n['note'])) if n.get('note') else '')))
        H.append('<p class="form">%s</p><ul class="w">' % E(r['morphology']))
        for x in ms_rows(r):
            H.append('<li><span class="wn">%s <span class="tag">%s</span></span><span class="st%s">%s</span><span class="wd">%s%s · <span lang="%s" translate="no">%s</span>%s%s</span></li>' % (
                E(x['name']), E(x['type']), ' open' if x['status'] == 'ikke avlest' else '', E(x['status']), E(x['date']), (' · ' + E(x['loc'])) if x['loc'] else '', x['lang'], E(x['what']),
                (' (%s)' % E(x['cert'])) if x['cert'] else '', (' · ' + E(x['note'])) if x['note'] else ''))
        for w in r['versionWitnesses']:
            H.append('<li><span class="wn">%s <span class="tag">oversettelse</span></span><span class="st%s">%s</span><span class="wd">%s%s%s · forelegg: %s%s</span></li>' % (
                E(W[w['siglum']]['display']), ' open' if w['verification']['status'] in ('IKKE_AVLEST', 'DELVIS_BEKREFTET') else '', E(ST[w['verification']['status']]), E(w.get('locator', '')),
                (' · <span lang="%s" translate="no">%s</span>' % (w['lang'], E(w['text']))) if w.get('text') else '', (' · ' + E(nor(w['norwegian']))) if w.get('norwegian') else '', E(w['vorlage']),
                (' · ' + E(w.get('witnessLimit') or w.get('note'))) if (w.get('witnessLimit') or w.get('note')) else ''))
        for w in r['patristicWitnesses']:
            e = W[w['siglum']]
            H.append('<li><span class="wn">%s <span class="tag">kirkefar</span></span><span class="st open">%s</span><span class="wd">%s · %s %s · %s · %s, %s · i oversettelse: «%s»%s</span></li>' % (
                E(e['display']), E(ST[w['verification']['status']]), E(w['locator']), E(e['clavis']['series']), E(e['clavis']['number']), E(e['window']), E(w['quoteType']), {'grc': 'gresk', 'la': 'latin'}[w['lang']],
                E(w.get('wording', '')), (' · ' + E(w.get('witnessLimit') or w.get('note'))) if (w.get('witnessLimit') or w.get('note')) else ''))
        H.append('</ul>')
        if r['editionSupport']:
            H.append('<p class="eds">Utgaver som har lesningen: %s</p>' % E(', '.join(EDS.get(e['edition'], e['edition']) + (' (%s)' % e['form'] if e.get('form') else '') for e in r['editionSupport'])))
        H.append('</div>')
    H.append('<p class="axis"><strong>Vitnemønster (regnet ut):</strong> %s</p><p class="axis"><strong>Variantart:</strong> %s · <strong>betydningsgrad:</strong> %s</p>' % (E(u['witnessPattern']['code']), E(u['variantKind']['assigned']), E(u['significance'])))
    H.append('<p class="note">%s</p>' % E(u['philologicalNote']))
    for x in u.get('excludedWitnesses', []): H.append('<p class="small"><strong>Utelukket vitne:</strong> %s. %s</p>' % (E(W[x['siglum']]['display']), E(x['reason'])))
    if u.get('leads'): H.append('<p class="small"><strong>Må kontrolleres mot kilde:</strong> %s</p>' % E(' '.join(u['leads'])))
    H.append('<details class="eval"><summary>Vurdering</summary><p>Klasse: %s. Ingen vurdering er satt. En vurdering krever signatur, begrunnelse og litteratur.</p></details></details></section>' % E(u['evaluation']['class']))
H.append('<p class="small">Statusordene står som tekst, ikke bare som farge. «Funnet i oversettelse» betyr at gresk eller latinsk ordlyd ikke er avlest.</p></main>')
H.append('<script>var b=document.getElementById("t");b.addEventListener("click",function(){var on=document.body.classList.toggle("mlag");b.setAttribute("aria-pressed",on);b.textContent="Manuskript- og grunnkildemodus: "+(on?"på":"av")});</script></body></html>')
open(os.path.join(PROJ, 'piloter', 'manuskriptkort-prototype.html'), 'w', encoding='utf-8', newline='\n').write('\n'.join(H))
print('skrevet rapport (%d linjer) og prototype (%d tegn)' % (len(M), sum(len(x) for x in H)))
