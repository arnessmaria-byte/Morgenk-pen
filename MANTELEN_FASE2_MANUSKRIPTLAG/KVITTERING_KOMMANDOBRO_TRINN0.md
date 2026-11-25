## [FABLE · FASE 2 TRINN 0 · REGISTRE, LISENSPORT OG 10 PILOTSTEDER · UTKAST, IKKE LÅST] 2026-11-25

Denne kvitteringen hører til `MANTELEN_KOMMANDOBRO.md` øverst i Min disk og kan felles inn øverst i den. Skyøkten kan ikke endre fellesfilen (opprettet lokalt av Codex), og ingen PC var koblet til økten.

Levert: G:\Min disk\MANTELEN_FASE2_MANUSKRIPTLAG. 26 filer pluss manifest. Ingen fil i låst R10/R11.1 er endret eller kopiert inn. De ni bokfilene og seks R11-ordlagene ble lest fra www.mantelen.no og har samme SHA-256 som `local-r10-lock.json` (R10-pakke 5704f12b80018fe790cce3a41d6b15d80de7099cf7a2f5a86d187fa897d6e396) og leserens innebygde manifest.

Validator: `validate_trinn0.py`, exit 0, kjørt både mot kopi med låsens SHA-256 og med `--fetch` mot nettstedet.
- JSON Schema: 10 / 10 pilotsteder.
- Ordanker (ord og SHA-256): 10 / 10. GT med `w[].id` og toveis adresse `mtRef` ↔ `stepPublicationRef`. NT med `wordIndex` + `g` + `bookSha256`.
- Sigla i `vitneregister.json`: 96 / 96. Patristiske referanser med Clavis-nummer: 17 / 17. Utgaver i `kildelisenser.json`: 61 / 61. Uregistrerte: 0.
- Dateringer skrevet inn for hånd: 0. 47 oppslag har datering fra INTF-registeret med SHA-256. 22 oppslag har ingen datering og en merknad om hvor den hentes.
- Negativ prøve: endret ankerord og ukjent siglum gir exit 1.

Status: UTKAST. Av 161 vitne- og utgaveopplysninger er 114 lest maskinelt i transkripsjon, utgavetekst eller R10. 47 må leses i kilden av navngitt leser før låsing: 25 utgavevalg ført etter frie datasett (NA28, THGNT, SBLGNT, WH, Tregelles), 17 fedresitater funnet bare i engelsk oversettelse, 1 delvis lest (Swete 5 Mos 32:43) og 4 ikke avlest (D 06 to hender, 046, Vetus Latina). Dobbel registrering er ikke kjørt. Akse 3 står som «ikke vurdert» i alle ti. Lisensporten (23 kilder) venter på Captain.

Funn som krever avgjørelse:
- Åp 22,19: P (025) er ikke vitne. INTFs sideindeks viser at håndskriftet slutter med Åp 22,2–6.
- Apg 8,37: verset står i tre greske former. Ingen transkribert håndskrift har nøyaktig Scriveners ordlyd.
- 1 Tim 3,16: D* og D² er ikke avlest. Ingen før-nikensk far er funnet med ordrett sitat.
- Rullene, B19ᴬ og fedrene har ingen årstall i registeret. De hentes fra DJD, Tov og utgavene.
- Pilotlisten følger oppdraget. Planens vedlegg B har 1 Sam 10,27b, Luk 23,34a, Mark 16,9–20 og 1 Joh 5,7–8 der oppdraget har Mark 1,1, Joh 1,18, Apg 8,37 og 1 Tim 3,16.
- Nettstedets mellomlager gir eldre kopier av `joh.json` og `1ti.json` uten versjonsparameter.

Rapport: G:\Min disk\MANTELEN_FASE2_MANUSKRIPTLAG\piloter\RAPPORT_TRINN0_10_PILOTER.md
Samlet manifest (26 filer): G:\Min disk\MANTELEN_FASE2_MANUSKRIPTLAG\SHA256SUMS.txt · SHA-256 f3d7bf0f92ffc0582d526d2f85731f4464508acba58e2e611e97f381c9a89c17

