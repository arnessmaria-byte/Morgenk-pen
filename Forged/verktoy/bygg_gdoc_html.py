#!/usr/bin/env python3
"""Lager kompakt HTML for import til Google Docs (EB Garamond, bokens overskriftsstil).

Bruk: python3 bygg_gdoc_html.py manus/FORGED_manus.md ut.html
"""
import re, sys, subprocess, pathlib, tempfile, html
here = pathlib.Path(__file__).parent
md, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
lines, res, i = md.read_text(encoding="utf-8").split("\n"), [], 0
while i < len(lines):
    l = lines[i]
    if l.startswith("## ") and not l.startswith("## Day "):
        res.append("#" + l)
    elif re.fullmatch(r"\*End of Day \d+\*", l.strip()):
        res.append('<p class="end">End of Day ' + re.search(r"\d+", l).group(0) + "</p>")
    elif l.startswith("# Phase ") and i + 2 < len(lines) and re.fullmatch(r"\*[^*]+\*", lines[i + 2].strip()):
        res += [l, "", '<p class="sub">' + html.escape(lines[i + 2].strip().strip("*")) + "</p>"]; i += 3; continue
    elif l.startswith("|") and i + 1 < len(lines) and re.fullmatch(r"\|[ :\-|]+\|?", lines[i + 1].strip()) and (i == 0 or not lines[i - 1].startswith("|")):
        res.append("|  |  |")
    else:
        res.append(l)
    i += 1
body = "\n".join(res)
if "--med-tittel" in sys.argv:
    body = ('<p class="title">FORGED</p>\n\n<p class="sub">A 40-Day Path to Durable Faith for Young Men</p>\n\n'
            '<p class="sub">Elias Solbak Årnes</p>\n\n') + body
with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as f:
    f.write(body); tmp = f.name
r = subprocess.run(["pandoc", tmp, "-f", "markdown-smart-auto_identifiers", "-t", "html5", "--wrap=none",
                    "--template", str(here / "maler" / "gdoc.html"), "-M", "title=FORGED"], capture_output=True, text=True, check=True)
h = r.stdout
h = re.sub(r"<table>\s*<colgroup>.*?</colgroup>", "<table>", h, flags=re.S)
h = re.sub(r"<thead>\s*<tr[^>]*>\s*(<th[^>]*>\s*</th>\s*)+</tr>\s*</thead>", "", h, flags=re.S)
h = re.sub(r' class="(odd|even|header)"', "", h)
h = re.sub(r' style="text-align: left;"', "", h)
h = re.sub(r"\n\s*\n", "\n", h)
out.write_text(h, encoding="utf-8")
print("skrev", out, len(h.encode()), "byte")
