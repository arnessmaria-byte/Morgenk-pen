"""Sjekk redegjørelsen mot de konkrete katalogfeltene. Leser bare lokale vedlegg."""
from pathlib import Path
import hashlib,json
PLACES=(
 ('GT-ISA-053-011-01','gt-isa','Isa.53.11'),('GT-DEU-032-008-01','gt-deut','Deut.32.8'),
 ('GT-DEU-032-043-01','gt-deut','Deut.32.43'),('GT-PSA-022-017-01','gt-ps','Ps.22.17'),
 ('GT-PSA-145-013-01','gt-ps','Ps.145.13'),('NT-MRK-001-001-01','mrk','1:1'),
 ('NT-JOH-001-018-01','joh','1:18'),('NT-ACT-008-037-01','act','8:37'),
 ('NT-1TI-003-016-01','1ti','3:16'),('NT-REV-022-019-01','rev','22:19'))
def avvik(root,units,reg,lic):
    errors=[]
    def test(ok,n):
        if not ok:errors.append(n)
    def read(name):return json.loads((Path(root)/name).read_bytes())
    got=[]
    for u in units:
        a=u['anchor'];got.append((u['variantId'],a['bookId'],a.get('mtRef') or '%s:%s'%(a['chapter'],a['verse'])))
    test(sorted(got)==sorted(PLACES),'Bestilte steder eller antall avviker')
    W=reg['witnesses']; raw=read('kilder/belegg/intf-liste.json')['records'];live=read('kilder/katalogkontroll/intf-direkte-kontroll.json')['entries']
    sig=[v['siglum'] for v in live]
    test(len(sig)==len(set(sig))==47 and set(sig)=={s for s,w in W.items() if w.get('intfDocId')},'INTF-omfang')
    for c in live:
        s=c['siglum'];w=W[s];r=raw[s]
        test(c['docID']==w['intfDocId']==r['docID'] and c['http']==200 and c['datesMatch'] and c['shelfInstancesMatch'] and c['sourceDocumentMatches'],s+': INTF-identitet')
        test(c['responseSha256']==r['rawSha256']==w['referenceSource']['sha256'] and c['url']==r['url']==w['referenceSource']['url'],s+': INTF-kilde')
        test(str(w['century'])==str(r['orig']) and w['dateRange']=={'notBefore':r['origEarly'],'notAfter':r['origLate']},s+': INTF-datering')
        expected=[{k:v.get(src) for k,src in [('institution','institution'),('place','place'),('country','country'),('shelfmark','shelfNumber')]} for v in r['shelfInstances']]
        test(w['repository']==expected and len(expected)==c['returnedShelfCount'],s+': INTF-depot')
    for s,w in W.items():
        test(w['siglum']==s and w.get('referenceSource'),s+': siglum/kilde')
        for key,proof in w.get('catalogFields',{}).items():
            p=read(proof['file'])
            for i in proof['path']:p=p[i]
            test(p==proof['value'],s+': kildeverdi '+key)
            bundle=read(proof['file']); path=proof['path']; source=proof['source']
            if path[0]=='records':
                item=bundle['records'][path[1]]
                test(path[1]==w.get('inventoryNumber') and source['sha256']==item['rawSha256'] and source['url']==item['url'],s+': opphavskontroll katalog')
            else:
                item=bundle[path[0]][path[1]]
                candidate=next(row for row in bundle['witnesses'] if row['siglum']==s)
                test(item['provider'] in candidate['candidateReferences'] and source['register']==item['provider'] and source['url']==item['url'],s+': katalogidentitet')
                fieldhash=hashlib.sha256(json.dumps(item['facts'],sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
                test(fieldhash==item['factHash'] and (source.get('sha256')==item.get('rawResponseSha256') if item.get('rawResponseSha256') else source.get('factSha256')==item['factHash']),s+': kontrollsum katalog')
            if key=='dateRange':
                test(w['dateRange']=={'catalogLabel':p},s+': dateringsetikett')
            elif key=='repository':
                test(w['repository']==[{'institution':p}],s+': depot')
            else:test(False,s+': ukjent katalogfelt')
        if w['type'] in ('rulle','hebraisk_kodeks'):
            for k in ('dateRange','repository'):
                test(not w.get(k) or k in w.get('catalogFields',{}),s+': '+k+' uten belegg')
    test(lic.get('authorization',{}).get('scope')=='trinn0_intern' and not lic['authorization'].get('releaseAuthorized',True),'Godkjenningsomfang')
    for v in lic['sources']:
        test(v.get('status') in ('fri_tekst','kun_henvisning','krever_avtale') and v['captainApproval'].get('scope') in ('tekst_på_dokumenterte_vilkår','katalogfakta_eller_henvisning','ingen_import'),v['id']+': lisensport')
    return errors
