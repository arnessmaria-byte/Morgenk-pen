#!/usr/bin/env python3
"""Kontrollerer at hvert sidetall i innholdslisten peker på siden der kapitlet faktisk starter."""
import re, sys, pymupdf as fitz
d = fitz.open(sys.argv[1])
pages = [p.get_text() for p in d]
def folio(i):
    # folio = siste linje som bare er tall/romertall, eller utledet fra nabosider
    lines = [l.strip() for l in pages[i].splitlines() if l.strip()]
    for l in reversed(lines):
        if re.fullmatch(r"\d+|[ivxlc]+", l): return l
    return None
toc_text = "\n".join(pages[3:8])
entries = re.findall(r"^(Day \d+ · .+?|PHASE [IV]+ · \w+|Foreword|Introduction|Conclusion · .+?|Appendix [ABC] · .+?|Also by .+?|About the Author)\s*(?:\. )*\.?\s*\n?\s*([ivx]+|\d+)\s*$", toc_text, re.M)
feil = 0
for name, num in entries:
    key = name.split(" · ")[0]
    if key.startswith("Day"):
        pat = re.compile(r"D\s*A\s*Y\s+" + r"\s*".join(key.split()[1]) + r"\b")
        def starts_day(txt):
            for m in pat.finditer(txt):
                if not re.search(r"O\s*F\s*$", txt[:m.start()]): return True
            return False
        hits = [i for i in range(8, len(d)) if starts_day(pages[i].replace("\n", " "))]
    else:
        word = re.sub(r"\s|·|\.", "", key).upper()
        hits = [i for i in range(8, len(d)) if word in re.sub(r"\s|·|\.", "", pages[i]).upper()[:80]]
    if not hits:
        print("FANT IKKE", name); feil += 1; continue
    i = hits[0]
    f = folio(i) or (str(int(folio(i + 1)) - 1) if folio(i + 1) and folio(i + 1).isdigit() else "?")
    ok = (f == num)
    if not ok: feil += 1
    print(("OK  " if ok else "FEIL"), f"{re.sub(r'[ .]+$', '', name)[:44]:44} innhold={num:>4}  faktisk={f}")
print("oppføringer:", len(entries), "feil:", feil)
sys.exit(1 if feil else 0)
