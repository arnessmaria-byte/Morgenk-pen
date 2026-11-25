"""Merge two bounded critical-edition results on a local staging copy. Never write G:.
Usage: python -B migrer_origenes.py INPUT_ROOT LOCAL_STAGING_ROOT  (input/read and output may be the same local staging tree)
       python -B migrer_origenes.py --verify LOCAL_STAGING_ROOT
Only writes piloter/trinn0-10-piloter.json, kilder/belegg/origenes-koetschau.json, and ONE audit file beside this script.
Keep the existing report generator: regenerate reports after all pilot updates.
"""
import argparse,collections,copy,hashlib,importlib.util,json,sys,unicodedata
from pathlib import Path
import jsonschema
P=Path(__file__).resolve().parent;ALLOWED=P.parent.resolve()
pilot=Path('piloter/trinn0-10-piloter.json');ev=Path('kilder/belegg/origenes-koetschau.json')
def sha(x):return hashlib.sha256(x).hexdigest()
def j(p):return json.loads(p.read_bytes())
def dump(p,x):p.parent.mkdir(exist_ok=True,parents=True);p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode())
def norm(s):return unicodedata.normalize('NFC',s)
def mapunit(x,book):return next(u for u in x['units'] if u['ref']['r10']==book)
def pat(u,r):return next(x for x in u['readings'] if x['readingId']==r)['patristicWitnesses']
def counts(p):
 c=collections.Counter()
 for u in p['units']:
  for r in u['readings']:
   for tag in ('manuscriptWitnesses','versionWitnesses','patristicWitnesses','editionSupport'):
    for w in r[tag]:c[(tag,w['verification']['status'])]+=1
 return {k+':'+s:n for (k,s),n in sorted(c.items())}
original=P/'origenes-to-steder-cc-by-sa.json'
assert sha(original.read_bytes())=='5ff4145b1ea58d0ea0ba254f158da182bbc0770d3c47178e5d7f7c2f8144af9c'
e=j(original);assert e['licence']=='https://creativecommons.org/licenses/by-sa/4.0/' and len(e['entries'])==2
credit='Paul Koetschau (red.), Origenes Werke I (1899); Perseus Project / Trustees of Tufts University, CC BY-SA 4.0, https://creativecommons.org/licenses/by-sa/4.0/.'
def verify(p,x):
 evidence=j(p/ev); raw=evidence['sourceSha256']; assert raw==e['sourceSha256']; mt,jt=(mapunit(x,b) for b in ('Mark 1,1','Joh 1,18'))
 m=[w for w in pat(mt,'c') if w['siglum']=='Orig-Cels']; assert len(m)==1;m=m[0];v=m['verification']
 assert v['evidence']==ev.as_posix()+'#Orig-Cels@II.4' and v['sha256']==raw and v['status']=='BEKREFTET_UTGAVETEKST'
 for orig,frag in zip(e['entries'],['Orig-Cels@II.4','Orig-Cels@II.71']):
  rec=evidence['records'][frag]; assert rec['greek']==orig['greek'] and rec['cts']==orig['cts'] and rec['printPage']==orig['printPage'] and rec['sourceSha256']==raw
  assert rec['historicalANF']['verification']['evidence'].endswith('#'+frag) and rec['provenanceInput']['sha256']==sha(original.read_bytes())
  if orig['bookRef']=='Mark 1,1':assert m['wording']==rec['greek'] and credit in m['witnessLimit'] and rec['function']=='attestedQuotation'
  else:assert rec['function']=='unassignedParallel' and rec['greek'] in jt['philologicalNote'] and rec['historicalANF']['wording'] in jt['philologicalNote'] and credit in jt['philologicalNote']
 assert not any(w['siglum']=='Orig-Cels' and ('II.71' in w.get('locator','')) for r in jt['readings'] for w in r['patristicWitnesses'])
 assert 'Orig-Cels II.71' not in json.dumps(jt['witnessPattern'],ensure_ascii=False)
