#!/usr/bin/env python3
"""bygg_epub.py: lager Kindle-klar EPUB 3 av FORGED_manus.md med pandoc."""
import re, sys, subprocess, pathlib
md_path, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
fonts = pathlib.Path(__file__).resolve().parent.parent / "bok" / "fonts"
md = md_path.read_text(encoding="utf-8")
lines, out_lines, top = md.split("\n"), [], ""
for l in lines:
    if l.startswith("# "):
        top = l[2:]
    if l.startswith("## ") and not re.match(r"## Day \d+:", l):
        l = "#" + l                      # underseksjoner i intro/konklusjon/tillegg ut av innholdslisten
    out_lines.append(l)
body = "\n".join(out_lines)
body = re.sub(r"(?m)^\*End of Day (\d+)\*$", r'::: endmark\nEnd of Day \1\n:::', body)
body = re.sub(r"(?m)^> (?!“)(.+)$", r"> []{.ref}\1", body)   # henvisningslinja i epigrafen
front = """---
title: "Forged"
subtitle: "A 40-Day Path to Durable Faith for Young Men"
author: "Elias Solbak Årnes"
lang: en-US
rights: "Copyright © 2026 Elias Solbak Årnes. All rights reserved."
publisher: "Independently published"
date: "2026"
---

# Copyright {.unnumbered .copyright}

Copyright © 2026 Elias Solbak Årnes. All rights reserved.

First edition, 2026. Independently published.

No part of this publication may be reproduced, stored in a retrieval system, or transmitted in any form or by any means without prior written permission, except for brief quotations used in reviews, scholarship, or other uses permitted by law.

Foreword © 2026 Sverre Johannes Langeland. Used by permission.

Scripture quotations are from the ESV® Bible (The Holy Bible, English Standard Version®), © 2001 by Crossway, a publishing ministry of Good News Publishers. ESV Text Edition: 2025. The ESV text may not be quoted in any publication made available to the public by a Creative Commons license. The ESV may not be translated in whole or in part into any other language. Used by permission. All rights reserved.

The scenarios in this book are drawn from lived experience; names and identifying details have been changed.

This is a work of spiritual formation. It is not medical, psychological, or legal advice.

"""
also = "\n\n# Also by Elias Solbak Årnes\n\n*The Foundation of Knowing: A Philosophical Inquiry*\n\n*The Supervised Hours: A Novel*\n\n"
body = body.replace("\n# About the Author", also + "# About the Author")
css = """
@font-face { font-family: "EB Garamond"; src: url("../fonts/EBGaramond-Regular.ttf"); }
@font-face { font-family: "EB Garamond"; font-style: italic; src: url("../fonts/EBGaramond-Italic.ttf"); }
@font-face { font-family: "EB Garamond"; font-weight: bold; src: url("../fonts/EBGaramond-Bold.ttf"); }
body { font-family: "EB Garamond", serif; line-height: 1.45; }
p { margin: 0; text-indent: 1.4em; text-align: justify; }
h1 + p, h2 + p, h3 + p, blockquote + p, table + p, ul + p, .endmark + p, div + p { text-indent: 0; }
h1 { font-weight: normal; text-align: center; letter-spacing: 0.12em; text-transform: uppercase; font-size: 1.15em; margin: 3em 0 1.5em; page-break-before: always; }
h2 { font-weight: normal; text-align: center; font-size: 1.25em; margin: 2.5em 0 1.2em; page-break-before: always; }
h3 { font-weight: normal; text-align: center; letter-spacing: 0.14em; text-transform: uppercase; font-size: 0.78em; margin: 1.8em 0 0.8em; }
blockquote { margin: 1em 2em 1.6em; text-align: center; font-style: italic; }
blockquote p { text-indent: 0; text-align: center; }
.ref { font-style: normal; font-variant: small-caps; letter-spacing: 0.05em; }
table { border-collapse: collapse; width: 100%; margin: 1em 0; font-size: 0.9em; }
th { text-align: left; font-weight: normal; letter-spacing: 0.08em; text-transform: uppercase; font-size: 0.8em; border-top: 1px solid #000; border-bottom: 1px solid #555; padding: 0.3em; }
td { padding: 0.25em 0.3em; vertical-align: top; }
tr:last-child td { border-bottom: 1px solid #000; }
ul { margin: 0.5em 0 0.6em 1.2em; padding: 0; }
li { margin: 0.2em 0; }
.endmark { text-align: center; letter-spacing: 0.2em; text-transform: uppercase; font-size: 0.7em; margin: 2em 0; }
.copyright p { text-indent: 0; font-size: 0.85em; margin-bottom: 0.7em; text-align: left; }
"""
tmp = out.with_suffix(".src.md"); tmp.write_text(front + body, encoding="utf-8")
cssf = out.with_suffix(".css"); cssf.write_text(css, encoding="utf-8")
cmd = ["pandoc", str(tmp), "-f", "markdown+smart", "-t", "epub3", "-o", str(out), "--toc", "--toc-depth=2",
       "--split-level=2", "--css", str(cssf), "--metadata", "toc-title=Contents"]
for f in ("EBGaramond-Regular.ttf", "EBGaramond-Italic.ttf", "EBGaramond-Bold.ttf"):
    cmd += ["--epub-embed-font", str(fonts / f)]
subprocess.run(cmd, check=True)
tmp.unlink(); cssf.unlink()
print("skrev", out)
