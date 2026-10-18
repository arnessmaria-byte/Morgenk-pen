#!/usr/bin/env python3
"""Lesbarhetsmåling for FORGED (engelsk klarspråk).

Måler brødtekst (ikke overskrifter, epigrafer eller tabeller):
ord, setninger, snitt setningslengde, Flesch Reading Ease, Flesch-Kincaid grade,
andel ord med tre stavelser eller flere, og treff på abstrakte ord fra en fast liste.
Tabellceller telles bare for abstrakte ord.

Bruk:
  python3 lesbarhet.py FIL.md [--per-dag] [--json ut.json] [--ord]
"""
import re, sys, json, argparse, collections

ABSTRAKT = [
    "formation", "formed", "forming", "formative", "alignment", "aligned", "align", "aligns",
    "coherence", "coherent", "integration", "integrated", "integrate", "integrates",
    "orientation", "oriented", "posture", "trajectory", "consolidate", "consolidates",
    "embody", "embodies", "embodied", "density", "gravity", "conviction", "convictions",
    "restraint", "discernment", "agency", "identity", "clarity", "clarified", "durable",
    "sustainable", "consistency", "stewardship", "accountability", "responsiveness",
    "reliability", "presence", "expression", "exposure", "momentum", "intentional",
    "intentionally", "internal", "inwardly", "outwardly", "manifest", "framework",
    "dynamic", "dynamics", "capacity", "resilience", "authenticity", "vulnerability",
]
ABS_RE = re.compile(r"\b(" + "|".join(ABSTRAKT) + r")\b", re.I)


def stavelser(ord_):
    w = ord_.lower()
    w = re.sub(r"[^a-z]", "", w)
    if not w:
        return 0
    if len(w) <= 3:
        return 1
    w = re.sub(r"(?:[^laeiouy]es|ed|[^laeiouy]e)$", "", w)
    w = re.sub(r"^y", "", w)
    n = len(re.findall(r"[aeiouy]{1,2}", w))
    return max(1, n)


def seksjoner(tekst):
    cur, buf, out = "Front", [], []
    for line in tekst.splitlines():
        m = re.match(r"^#{1,2} (.+)", line)
        if m and (line.startswith("# ") or m.group(1).startswith("Day ")):
            out.append((cur, buf)); cur, buf = m.group(1).strip(), []
        else:
            buf.append(line)
    out.append((cur, buf))
    return [(n, b) for n, b in out if any(x.strip() for x in b)]


def mal(linjer):
    prosa, tabell = [], []
    for l in linjer:
        s = l.strip()
        if not s or s.startswith("#") or s.startswith(">") or re.fullmatch(r"\*End of Day \d+\*", s):
            continue
        if s.startswith("|"):
            if not re.fullmatch(r"[|:\- ]+", s):
                tabell.append(s)
            continue
        s = re.sub(r"^[-*] ", "", s)
        s = re.sub(r"[*_]", "", s)
        prosa.append(s)
    tekst = " ".join(prosa)
    tekst = tekst.replace("’", "'").replace("‘", "'")
    setn = [x for x in re.split(r"(?<=[.!?])[\"”']?\s+", tekst) if re.search(r"[A-Za-z]", x)]
    ord_ = re.findall(r"[A-Za-z][A-Za-z']*", tekst)
    syl = [stavelser(w) for w in ord_]
    W, S = len(ord_), max(1, len(setn))
    Y = sum(syl)
    abs_hits = collections.Counter(m.group(1).lower() for m in ABS_RE.finditer(tekst + " " + " ".join(tabell)))
    return {
        "ord": W, "setninger": len(setn),
        "snitt_setning": round(W / S, 1),
        "flesch": round(206.835 - 1.015 * (W / S) - 84.6 * (Y / max(1, W)), 1),
        "fk_grade": round(0.39 * (W / S) + 11.8 * (Y / max(1, W)) - 15.59, 1),
        "lange_ord_pst": round(100 * sum(1 for s in syl if s >= 3) / max(1, W), 1),
        "abstrakte": sum(abs_hits.values()),
        "abstrakte_per_1000": round(1000 * sum(abs_hits.values()) / max(1, W), 1),
        "abstrakte_ord": dict(abs_hits.most_common()),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("fil"); ap.add_argument("--per-dag", action="store_true")
    ap.add_argument("--json"); ap.add_argument("--ord", action="store_true")
    a = ap.parse_args()
    t = open(a.fil, encoding="utf-8").read()
    # Forordet måles ikke: det er gjestetekst og redigeres ikke.
    t = re.sub(r"(?ms)^# Foreword\n.*?(?=^# )", "", t)
    total = mal(t.splitlines())
    res = {"totalt": total, "seksjoner": {}}
    for n, b in seksjoner(t):
        res["seksjoner"][n] = mal(b)
    print(f"Ord {total['ord']}  setninger {total['setninger']}  snitt {total['snitt_setning']}  "
          f"Flesch {total['flesch']}  FK-grade {total['fk_grade']}  lange ord {total['lange_ord_pst']} %  "
          f"abstrakte {total['abstrakte']} ({total['abstrakte_per_1000']} per 1000)")
    if a.ord:
        print("  " + ", ".join(f"{k} {v}" for k, v in total["abstrakte_ord"].items()))
    if a.per_dag:
        for n, m in res["seksjoner"].items():
            print(f"  {n[:44]:44} snitt {m['snitt_setning']:5}  FK {m['fk_grade']:5}  abstr {m['abstrakte']:3}")
    if a.json:
        json.dump(res, open(a.json, "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
