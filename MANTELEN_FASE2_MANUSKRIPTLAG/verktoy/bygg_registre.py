#!/usr/bin/env python3
"""Trinn 0, steg 2: skriver registre/kildelisenser.json og registre/schema-manuscript-layer.json.

Bruk: bygg_registre.py <prosjektmappe>
Lisensstatus er fagledelsens forslag med belegg. Captain godkjenner lisensporten (plan 7.6 og 7.7).
"""
import json, os, sys

PROJ = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = lambda f: json.load(open(os.path.join(PROJ, 'kilder', 'belegg', f), encoding='utf-8'))


def dump(rel, obj):
    p = os.path.join(PROJ, rel)
    with open(p, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(obj, f, ensure_ascii=False, indent=1); f.write('\n')


def src(id_, name, layer, status, license_, basis, evidence, use, conditions=None, open_points=None, **extra):
    d = {'id': id_, 'name': name, 'layer': layer, 'status': status, 'license': license_, 'basis': basis,
         'evidence': evidence, 'useInLayer': use, 'conditions': conditions or [], 'openPoints': open_points or [],
         'captainApproval': {'approved': None, 'by': None, 'date': None}}
    d.update(extra)
    return d


nt, sw, dss, tr, mam = B('nt-utgaver-utdrag.json'), B('swete-utdrag.json'), B('etcbc-dss-utdrag.json'), B('intf-transkripsjoner.json'), B('mam-utdrag.json')
EV_READ, EV_DATA, EV_R10, EV_NONE = 'lisenstekst lest i Trinn 0', 'oppgitt i datasettet', 'oppgitt i låst R10', 'ikke kontrollert i Trinn 0'

sources = [
 src('WLC-OSHB', 'Westminster Leningrad Codex / Open Scriptures Hebrew Bible', 'GT hovedtekst (MT etter Leningrad B19A)', 'fri_tekst',
     'WLC: public domain. OSHB lemma og morfologi: CC BY 4.0.', 'Kilden er allerede i låst R10 med kreditering.',
     {'type': EV_R10, 'ref': 'attribution-feltet i R10-bokfilene (gt-isa.json m.fl.), OSHB-revisjon 3d15126fb1ef74867fc1434be1942e837932691f'},
     'Ankertekst. Laget leser R10-filene og endrer dem ikke.', ['Navngivelse for OSHB-morfologien (CC BY 4.0).']),
 src('MAM', 'Miqra according to the Masorah (MT etter Aleppo der kodeksen er bevart)', 'GT sammenligning', 'fri_tekst',
     'CC BY-SA (slik Sefaria oppgir for versjonen «Miqra according to the Masorah»).', 'Lisensfeltet i API-svaret for de fem pilotversene.',
     {'type': EV_DATA, 'ref': 'kilder/belegg/mam-utdrag.json', 'quote': sorted({r['license'] for r in mam['records'].values()})},
     'Utgavefelt (hvilken lesning MAM har). Full sammenligning WLC–MAM hører til senere trinn.',
     ['Navngivelse.', 'Del på samme vilkår (SA).'],
     ['Lisensversjonen (3.0 eller 4.0) må leses hos kilden på hebraisk Wikisource.', 'SA-vilkåret må vurderes før MAM-tekst legges i et lag som gis ut sammen med vernet materiale.',
      'Hvilke avsnitt Aleppo-kodeksen faktisk bevarer, hentes fra MAM-dokumentasjonen. Det er ikke registrert i Trinn 0.']),
 src('SWETE', 'H. B. Swete, The Old Testament in Greek according to the Septuagint', 'LXX grunntekst', 'fri_tekst',
     'Trykt utgave: fri. Digital tekst (nathans/lxx-swete, avledet av First1KGreek): ' + sw['license'].split(' (')[0] + '.',
     'README i datasettet oppgir lisensen for den digitale teksten.',
     {'type': EV_READ, 'ref': 'kilder/belegg/swete-utdrag.json', 'commit': sw['commit'], 'quote': 'The Greek text and its annotations in the data directory are published under the terms of the Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0) license.'},
     'LXX-lesninger med ordrett norsk. Brukes allerede i R10-notene.', ['Navngivelse og del på samme vilkår for den digitale teksten.'],
     ['Den digitale teksten er OCR-avledet og har tap i 5 Mos 32:43. Den kan ikke importeres uten korrektur mot trykt utgave.'], qualityWarning=sw['qualityWarning']),
 src('VON-GALL', 'A. von Gall, Der hebräische Pentateuch der Samaritaner (1914–1918)', 'Den samaritanske Pentateuk, grunntekst', 'fri_tekst',
     'Trykt utgave antatt fri på grunn av alder.', 'Planens vedlegg A. Ikke etterprøvd i Trinn 0.', {'type': EV_NONE},
     'Ingen SP-lesning er registrert som bekreftet vitne i pilotene.', [],
     ['Vernetiden etter utgiverens dødsår er ikke kontrollert.', 'Ingen maskinlesbar transkripsjon er funnet eller hentet.']),
 src('SCR1894', 'F. H. A. Scrivener, The New Testament in the Original Greek (1894)', 'NT hovedtekst (strøm 4)', 'fri_tekst',
     'Fri.', 'Kilden er allerede i låst R10. Leseren krediterer datagrunnlaget.',
     {'type': EV_R10, 'ref': 'source-feltet i R10-bokfilene og krediteringen i den publiserte leseren («Scrivener 1894: Honza Pokorny (data til fri bruk)»)'},
     'Ankertekst. Utgave, ikke vitne.'),
 src('RP2018', 'Robinson–Pierpont, The New Testament in the Original Greek: Byzantine Textform (2018)', 'NT bysantinsk utgave (strøm 3)', 'fri_tekst',
     'Public domain.', 'LICENSE i byztxt/byzantine-majority-text.',
     {'type': EV_READ, 'ref': 'kilder/belegg/nt-utgaver-utdrag.json', 'commit': nt['sources']['RP2018']['commit'], 'quote': 'THIS REPOSITORY, INCLUDING CODE AND TEXTUAL CONTENTS, IS IN THE PUBLIC DOMAIN.'},
     'Utgavefelt. Utgave bygd på flertallet av vitnene, ikke et vitne.'),
 src('THGNT', 'The Greek New Testament, produced at Tyndale House, Cambridge', 'NT utgavevalg og referanse', 'kun_henvisning',
     'Tekstens egen lisens er ikke lest i Trinn 0.', 'Utgavevalget hentes fra STEPBible TAGNT, som merker THGNT-ord med «Tyn».',
     {'type': EV_NONE, 'ref': 'kilder/belegg/nt-utgaver-utdrag.json (TAGNT)'},
     'Bare hvilken lesning utgaven har, hentet fra TAGNT.', [], ['Lisensen leses hos Tyndale House før THGNT-tekst importeres.', 'Utgavevalgene er belagt med én kilde (TAGNT) og bør leses mot utgaven.']),
 src('TREG', 'S. P. Tregelles, The Greek New Testament (1857–1879)', 'NT utgavevalg', 'fri_tekst',
     'Trykt utgave: fri.', 'Alder. Den digitale transkripsjonens lisens er ikke lest.', {'type': EV_NONE, 'ref': 'TAGNT («Treg»)'},
     'Bare hvilken lesning utgaven har, hentet fra TAGNT.', [], ['Lisensen for digital Tregelles-tekst leses før import.']),
 src('TISCH8', 'C. Tischendorf, Novum Testamentum Graece, editio octava critica maior (1869–1872)', 'NT utgavevalg', 'fri_tekst',
     'Public domain.', 'README i morphgnt/tischendorf-data (word-per-line 2.8) oppgir Public Domain.',
     {'type': EV_READ, 'ref': 'kilder/belegg/nt-utgaver-utdrag.json', 'commit': nt['sources']['TISCH8']['commit']},
     'Utgavefelt. Tischendorfs apparat er ikke hentet.'),
 src('WH', 'Westcott–Hort, The New Testament in the Original Greek (1881)', 'NT utgavevalg', 'fri_tekst',
     'Trykt utgave: fri.', 'Alder.', {'type': EV_NONE, 'ref': 'TAGNT («WH»)'}, 'Bare hvilken lesning utgaven har, hentet fra TAGNT.'),
 src('SBLGNT', 'SBL Greek New Testament (2010)', 'NT utgavevalg', 'kun_henvisning',
     'Lisensen er ikke lest i Trinn 0.', 'Planens vedlegg A: avklares.', {'type': EV_NONE, 'ref': 'TAGNT («SBL»)'},
     'Bare hvilken lesning utgaven har, hentet fra TAGNT.', [], ['Lisensen leses før tekst importeres.']),
 src('TAGNT', 'STEPBible TAGNT (Translators Amalgamated Greek NT), Tyndale House', 'NT utgavefelt per ord', 'fri_tekst',
     'CC BY 4.0.', 'Filhodet i begge TAGNT-filene. Samme revisjon som R11-ordlaget bruker.',
     {'type': EV_READ, 'ref': 'kilder/belegg/nt-utgaver-utdrag.json', 'revision': nt['sources']['TAGNT']['revision'], 'fileSha256': nt['sources']['TAGNT']['fileSha256'],
      'quote': 'TAGNT Mat-Jhn - Translators Amalgamated Greek NT - STEPBible.org CC BY 4.0'},
     'Kilde for hvilke utgaver som har hvilket ord (NA28, NA27, THGNT, SBLGNT, WH, Tregelles).', ['Navngivelse.'],
     ['Utgavefeltet for τοῦ i Mark 1:1 fører opp NA28, mens ordtypen i samme rad og Robinson–Pierponts variantnote sier at NA-teksten mangler artikkelen. Avviket er registrert i pilot 6.']),
 src('INTF-LISTE', 'INTF, Kurzgefasste Liste der griechischen Handschriften des Neuen Testaments (via NTVMR)', 'Register over NT-håndskrifter', 'kun_henvisning',
     'INTFs database. Ingen åpen lisens er oppgitt for registeret.', 'Laget gjengir siglum, datering og oppbevaringssted som faktaopplysninger med henvisning og lenke. Registeret kopieres ikke.',
     {'type': EV_NONE, 'ref': 'kilder/belegg/intf-liste.json (hentet via NTVMR API 2026-11-25, SHA-256 per svar)'},
     'Alle NT-sigla, dateringer og oppbevaringssteder i vitneregisteret.', [], ['Skriftlig avklaring med INTF om bruk av API-et når laget settes i drift.']),
 src('INTF-TRANSKR', 'INTF/NTVMR, publiserte transkripsjoner av NT-håndskrifter', 'NT vitner (strøm 1)', 'fri_tekst',
     'CC BY 4.0.', 'Oppgitt i TEI-hodet til hver transkripsjon som er hentet.',
     {'type': EV_READ, 'ref': 'kilder/belegg/intf-transkripsjoner.json', 'quote': '(C) 2026 Institut für Neutestamentliche Textforschung. This work is licensed under a Creative Commons Attribution 4.0 Unported License'},
     'Belegg for hva hver hånd har på stedet. Utdragene ligger i kilder/belegg med SHA-256 for hvert API-svar.', ['Navngivelse.']),
 src('DJD-TOV', 'Discoveries in the Judaean Desert; Tov, Revised Lists of the Texts from the Judaean Desert; Ulrich, The Biblical Qumran Scrolls', 'Qumran: utgaver og register', 'kun_henvisning',
     'Vernet.', 'Planens vedlegg A.', {'type': EV_NONE}, 'Henvisning. Datering og bokstavindeks for rullene hentes herfra av navngitt leser.'),
 src('ETCBC-DSS', 'ETCBC/dss (Text-Fabric), Martin Abeggs transkripsjoner av Dødehavsrullene', 'Qumran: maskinlesbar transkripsjon', 'krever_avtale',
     'CC BY-NC 4.0.', 'README og LICENSE i datasettet.',
     {'type': EV_READ, 'ref': 'kilder/belegg/etcbc-dss-utdrag.json', 'commit': dss['commit'], 'quote': 'This dataset is licensed under a Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0).'},
     'I Trinn 0 bare kontroll av lesninger i fem vers (ikke-kommersiell forskningsbruk med kreditering). Laget lagrer lesningen og stedet, ikke datasettet.',
     ['Navngivelse.', 'Ikke kommersiell bruk.'], ['Avtale med rettighetshaver før transkripsjonene importeres i et lag som følger en trykt utgave til salgs.']),
 src('LEON-LEVY', 'Leon Levy Dead Sea Scrolls Digital Library (Israel Antiquities Authority)', 'Qumran: bilder og katalog', 'kun_henvisning',
     'Vernet. Ingen åpen lisens oppgitt.', 'Bare lenker og katalogopplysninger. Bilder lagres ikke.', {'type': EV_NONE, 'ref': 'kilder/belegg/leon-levy-utdrag.json'},
     'Bildelenker, periodebetegnelse og henvisning til offisiell utgave for rullene.'),
 src('RAHLFS-GOTT', 'Rahlfs 1935; Rahlfs–Hanhart 2006; Septuaginta Gottingensis; Rahlfs–Fraenkel, Verzeichnis', 'LXX: utgaver og register', 'kun_henvisning',
     'Rahlfs–Hanhart og Göttingen-utgavene er vernet. Rahlfs 1935 er ikke avklart.', 'Planens vedlegg A.', {'type': EV_NONE},
     'Henvisning. LXX-håndskrifter registreres først når siglum og datering er lest i Verzeichnis.'),
 src('NA28', 'Nestle–Aland 28 (med UBS5 og Editio Critica Maior)', 'NT eklektisk tekst og apparat', 'kun_henvisning',
     'Vernet tekst og apparat.', 'Planens vedlegg A.', {'type': EV_NONE},
     'Bare hvilken lesning NA-teksten har, hentet fra frie kilder (Robinson–Pierponts variantnoter og TAGNT). Apparat og notetekst kopieres ikke.', [],
     ['NA28-valgene i pilotene er belagt sekundært og bør leses mot utgaven av navngitt leser.']),
 src('CLAVIS', 'Clavis Patrum Graecorum / Clavis Patrum Latinorum (Clavis Clavium, Brepols, åpen tilgang)', 'Register over fedre og verk', 'kun_henvisning',
     'Vernet database med åpen lesetilgang.', 'Nummer, plassering og tittel gjengis som faktaopplysninger med lenke.', {'type': EV_NONE, 'ref': 'kilder/belegg/clavis-utdrag.json'},
     'Alle Clavis-numre i vitneregisteret er slått opp i basen 2026-11-25.'),
 src('PATR-UTG', 'Kritiske utgaver av fedrene (Sources Chrétiennes, GCS, CCSL, GNO m.fl.)', 'Fedrenes tekst', 'kun_henvisning',
     'Vernet.', 'Planens vedlegg A.', {'type': EV_NONE}, 'Henvisning. Ordlyden på gresk og latin leses her av navngitt leser.'),
 src('ANF-NPNF', 'Ante-Nicene Fathers og Nicene and Post-Nicene Fathers (engelsk, 1885–1900), tekstfiler fra CCEL', 'Fedrene i oversettelse', 'fri_tekst',
     'Fri.', 'Alder.', {'type': EV_NONE, 'ref': 'kilder/belegg/fedre-oversettelse-utdrag.json (SHA-256 per bind)'},
     'Bare til å bekrefte at et sted finnes og hva oversettelsen har. Aldri som belegg for gresk eller latinsk ordlyd.'),
 src('VG-CLEM', 'Vulgata Clementina (digital tekst: scrollmapper/bible_databases)', 'Latinsk oversettelse', 'fri_tekst',
     'Teksten er fri. Repoet er MIT-lisensiert.', 'Alder og repoets lisens.', {'type': EV_NONE, 'ref': 'kilder/belegg/vulgata-clementina-utdrag.json'},
     'Latinsk lesning i den trykte Vulgata-tradisjonen. Vulgata-håndskriftene er ikke registrert.', [], ['Clementina er en utgave fra 1592. Håndskriftene bak leses i Stuttgart-utgavens apparat (vernet).']),
]
internal = [{'id': 'R10', 'name': 'MANTELEN R10/R11.1 (låst)', 'note': 'Prosjektets egen låste utgave: WLC/OSHB i GT og Scrivener 1894 i NT. Utgave, ikke vitne.'}]
dump('registre/kildelisenser.json', {
 'schemaVersion': 'kildelisenser.v1-trinn0', 'generated': '2026-11-25', 'status': 'FORSLAG: venter på Captains godkjenning av lisensporten',
 'statusValues': {'fri_tekst': 'Teksten kan hentes inn med kreditering og eventuelle vilkår som er oppført.',
                  'kun_henvisning': 'Kilden siteres og henvises til. Tekst, apparat og layout kopieres ikke.',
                  'krever_avtale': 'Kilden kan ikke importeres før det foreligger avtale eller lisens.'},
 'evidenceTypes': [EV_READ, EV_DATA, EV_R10, EV_NONE],
 'sources': sources, 'internalEditions': internal,
 'notTreatedInTrinn0': ['UXLC', 'CATSS', 'IGNTP-transkripsjonene', 'Codex Sinaiticus Project', 'CNTTS', 'Hodges–Farstad', 'BHS/BHQ'],
 'rule': 'Ingen data hentes inn i laget før Captain har godkjent kilden skriftlig (plan 7.6).'})

# ---------------- JSON Schema ----------------
VER = {'type': 'object', 'required': ['status'], 'additionalProperties': False, 'properties': {
    'status': {'enum': ['BEKREFTET_ANKER', 'BEKREFTET_TRANSKRIPSJON', 'BEKREFTET_UTGAVETEKST', 'BEKREFTET_SEKUNDAERT', 'BEKREFTET_I_OVERSETTELSE', 'DELVIS_BEKREFTET', 'IKKE_AVLEST']},
    'evidence': {'type': 'string'}, 'sha256': {'type': 'string', 'pattern': '^[0-9a-f]{64}$'}, 'basis': {'type': 'string'}, 'mustReadIn': {'type': 'string'}}}
SIG = {'type': 'string', 'minLength': 1}
NOR = {'type': 'array', 'minItems': 1, 'items': {'type': 'object', 'required': ['text', 'kind'], 'additionalProperties': False, 'properties': {
    'text': {'type': 'string', 'minLength': 1}, 'kind': {'enum': ['ordrett', 'tolkende', 'r10']}, 'note': {'type': 'string'}}}}
schema = {
 '$schema': 'https://json-schema.org/draft/2020-12/schema', '$id': 'https://mantelen.no/schema/mlag.schema.v1-trinn0.json',
 'title': 'MANTELEN manuskriptlag: variantenheter (Trinn 0)',
 'description': 'Validerer skillet mellom utgaver og vitner, de tre adskilte aksene og ordankrene mot låst R10/R11.1. Datering, type og oppbevaringssted lagres bare i vitneregisteret, aldri i enheten.',
 'type': 'object', 'required': ['schemaVersion', 'r10ReleaseId', 'status', 'units'], 'additionalProperties': False,
 'properties': {'schemaVersion': {'const': 'mlag.schema.v1-trinn0'}, 'generated': {'type': 'string'}, 'r10ReleaseId': {'type': 'string'},
                'status': {'enum': ['UTKAST', 'LÅST']}, 'registers': {'type': 'object'}, 'notice': {'type': 'string'},
                'units': {'type': 'array', 'minItems': 1, 'items': {'$ref': '#/$defs/unit'}}},
 '$defs': {
  'verification': VER,
  'gtAnchor': {'type': 'object', 'additionalProperties': False,
   'required': ['testament', 'bookId', 'bookSha256', 'mtRef', 'firstWordId', 'lastWordId', 'relation', 'words'],
   'properties': {'testament': {'const': 'GT'}, 'bookId': {'type': 'string', 'pattern': '^gt-[a-z0-9]+$'}, 'bookSha256': {'type': 'string', 'pattern': '^[0-9a-f]{64}$'},
                  'mtRef': {'type': 'string'}, 'stepPublicationRef': {'type': 'string'}, 'firstWordId': {'type': 'string', 'pattern': '^[0-9A-Za-z]{5}$'},
                  'lastWordId': {'type': 'string', 'pattern': '^[0-9A-Za-z]{5}$'}, 'relation': {'enum': ['erstatter', 'etter', 'hele_verset']},
                  'words': {'type': 'array', 'minItems': 1, 'items': {'type': 'object', 'required': ['id', 'position', 'g'], 'additionalProperties': False,
                            'properties': {'id': {'type': 'string', 'pattern': '^[0-9A-Za-z]{5}$'}, 'position': {'type': 'integer', 'minimum': 1}, 'g': {'type': 'string', 'minLength': 1}}}}}},
  'ntAnchor': {'type': 'object', 'additionalProperties': False,
   'required': ['testament', 'bookId', 'bookSha256', 'chapter', 'verse', 'firstWordIndex', 'lastWordIndex', 'relation', 'words'],
   'properties': {'testament': {'const': 'NT'}, 'bookId': {'type': 'string', 'pattern': '^[0-9a-z]{3}$'}, 'bookSha256': {'type': 'string', 'pattern': '^[0-9a-f]{64}$'},
                  'r11LayerSha256': {'type': 'string', 'pattern': '^[0-9a-f]{64}$'}, 'r111Note': {'type': 'string'},
                  'chapter': {'type': 'integer', 'minimum': 1}, 'verse': {'type': 'integer', 'minimum': 1},
                  'firstWordIndex': {'type': 'integer', 'minimum': 1}, 'lastWordIndex': {'type': 'integer', 'minimum': 1}, 'relation': {'enum': ['erstatter', 'etter', 'hele_verset']},
                  'words': {'type': 'array', 'minItems': 1, 'items': {'type': 'object', 'required': ['wordIndex', 'g'], 'additionalProperties': False,
                            'properties': {'wordIndex': {'type': 'integer', 'minimum': 1}, 'g': {'type': 'string', 'minLength': 1}}}}}},
  'editionSupport': {'type': 'object', 'required': ['edition', 'verification'], 'additionalProperties': False,
   'description': 'En utgave som har valgt lesningen. Utgaver er ikke vitner og har ikke siglum.',
   'properties': {'edition': {'type': 'string'}, 'form': {'type': 'string'}, 'note': {'type': 'string'}, 'verification': VER}},
  'manuscriptWitness': {'type': 'object', 'required': ['siglum', 'verification'], 'additionalProperties': False,
   'description': 'Et fysisk håndskrift. Datering og oppbevaringssted hentes fra vitneregisteret via siglum.',
   'properties': {'siglum': SIG, 'hand': {'type': ['string', 'null'], 'pattern': '^(\\*|C[0-9]?)$'}, 'locator': {'type': ['string', 'null']}, 'reading': {'type': 'string', 'description': 'Hele verset slik transkripsjonen har det for denne hånden.'}, 'attested': {'type': 'string', 'description': 'Utdraget der lesningen står, slik transkripsjonen har det.'},
                  'certainty': {'enum': ['lest', 'usikre bokstaver', 'delvis rekonstruert', 'rekonstruert', 'utelatt', 'ikke avlest']}, 'note': {'type': 'string'}, 'verification': VER}},
  'versionWitness': {'type': 'object', 'required': ['siglum', 'lang', 'vorlage', 'verification'], 'additionalProperties': False,
   'properties': {'siglum': SIG, 'text': {'type': 'string'}, 'lang': {'enum': ['grc', 'la', 'syr', 'cop']}, 'norwegian': NOR, 'readIn': {'type': 'string'}, 'locator': {'type': 'string'},
                  'vorlage': {'enum': ['sikker', 'sannsynlig', 'kan ikke avgjøres']}, 'witnessLimit': {'type': 'string'}, 'compatibleWith': {'type': 'array', 'items': {'type': 'string'}},
                  'note': {'type': 'string'}, 'verification': VER}},
  'patristicWitness': {'type': 'object', 'required': ['siglum', 'locator', 'lang', 'quoteType', 'verification'], 'additionalProperties': False,
   'properties': {'siglum': SIG, 'locator': {'type': 'string', 'minLength': 1}, 'lang': {'enum': ['grc', 'la', 'syr']}, 'quoteType': {'enum': ['sitat', 'parafrase', 'omtale', 'omstridt']},
                  'wording': {'type': 'string'}, 'witnessLimit': {'type': 'string'}, 'compatibleWith': {'type': 'array', 'items': {'type': 'string'}}, 'note': {'type': 'string'}, 'verification': VER}},
  'reading': {'type': 'object', 'additionalProperties': False,
   'required': ['readingId', 'label', 'text', 'lang', 'morphology', 'norwegian', 'editionSupport', 'manuscriptWitnesses', 'versionWitnesses', 'patristicWitnesses'],
   'properties': {'readingId': {'type': 'string', 'pattern': '^[a-z][0-9]?$'}, 'label': {'type': 'string'}, 'isR10': {'type': 'boolean'}, 'agreesWith': {'type': 'string'},
                  'text': {'type': 'string'}, 'textNote': {'type': 'string'}, 'lang': {'enum': ['he', 'grc']}, 'morphology': {'type': 'string', 'minLength': 1}, 'norwegian': NOR,
                  'editionSupport': {'type': 'array', 'items': {'$ref': '#/$defs/editionSupport'}},
                  'manuscriptWitnesses': {'type': 'array', 'items': {'$ref': '#/$defs/manuscriptWitness'}},
                  'versionWitnesses': {'type': 'array', 'items': {'$ref': '#/$defs/versionWitness'}},
                  'patristicWitnesses': {'type': 'array', 'items': {'$ref': '#/$defs/patristicWitness'}}},
   'anyOf': [{'properties': {'manuscriptWitnesses': {'minItems': 1}}}, {'properties': {'versionWitnesses': {'minItems': 1}}}, {'properties': {'patristicWitnesses': {'minItems': 1}}}],
   '$comment': 'Minst ett vitne per lesning (plan 1.2 regel 1). En lesning som bare står i utgaver, kan ikke registreres.'},
  'unit': {'type': 'object', 'additionalProperties': False,
   'required': ['variantId', 'pilotNr', 'status', 'ref', 'anchor', 'readings', 'witnessPattern', 'variantKind', 'significance', 'evaluation', 'philologicalNote', 'checks'],
   'properties': {
    'variantId': {'type': 'string', 'pattern': '^(GT|NT)-[A-Z0-9]{3}-[0-9]{3}-[0-9]{3}-[0-9]{2}$'}, 'pilotNr': {'type': 'integer'}, 'status': {'enum': ['UTKAST', 'LÅST']},
    'ref': {'type': 'object', 'required': ['r10'], 'additionalProperties': False, 'properties': {
        'r10': {'type': 'string'}, 'mtRef': {'type': 'string'}, 'stepPublicationRef': {'type': 'string'}, 'western': {'type': 'string'}, 'lxxRef': {'type': 'string'}, 'ntRef': {'type': 'string'}}},
    'anchor': {'oneOf': [{'$ref': '#/$defs/gtAnchor'}, {'$ref': '#/$defs/ntAnchor'}]},
    'r10Verse': {'type': 'string'},
    'readings': {'type': 'array', 'minItems': 2, 'items': {'$ref': '#/$defs/reading'}},
    'witnessPattern': {'type': 'object', 'required': ['computed', 'code'], 'properties': {'computed': {'const': True}, 'code': {'type': 'string', 'minLength': 1}},
                       'description': 'Akse 1. Regnes maskinelt ut fra vitnene. Skrives aldri for hånd.'},
    'variantKind': {'type': 'object', 'required': ['computed', 'assigned'], 'additionalProperties': False, 'description': 'Akse 2. Beskrivende.',
                    'properties': {'computed': {'type': 'string'}, 'assigned': {'enum': ['ortografisk', 'morfologisk', 'leksikalsk', 'pluss', 'minus', 'ordfølge', 'harmonisering', 'skrivefeil', 'eksegetisk']},
                                   'assignedBy': {'type': 'string'}, 'note': {'type': 'string'}}},
    'significance': {'enum': ['betydning', 'form', 'ortografi']},
    'evaluation': {'type': 'object', 'required': ['class', 'by', 'date', 'arguments', 'literature', 'dissent'], 'additionalProperties': False, 'description': 'Akse 3. Signert faglig skjønn. Settes aldri maskinelt.',
                   'properties': {'class': {'enum': ['ikke vurdert', 'A', 'B', 'C', 'omstridt']}, 'by': {'type': ['string', 'null']}, 'date': {'type': ['string', 'null']},
                                  'arguments': {'type': 'array', 'items': {'type': 'string'}}, 'literature': {'type': 'array', 'items': {'type': 'string'}}, 'dissent': {'type': 'array', 'items': {'type': 'string'}}},
                   'if': {'properties': {'class': {'const': 'ikke vurdert'}}},
                   'then': {'properties': {'by': {'type': 'null'}, 'date': {'type': 'null'}}},
                   'else': {'properties': {'by': {'type': 'string', 'minLength': 1}, 'date': {'type': 'string', 'minLength': 1}, 'arguments': {'minItems': 1}, 'literature': {'minItems': 1}}}},
    'philologicalNote': {'type': 'string', 'minLength': 40},
    'crossReferences': {'type': 'array', 'items': {'type': 'object'}},
    'excludedWitnesses': {'type': 'array', 'items': {'type': 'object', 'required': ['siglum', 'reason'], 'properties': {'siglum': SIG, 'reason': {'type': 'string'}}}},
    'leads': {'type': 'array', 'items': {'type': 'string'}, 'description': 'Spor som må kontrolleres mot kilde. De er ikke vitner og teller ikke i vitnemønsteret.'},
    'dataConflicts': {'type': 'array', 'items': {'type': 'string'}},
    'provenance': {'type': 'array', 'items': {'type': 'object'}},
    'checks': {'type': 'object', 'required': ['sigla', 'anchor', 'unicode', 'doubleEntry'], 'properties': {'doubleEntry': {'enum': ['IKKE KJØRT', 'BESTÅTT']}}}}}}}
dump('registre/schema-manuscript-layer.json', schema)
print('skrevet: registre/kildelisenser.json (%d kilder), registre/schema-manuscript-layer.json' % len(sources))