SHA-256 for alle Trinn 0-filene (stier fra mappen):

~~~text
900becfb499267dd6fea2f935c06606694545088a360603ab0e82db233abd355  LES-MEG.md
2e5decc9b95797a1716d87823bf1178642207418987feb35215107e8c0218431  kilder/belegg/clavis-utdrag.json
79c430c56cd02c7f3113b95dacea492b5e323032d7d991532274ed6fe0501f77  kilder/belegg/etcbc-dss-utdrag.json
9deaecd9b31bcd8e119d6600cdcc53f74a6bcfa234cd0304cca330237a59b754  kilder/belegg/fedre-oversettelse-utdrag.json
889060164dea06bd8431658658a6fe3bded902081466282a895bf83a9dd5a566  kilder/belegg/intf-liste.json
6d7bd871b82e2a2b05de9a3d211f43ad2db7910b5a4e4f2c46c652ac1d7d208e  kilder/belegg/intf-transkripsjoner.json
5f33a8f9772b0b9734ff53a73cd14966e7252ec87da557a87b3b95f04937319f  kilder/belegg/leon-levy-utdrag.json
2bd73be24cdf6ef994cdcd56788ec89f02a693dd05b67f385238db4b307170d7  kilder/belegg/mam-utdrag.json
eb3752dede5d1c02f3e43d8eb73561cd6c7657ae64136a3cdf1cbbfa563bd34f  kilder/belegg/nt-utgaver-utdrag.json
d14346132aee5eb9508bda60cd1a1681ba3ea27dcee9be7e692595838325e15c  kilder/belegg/proveniens.json
a301528f4ecff2d435224b472dbf2ddf90ed299983ce027128757e9d6606fe09  kilder/belegg/swete-utdrag.json
5e9aa1855827d71aafb98d397b043f8a8d399bf8d05c4a605385a228621c6f8a  kilder/belegg/vulgata-clementina-utdrag.json
0d54fc44ec3b97c5462b8a5ceb53f1af2c333a1a4577b6593ca90011b28daba4  piloter/RAPPORT_TRINN0_10_PILOTER.md
2a0b8badc12a252f62fbeea406365aec829d46381b933bf58e209cc9a4ef73e1  piloter/VALIDERING_TRINN0.txt
13b88b20d7132b7aa5e80cece43b76c15ae2bd5246a44cb2aee50fc4ab6b94ec  piloter/manuskriptkort-prototype.html
7937184eefe6ec18897149d861a5ba247f4058ba8e47a565025e1b7384885395  piloter/trinn0-10-piloter.json
c7a7ef062aea0eca8b9de95ed9b8b8ec1037369fca5d7ddf601eb0d645696dee  registre/kildelisenser.json
6877a83dd704f688e3d38460ea3f62439d1b816111ff00014f1eb01d89254f3f  registre/r10-laas.json
da3c039f078bb1341723a021309830f40e5a9abd5835b84ce40cdd0110d9db6e  registre/schema-manuscript-layer.json
05df47dfbafd7d3dc5e55bd061148c5c7b428fa83eb23f6abafa942dc487aebc  registre/vitneregister.json
4e0a13ff8754d0334d3837432ec40403692dbb28f5130573a96329112f4cf5b5  validate_trinn0.py
9ff9e7da64e013d7e2ac78ce7276d08bc7b559831910d6c632ba6671f33fb8db  verktoy/bygg_piloter.py
fba37f635d3d69edca2fc096bb437480c994b56cdbb953d89b1d85f08cb1303d  verktoy/bygg_registre.py
4b9bf733f404446afecc133e525d9130cb0c734c7bdae2d3e98045f2c3f8ae44  verktoy/hent_belegg.py
a0430d0a43b7d0917100123d8102289fa31e72478174add2d8df4633d4500422  verktoy/monster.py
c738214743361686ede1bfaa5e711b5acb01eb2e8e3d1e9d781a8e1a58b8751d  verktoy/rapport.py
~~~

Avgjort: Trinn 0 er bygd og validert som utkast. Ikke låst.