def run(src,out):
 assert ALLOWED in out.parents and str(out.drive).lower()!='g:' and out!=P, ('unsafe output',out)
 x=j(src/pilot);before=counts(x); source=j(src/'registre/vitneregister.json')
 m,jt=(mapunit(x,b) for b in ('Mark 1,1','Joh 1,18'))
 M=[w for w in pat(m,'c') if w['siglum']=='Orig-Cels' and w['locator']=='II.4']
 J=[w for w in pat(jt,'a') if w['siglum']=='Orig-Cels' and w['locator']=='II.71']
 assert len(M)==len(J)==1,(len(M),len(J)); mark=M[0];john=J[0]
 for w in M+J:assert w['verification']['status']=='BEKREFTET_I_OVERSETTELSE' and w['verification']['sha256']=='b9f385a048c18158c2f74dcd37062f48a1c68a5d05bdb07270a93692d172da2e'
 byid={entry['bookRef']:entry for entry in e['entries']}
 data={k:v for k,v in e.items() if k not in ('editions','entries')};data['records']={}
 for orig,frag,old,fun in [(byid['Mark 1,1'],'Orig-Cels@II.4',mark,'attestedQuotation'),(byid['Joh 1,18'],'Orig-Cels@II.71',john,'unassignedParallel')]:
  data['records'][frag]=dict(orig,sourceSha256=e['sourceSha256'],function=fun,historicalANF=copy.deepcopy(old),provenanceInput={'file':original.name,'sha256':sha(original.read_bytes())})
 zm=byid['Mark 1,1'];zj=byid['Joh 1,18'];mark['wording']=zm['greek'];mark['witnessLimit']=zm['limit']+' '+credit;mark['verification']={'status':'BEKREFTET_UTGAVETEKST','evidence':ev.as_posix()+'#Orig-Cels@II.4','sha256':e['sourceSha256'],'basis':'Kritisk gresk tekst, I s. 131, Contra Celsum II.4, CTS 2.4; digital utgave. Ingen bildeavlesing eller ny menneskelig attest.'}
 pat(jt,'a').remove(john)
 oldNote='Sitatene er bare funnet i engelsk oversettelse, og et latinsk eller oversatt sitat viser ikke artikkelen.'
 assert jt['philologicalNote'].count(oldNote)==1
 jt['philologicalNote']=jt['philologicalNote'].replace(oldNote,'Et latinsk eller oversatt sitat avgjør ikke den greske artikkelen.')
 jt['philologicalNote']+=' Origenes, Contra Celsum II.71 (I s. 193): «'+zj['greek']+'». ANF har «'+john['wording']+'». Denne greske parallellen har θεός med innskutte ord; den er ikke ført som støtte for a, b eller c. '+credit+' Kilde: '+ev.as_posix()+'#Orig-Cels@II.71.'
 # The original count routine includes supports by location. Recompute after removing one.
 spec=importlib.util.spec_from_file_location('local_monster',src/'verktoy/monster.py');mym=importlib.util.module_from_spec(spec);spec.loader.exec_module(mym)
 for unit in [m,jt]:unit['witnessPattern']=mym.pattern(unit,source)
 after=counts(x);delta={k:after.get(k,0)-before.get(k,0) for k in set(before)|set(after) if before.get(k,0)!=after.get(k,0)}
 assert delta=={'patristicWitnesses:BEKREFTET_I_OVERSETTELSE':-2,'patristicWitnesses:BEKREFTET_UTGAVETEKST':1},delta
 jsonschema.Draft202012Validator(j(src/'registre/schema-manuscript-layer.json')).validate(x)
 for dest in [out/pilot,out/ev]:
  if dest.exists() and not(dest==src/pilot and src==out):raise FileExistsError(dest)
 dump(out/ev,data);dump(out/pilot,x);verify(out,j(out/pilot))
 audit=dict(delta=delta,before=before,after=after,priorTotal=sum(before.values()),afterTotal=sum(after.values()),unassignedParallels=1,schemaPassed=True,fragmentAndTextVerified=True,inputPilotSha256=sha((src/pilot).read_bytes()) if src!=out else None,afterPilotSha256=sha((out/pilot).read_bytes()),evidenceSha256=sha((out/ev).read_bytes()))
 dump(P/'migrering-origenes-kvittering.json',audit);print(json.dumps(audit,ensure_ascii=False))
if __name__=='__main__':
 if len(sys.argv)==3 and sys.argv[1]=='--verify':
  o=Path(sys.argv[2]);verify(o,j(o/pilot));print('PASS: begge fragmentene, originaltekst og utflyttet parallell.')
 elif len(sys.argv)==3:run(Path(sys.argv[1]).resolve(),Path(sys.argv[2]).resolve())
 else:raise SystemExit(__doc__)

