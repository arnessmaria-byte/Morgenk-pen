#!/usr/bin/env python3
"""Lager et formatert Word-manus (EB Garamond, 6 x 9) fra FORGED_manus.md.

Bruk: python3 bygg_docx.py manus/FORGED_manus.md ut/FORGED_manus.docx
Dager og hovedkapitler starter på ny side. Epigrafer settes sentrert i kursiv.
"""
import re, sys, subprocess, pathlib, tempfile
here = pathlib.Path(__file__).parent
md, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
t = md.read_text(encoding="utf-8")
lines, res = t.split("\n"), []
i = 0
while i < len(lines):
    l = lines[i]
    if l.startswith("## ") and not l.startswith("## Day "):
        res.append("#" + l)                        # underseksjoner i intro og avslutning
    elif re.fullmatch(r"\*End of Day \d+\*", l.strip()):
        n = re.search(r"\d+", l).group(0)
        res += ["::: {custom-style=\"End Mark\"}", f"End of Day {n}", ":::"]
    elif l.startswith("# Phase ") and i + 2 < len(lines) and re.fullmatch(r"\*[^*]+\*", lines[i + 2].strip()):
        res += [l, "", "::: {custom-style=\"Phase Subtitle\"}", lines[i + 2].strip().strip("*"), ":::"]
        i += 3; continue
    elif l.startswith("|") and i + 1 < len(lines) and re.fullmatch(r"\|[ :\-|]+\|?", lines[i + 1].strip()) and (i == 0 or not lines[i - 1].startswith("|")):
        res.append("|  |  |")                      # tabell uten overskriftsrad, som i trykket
    else:
        res.append(l)
    i += 1
meta = ("---\ntitle: \"FORGED\"\nsubtitle: \"A 40-Day Path to Durable Faith for Young Men\"\n"
        "author: \"Elias Solbak Årnes\"\nlang: en-US\n---\n\n")
with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as f:
    f.write(meta + "\n".join(res)); tmp = f.name
subprocess.run(["pandoc", tmp, "-f", "markdown-smart", "-o", str(out),
                "--reference-doc", str(here / "maler" / "reference.docx")], check=True)

# Sideskift direkte på avsnittet (ikke bare i stilen), så Google Docs og andre
# programmer som ignorerer stilarv også starter hver dag og hvert kapittel på ny side.
import zipfile, shutil
tmpzip = out.with_suffix(".tmp.docx")
with zipfile.ZipFile(out) as zin, zipfile.ZipFile(tmpzip, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zout:
    for item in zin.infolist():
        data = zin.read(item.filename)
        if item.filename == "word/document.xml":
            x = data.decode("utf-8")
            n_before = x.count("<w:pageBreakBefore")
            x = re.sub(r'<w:pPr><w:pStyle w:val="(Heading1|Heading2)" />',
                       r'<w:pPr><w:pStyle w:val="\1" /><w:pageBreakBefore />', x)
            data = x.encode("utf-8")
        zout.writestr(item, data)
shutil.move(tmpzip, out)
print("skrev", out)
