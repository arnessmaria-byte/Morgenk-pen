#!/usr/bin/env python3
"""antitese_scan.py: teller engelske AI-mønstre som slop_scan.py ikke fanger.

Bruk: python3 antitese_scan.py MANUS.md [--per-day] [--list] [--json ut.json]

Mønstrene er skrevet for FORGED: andaktsprosa der «not X. It is Y.» og
moralske énlinjers avslutninger er hovedproblemet. Hver kategori har en
grense per dag (40 dager + intro + back matter). Grensene er sperrende.
"""
import re, sys, json, argparse

PATTERNS = {
 # antitese: «X is not A. It is B.» og varianter over to setninger
 "antitese_to_setninger": r"\b(?:is|are|was|does|do|did|has|have)\s+not\b[^.!?;]{0,80}[.;]\s+(?:It|They|He|This|That|You|She|We)\s+(?:is|are|was|does|do|did|has|have)\b",
 # «not X, but Y» / «not X; Y»
 "not_x_but_y": r"\bnot\s+(?:only\s+|just\s+|merely\s+|simply\s+)?[\w’'\- ]{1,40},?\s+but\b",
 "not_because": r"\b[Nn]ot because\b",
 "this_day_is_not_about": r"\bThis day is not about\b",
 "fragment_Not": r"(?:^|[.!?]\s+)Not\s+[\w’' ,]{1,40}[.]",
 "you_are_not_you_are": r"\bYou are not\b[^.!?]{0,60}\.\s+You are\b",
 "this_is_different": r"\bThis is (?:different|not that)\b",
 "signpost": r"\b(?:I want to say plainly|stated plainly|Two final things|One more thing|And one distinction|Of course the picture|The picture is too simple|let me|Here is what|here is what I have found|You will notice|The second is this|so you can trust it|We all know|I will not pretend|You may object)\b",
 "for_some_men": r"\bFor some(?: men)?,",
 "quietly": r"\bquiet(?:ly)?\b",
 "the_question_is": r"\b[Tt]he question is (?:not|no longer)\b",
 "x_does_not_y_it_z": r"\b(?:does|do|did) not\s+\w+\s*(?:\w+\s*){0,4}[.;]\s+It\s+\w+",
}
LIMITS = {  # maks per seksjon (dag); None = bare telles
 "antitese_to_setninger": 1, "not_x_but_y": 1, "not_because": 0,
 "this_day_is_not_about": 0, "fragment_Not": 1, "you_are_not_you_are": 0,
 "this_is_different": 0, "signpost": 0, "for_some_men": None, "quietly": None,
 "the_question_is": 0, "x_does_not_y_it_z": None,
}
TOTAL_LIMITS = {"for_some_men": 8, "quietly": 30}

def sections(text):
    parts = re.split(r"(?m)^(#{1,2} .+)$", text)
    out = [("(start)", parts[0])]
    for i in range(1, len(parts), 2):
        out.append((parts[i].strip("# ").strip(), parts[i+1] if i+1 < len(parts) else ""))
    # slå sammen per dag/kapittel: ## Day N eller # Kapittel
    merged, cur, buf = [], None, ""
    for h, body in out:
        if h.startswith(("Day ","Introduction","Conclusion","Appendix","About","To the One","Foreword","PHASE","Phase")):
            if cur is not None: merged.append((cur, buf))
            cur, buf = h, body
        else:
            buf += "\n## " + h + "\n" + body if cur else body
            if cur is None: cur = h
    if cur is not None: merged.append((cur, buf))
    return merged

def strip(t):
    t = re.sub(r"(?m)^\s*\|.*\|\s*$", " ", t)      # tabeller er bevisste kontraster
    t = re.sub(r"(?m)^>.*$", " ", t)                # skriftsitat
    t = re.sub(r"[*_]", "", t)
    return t

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file"); ap.add_argument("--per-day", action="store_true")
    ap.add_argument("--list", action="store_true"); ap.add_argument("--json")
    ap.add_argument("--allow", help="fil med bevisste unntak, én ordrett frase per linje")
    a = ap.parse_args()
    text = open(a.file, encoding="utf-8").read()
    allowed = []
    if a.allow:
        allowed = [l.strip() for l in open(a.allow, encoding="utf-8") if l.strip() and not l.startswith("#")]
        for ph in allowed:
            if ph not in text.replace("’", "'").replace("‘", "'") and ph not in text:
                print("ADVARSEL: unntaksfrase finnes ikke i manus:", ph)
            text = text.replace(ph, " ").replace(ph.replace("'", "’"), " ")
    secs = sections(text)
    tot = {k: 0 for k in PATTERNS}; brudd = []; rows = []; hits = []
    for name, body in secs:
        b = strip(body); row = {"seksjon": name}
        for k, p in PATTERNS.items():
            ms = list(re.finditer(p, b, flags=re.M))
            row[k] = len(ms); tot[k] += len(ms)
            for m in ms: hits.append((name, k, re.sub(r"\s+", " ", b[max(0,m.start()-40):m.end()+40])))
            lim = LIMITS[k]
            if lim is not None and len(ms) > lim:
                brudd.append(f"{name}: {k} = {len(ms)} (grense {lim})")
        rows.append(row)
    for k, lim in TOTAL_LIMITS.items():
        if tot[k] > lim: brudd.append(f"TOTALT: {k} = {tot[k]} (grense {lim})")
    words = len(re.findall(r"[A-Za-z’']+", strip(text)))
    print(f"Ord: {words}")
    print("Totalt per mønster:"); [print(f"  {k:24} {v}") for k, v in tot.items()]
    if a.per_day:
        keys = list(PATTERNS)
        print("\n" + "seksjon".ljust(44) + " ".join(k[:6] for k in keys))
        for r in rows: print(r["seksjon"][:43].ljust(44) + " ".join(str(r[k]).rjust(6) for k in keys))
    if a.list:
        print("\nTreff:"); [print(f"  [{s[:20]}] {k}: …{c}…") for s, k, c in hits if k not in ("quietly",)]
    if allowed: print(f"\nBevisste unntak (ordrett forfatter, se slop-revisjonen): {len(allowed)}")
    print("\nSperrende brudd:", len(brudd)); [print("  -", b) for b in brudd]
    if a.json: json.dump({"ord": words, "totalt": tot, "brudd": brudd, "rader": rows}, open(a.json, "w"), ensure_ascii=False, indent=1)
    sys.exit(1 if brudd else 0)

if __name__ == "__main__": main()
