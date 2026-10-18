#!/usr/bin/env python3
"""Setter sammen delfilene til FORGED_manus.md og gjør anførselstegn typografiske."""
import re, sys, pathlib
d = pathlib.Path(sys.argv[1])
parts = ["01-front-intro-phase1.md", "02-phase2-phase3.md", "03-phase4-phase5.md", "04-back.md"]
text = "\n\n".join((d / p).read_text(encoding="utf-8").strip() for p in parts) + "\n"
def smart(line):
    if line.startswith("|") or "http" in line:
        line2 = line
    else:
        line2 = line
    out, prev = [], " "
    i = 0
    while i < len(line2):
        c = line2[i]
        if c == '"':
            out.append("“" if prev in " \t([{>\u2014\u2013\n*_" or i == 0 else "”")
        elif c == "'":
            out.append("‘" if (prev in " \t([{“\n*_" or i == 0) and not re.match(r"'(?:\d|tis|em\b)", line2[i:]) else "’")
        else:
            out.append(c)
        prev = c; i += 1
    return "".join(out)
lines = [l if "http" in l else smart(l) for l in text.split("\n")]
text = "\n".join(lines)
(d / "FORGED_manus.md").write_text(text, encoding="utf-8")
print("skrevet", len(text.split()), "ord")
