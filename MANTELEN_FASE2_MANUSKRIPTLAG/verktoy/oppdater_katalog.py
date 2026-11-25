"""Gjenskap katalogfeltene i en arbeidskopi etter opprinnelig registerbygg. Ingen nett eller korpusskriving."""
import json,sys
from pathlib import Path
def run(P):
    P=Path(P)
    def read(f):return json.loads((P/f).read_bytes())
    def save(f,x):(P/f).write_text(json.dumps(x,indent=1,ensure_ascii=False)+'\n',encoding='utf8',newline='\n')
    def sf(name):return 'kilder/katalogkontroll/'+name
    gfile=sf('katalogfakta-kontroll.json');g=read(gfile)
    ntfile=sf('intf-direkte-kontroll.json');n=read(ntfile)
    wfile='registre/vitneregister.json';lfile='registre/kildelisenser.json';reg=read(wfile);lic=read(lfile)
    W=reg['witnesses']; catalog=read('kilder/belegg/leon-levy-utdrag.json')['records']
    for x in n['entries']:W[x['siglum']]['catalogVerification']={'file':ntfile,'docID':x['docID'],'scope':'INTF-katalogens oppgitte depot(er) og kodexdatering; ingen datering av korrekturhånd.'}
    for w in W.values():
        if w['type'] in ('oversettelse','kirkefar_verk'):
            w.update(repository=None,repositoryStatus='Ikke ett fysisk håndskrift; feltet gjelder ikke for verket eller tradisjonen.')
    specs=read(sf('katalogkilder.json'))
    providers={}
    for ix,r in enumerate(g['sourceFacts']):
        if r.get('facts') and r.get('rawResponseSha256'):providers[r['provider']]=(ix,r)
    for row in g['witnesses']:
        s=row['siglum'];w=W[s];meta=row['existing']; prev=w.get('bibliographicIdentification',w['referenceSource'])
        w['bibliographicIdentification']=prev
        fields={}
        def register(key,file,route,val,source):
            if not val:return
            fields[key]={'file':file,'path':route,'value':val,'source':source}
            w[key]={'catalogLabel':val} if key=='dateRange' else [{'institution':val}]
        inventory=w.get('inventoryNumber') or w.get('etcbcScrollCode')
        if inventory in catalog:
            old=catalog[inventory]; src={'register':'LEON-LEVY','url':old['url'],'sha256':old['rawSha256']}
            register('dateRange','kilder/belegg/leon-levy-utdrag.json',['records',inventory,'period'],old.get('period'),src)
        for label in row['candidateReferences']:
            if label not in providers:continue
            ix,r=providers[label]; facts=r['facts']; src={'register':label,'url':r['url'],'sha256':r['rawResponseSha256']}
            if label=='IAA-HEV-CATALOG':
                register('dateRange',gfile,['sourceFacts',ix,'facts','period'],facts['period'],src)
                w.update(period=facts['period'],site=facts['site'],inventoryNumber=facts['manuscript_id'])
            if label=='LOC-11Q5':
                w['historicalLoan']={'exhibition':'Library of Congress, 1993','lender':facts['lender'],'columns':facts['exhibitedColumns'],'currentRepositoryProven':False,'source':src}
            # Kun datoer fra spesifisert katalog/utgave; vilkårlig datering fra sekundærlitteratur brukes ikke.
            if label in {'NLR-RU','NLR','NLI','IMJ','SI-B','LOC-11Q5','UXLCold','NLR-ALT','IMJ-HEV','IAA-HEV','IAA-HEV-EN'}:
                register('dateRange',gfile,['sourceFacts',ix,'facts','dateLabel'],facts.get('dateLabel'),src)
            if label in {'IMJ','NLR-RU','NLR','NLI','UXLC','IMJ-HEV'}:
                register('repository',gfile,['sourceFacts',ix,'facts','repository'],facts.get('repository'),src)
        for ix,r in enumerate(g['publishedReferenceFacts']):
            if r['siglum']!=s:continue
            if r['provider']=='SI-B-RENDER':
                src={'register':r['provider'],'url':r['url'],'factSha256':r['factHash'],'method':r['status']}
                register('repository',gfile,['publishedReferenceFacts',ix,'facts','repository'],r['facts']['repository'],src)
                w['cataloguedHolding']={k:r['facts'][k] for k in ('place','shelfmark','owner','catalogId')}
                w['repositoryStatus']='Som oppført for 1Q8 i publisert kuratorkatalog; indeksert oppslag, ikke ny fysisk inspeksjon av fragmentet.'
            w.setdefault('publishedReferences',{})[r['provider']]={'file':gfile,'path':['publishedReferenceFacts',ix],'factSha256':r['factHash'],'role':r['role'],'facts':r['facts']}
        if s=='B19A':w['folioReferences']=[{'ref':e['ref'],'folio':e['facts'][0]['folio'],'url':e['url'],'sha256':e['rawResponseSha256']} for e in g['B19AFolioReferences']]
        if fields:
            w['catalogFields']=fields
            w['referenceSource']=(fields.get('dateRange') or fields['repository'])['source']
        if w.get('dateRange'):w['dateStatus']='Ordlyd importert fra angitt kildefelt. Ingen tallfesting utover katalogen.'
        if not w.get('repository'):w['repositoryStatus']='Ikke verifisert for pilotfragmentet; funnsted, digital vert og utlåner er ikke fysisk depot.'
        urls={r['provider']:r['url'] for r in g['sourceFacts']+g['publishedReferenceFacts']}
        w['catalogReferences']=[{'id':i,'url':urls.get(i) or specs.get('captureSources',{}).get(i,specs.get('references',{}).get(i,{})).get('url')} for i in row['candidateReferences']]
    cnt=sum(bool(v.get('dateRange') or v.get('century')) for v in W.values())
    reg['counts'].update(medImportertDatering=cnt,utenDatering=len(W)-cnt)
    reg['physicalCatalogue']={'total':56,'withDateOrNamedPeriod':sum(bool(w.get('dateRange') or w.get('century')) for w in W.values() if w['type'] not in ('oversettelse','kirkefar_verk')),'repositoryMissing':[s for s,w in W.items() if w['type'] not in ('oversettelse','kirkefar_verk') and not w.get('repository')],'dateMissing':[s for s,w in W.items() if w['type'] not in ('oversettelse','kirkefar_verk') and not (w.get('dateRange') or w.get('century'))]}
    save(wfile,reg)
    lic['status']='Captain har godkjent intern kildebruk i Trinn 0 med grensene nedenfor.'
    lic['authorization']={'scope':'trinn0_intern','by':'Captain','date':'2026-11-25','releaseAuthorized':False,'catalogueScope':'Enkeltstående registrerte katalogfakta og kildehenvisning når vilkårene tillater det. Ingen beskyttede bilder, transkripsjoner eller apparater.','textScope':'Faktiske ordformer fra konkret fri utgave på dokumenterte vilkår. Godkjenningen gir ingen rettigheter fra en tredjepart.'}
    ix={r['id']:r for r in lic['sources']}
    sbl=ix['SBLGNT'];sbl.update(license='Digital utgave fra utgiver: CC BY 4.0. Pilotens valg er fortsatt sekundært rapportert, ikke lest i utgaven.',basis='Utgiverens lisens for dagens digitale utgave.',evidence={'type':'lisenstekst lest i Trinn 0','ref':'https://github.com/Faithlife/SBLGNT/blob/master/README.md#license'},openPoints=['Pilotlesningene må kontrolleres direkte før de føres som lest i utgaven.'])
    th=ix['THGNT'];th.update(license='© Tyndale House, Cambridge 2017. Fri lisens for den ønskede tekstbruken er ikke dokumentert.',basis='Utgiverens angivelse i STEP. Henvisning/sekundært utgavevalg i dette laget; ikke import av utgavetekst.',evidence={'type':'utgiverens kildeopplysning','ref':'https://www.stepbible.org/version.jsp?version=THGNT'})
    for r in ix.values():
        if r['id']=='ETCBC-DSS':r['distribution']='Tidligere kontrollutdrag: ikke frigitt for nett, app eller trykk. Ingen ny import.'
    extras={k: (v.get('url'), 'kun_henvisning') for k,v in {**specs.get('references',{}),**specs.get('captureSources',{})}.items()}
    for r in g['sourceFacts']+g['publishedReferenceFacts']: extras[r['provider']]=(r['url'],'kun_henvisning')
    for k in lic.get('notTreatedInTrinn0',[]):
        if k not in extras:extras[k]=(None,'krever_avtale' if k in ['CNTTS','CATSS','IGNTP-transkripsjonene'] else 'kun_henvisning')
    extras.update({'PATR-PD':(None,'fri_tekst'),'BL-CAT':('https://www.bl.uk/','kun_henvisning'),'BAV-CAT':('https://digi.vatlib.it/','kun_henvisning'),'CB-CAT':('https://chesterbeatty.ie/','kun_henvisning'),'BODMER-CAT':('https://fondationbodmer.ch/','kun_henvisning')})
    for k,(url,status) in extras.items():
        if k not in ix:
            r={'id':k,'name':k,'status':status,'evidence':{'ref':url,'type':'kildehenvisning; ingen generell tillatelse'},'useInLayer':('Bare identifisert fri utgave med dokumenterte vilkår.' if k=='PATR-PD' else 'Ingen tekst eller bilder importeres.'),'conditions':[],'openPoints':[]}
            ix[k]=r;lic['sources'].append(r)
    for r in lic['sources']:
        if r['id']=='PATR-PD':
            ev=read('kilder/belegg/origenes-koetschau.json')
            r.update(name='Koetschau (1899), Origenes: Contra Celsum; andre frie utgaver må identifiseres særskilt',evidence={'type':'TEI-lisens kontrollert','ref':ev['source']},license=ev['licence'],conditions=[ev['digitalAttribution'],ev['licenceShareAlike'],ev['changes']])
        rights={'fri_tekst':'tekst_på_dokumenterte_vilkår','kun_henvisning':'katalogfakta_eller_henvisning','krever_avtale':'ingen_import'}[r['status']]
        r['captainApproval']={'approved':rights!='ingen_import','by':'Captain','date':'2026-11-25','scope':rights,'thirdPartyGrant':False}
    save(lfile,lic)
if __name__=='__main__':run(sys.argv[1])
