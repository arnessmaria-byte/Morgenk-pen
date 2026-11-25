"""Prøv fire reelle feilbaner på en ny, isolert filkopi. Berører ikke kildene."""
from pathlib import Path
import sys,shutil,json,subprocess,tempfile,hashlib
def main(r10):
    root=Path(__file__).resolve().parents[1];r10=Path(r10)
    def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
    with tempfile.TemporaryDirectory(prefix='mantelen-trinn0-neg-') as tmp:
        copy=Path(tmp)/'lag';shutil.copytree(root,copy)
        anchor=Path(tmp)/'r10'; lock=json.loads((copy/'registre/r10-laas.json').read_bytes())
        for b in lock['books'].values():
            for field in ('publishedPath','r11LayerPath'):
                if field in b:
                    rel=b[field];p=anchor/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(r10/rel,p)
        def test(label,needle):
            r=subprocess.run([sys.executable,'-B','-X','utf8',str(copy/'validate_trinn0.py'),'--r10-dir',str(anchor)],encoding='utf8',capture_output=True)
            if r.returncode!=1 or needle not in r.stdout:raise RuntimeError((r.returncode,r.stdout[-1000:],r.stderr))
            print(label+': avvist, exit 1')
        path=copy/'piloter/trinn0-10-piloter.json'; original=path.read_bytes()
        def change(mutate):
            v=json.loads(original);mutate(v);path.write_text(json.dumps(v,ensure_ascii=False),encoding='utf8')
        change(lambda v:v['units'].pop(0));test('Utelatt pilot','Bestilte steder eller antall avviker')
        change(lambda v:v['units'][0]['anchor']['words'][0].update(g='AVVIK'));test('Feil ankerord','treffer ikke')
        path.write_bytes(original)
        w=copy/'registre/vitneregister.json';reg=json.loads(w.read_bytes());data=w.read_bytes()
        reg['witnesses']['01']['dateRange']['notAfter']+=1;w.write_text(json.dumps(reg),encoding='utf8')
        test('Feil katalogdato','01: INTF-datering');w.write_bytes(data)
        side=anchor/lock['books']['joh']['r11LayerPath'];side.rename(side.with_suffix('.skjult'))
        test('Manglende R11-ordlag','påkrevd R11-ordlag mangler')
if __name__=='__main__':main(sys.argv[1])
