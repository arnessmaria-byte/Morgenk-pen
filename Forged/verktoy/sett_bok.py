#!/usr/bin/env python3
"""sett_bok.py: setter FORGED_manus.md til KDP-innmat (PDF) med Typst.

Typografi etter forfatterens tidligere bøker (The Supervised Hours v9.4.1 og
The Foundation of Knowing v1.5.1): EB Garamond, 11,5 pt, sperrede versaler i
titler, sentrert topptekst (verso forfatter, recto tittel), sentrert folio,
CONTENTS med punktlinjer, Part-sider for fasene.

Bruk: python3 sett_bok.py MANUS.md UT.pdf [--trim 6x9|5x8] [--typ UT.typ]
"""
import re, sys, argparse, pathlib, json
_dumps = json.dumps
json.dumps = lambda o, **k: _dumps(o, ensure_ascii=False, **k)

FONTS = str(pathlib.Path(__file__).resolve().parent.parent / "bok" / "fonts")

TRIMS = {
    # bredde, høyde, inner, ytre, topp, bunn (tommer); kroppstekst, linjeavstand (pt)
    "6x9": dict(w=6.0, h=9.0, inner=0.80, outer=0.72, top=0.80, bottom=0.82, size=11.5, lead=15.1),
    "5x8": dict(w=5.0, h=8.0, inner=0.72, outer=0.55, top=0.72, bottom=0.75, size=10.8, lead=14.2),
}

# ---------- inline-konvertering fra markdown til typst-markup ----------

def esc(s):
    out = []
    for ch in s:
        if ch in '\\#$@<>*_`[]~=+"':
            out.append("\\" + ch)
        else:
            out.append(ch)
    s = "".join(out)
    s = s.replace("//", "/\\/").replace("--", "-\\-")
    return s

def inline(s):
    """*kursiv* og **fet** til typst; alt annet escapes."""
    parts = re.split(r"(\*\*[^*]+\*\*|\*[^*]+\*)", s)
    res = []
    for p in parts:
        if p.startswith("**") and p.endswith("**") and len(p) > 4:
            res.append("#strong[" + esc(p[2:-2]) + "]")
        elif p.startswith("*") and p.endswith("*") and len(p) > 2:
            res.append("#emph[" + esc(p[1:-1]) + "]")
        else:
            res.append(esc(p))
    t = "".join(res)
    # linjestart som typst ville lest som liste/overskrift/tall-liste
    t = re.sub(r"^(\d+)\.", r"\1\\.", t)
    if t[:1] in "-/":
        t = "\\" + t
    return t

# ---------- parsing av manus ----------

def blocks(lines):
    """Grupperer linjer i blokker: avsnitt, liste, tabell, sitat, overskrift."""
    i, out = 0, []
    while i < len(lines):
        l = lines[i]
        if not l.strip():
            i += 1; continue
        if l.startswith("#"):
            lvl = len(l) - len(l.lstrip("#"))
            out.append(("h", lvl, l[lvl:].strip())); i += 1; continue
        if l.startswith(">"):
            q = []
            while i < len(lines) and lines[i].startswith(">"):
                q.append(lines[i][1:].strip()); i += 1
            q = [x for x in q if x]
            out.append(("quote", q)); continue
        if l.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-+:?", c) for c in cells):
                    rows.append(cells)
                i += 1
            out.append(("table", rows)); continue
        if l.startswith("- "):
            items = []
            while i < len(lines) and lines[i].startswith("- "):
                items.append(lines[i][2:].strip()); i += 1
            out.append(("list", items)); continue
        para = [l.strip()]; i += 1
        while i < len(lines) and lines[i].strip() and not lines[i].startswith(("#", ">", "|", "- ")):
            para.append(lines[i].strip()); i += 1
        out.append(("p", " ".join(para)))
    return out

def parse(md):
    """Deler manus i kapitler: frontnote, foreword, intro, phase, day, back."""
    chapters, cur = [], None
    for b in blocks(md.split("\n")):
        if b[0] == "h" and b[1] == 1:
            title = b[2]
            if title.startswith("Phase"):
                cur = {"kind": "phase", "title": title, "blocks": []}
            else:
                cur = {"kind": "chapter", "title": title, "blocks": []}
            chapters.append(cur); continue
        if b[0] == "h" and b[1] == 2 and re.match(r"Day \d+:", b[2]):
            cur = {"kind": "day", "title": b[2], "blocks": []}
            chapters.append(cur); continue
        cur["blocks"].append(b)
    return chapters

# ---------- typst-generering ----------

PREAMBLE = r'''
#let T = (TRIM)
#let BLANKS = (BLANKLIST)
#let book-title = "FORGED"
#let book-author = "ELIAS SOLBAK ÅRNES"

#set document(title: "Forged: A 40-Day Path to Durable Faith for Young Men", author: "Elias Solbak Årnes", keywords: ("devotional", "young men", "faith"))
#set text(font: "EB Garamond", size: T.size * 1pt, lang: "en", region: "US", hyphenate: true, number-type: "old-style", kerning: true, ligatures: true)
#set par(justify: true, leading: T.lead * 1pt - 0.65em, spacing: T.lead * 1pt - 0.65em, first-line-indent: (amount: 1.5em, all: false))
#show heading: it => it.body

// sidetilstand
#let chapter-start = state("chapter-start", false)
#let in-front = state("in-front", true)
#let no-head = state("no-head", false)

#let tracked(s, size: 8.5pt, tr: 0.18em) = text(size: size, tracking: tr, upper(s))

#set page(
  width: T.w * 1in, height: T.h * 1in,
  margin: (inside: T.inner * 1in, outside: T.outer * 1in, top: T.top * 1in, bottom: T.bottom * 1in),
  header-ascent: 38%, footer-descent: 34%,
  header: context {
    let p = here().page()
    let starts = query(<chapter-start>).map(m => m.location().page())
    if p in starts or p in BLANKS or no-head.get() { return }
    if in-front.get() { return }
    align(center, if calc.even(p) { tracked(book-author) } else { tracked(book-title) })
  },
  footer: context {
    if no-head.get() and not in-front.get() { return }
    let p = here().page()
    if p in BLANKS { return }
    let n = counter(page).display(if in-front.get() { "i" } else { "1" })
    if in-front.get() and query(<no-folio>).map(m => m.location().page()).contains(p) { return }
    align(center, text(size: 8.5pt, number-type: "lining", n))
  },
)

#let blank-recto() = {
  pagebreak(to: "odd", weak: true)
}

// tom side markeres slik at den får verken topptekst eller folio
#let to-recto() = pagebreak(to: "odd", weak: true)

#let chapter-title(label, title) = {
  [#metadata(none)<chapter-start>]
  v(0.55in)
  if label != none { align(center, tracked(label, size: 10.5pt, tr: 0.22em)); v(10pt) }
  align(center, text(size: 15pt, tracking: 0.04em, title))
  v(0.42in)
}

#let simple-title(title) = {
  [#metadata(none)<chapter-start>]
  v(0.55in)
  align(center, tracked(title, size: 12pt, tr: 0.2em))
  v(0.38in)
}

#let epigraph(quote, ref) = {
  align(center, block(width: 82%, {
    set par(justify: false, first-line-indent: 0pt)
    text(style: "italic", size: 10.5pt, quote)
    v(4pt)
    text(size: 8.5pt, tracking: 0.08em, smallcaps(ref))
  }))
  v(0.3in)
}

#let section(title) = {
  v(1.1em, weak: true)
  block(width: 100%, sticky: true, above: 1.4em, below: 0.85em, align(center, tracked(title, size: 8.6pt, tr: 0.2em)))
}

#let subsection(title) = {
  block(sticky: true, above: 1.3em, below: 0.7em, align(left, text(style: "italic", size: 11pt, title)))
}

#let healing(title, body, end: none) = {
  v(0.9em)
  block(breakable: false, width: 100%, block(width: 100%, inset: (x: 0.18in, top: 10pt, bottom: 10pt), stroke: (top: 0.4pt + luma(90), bottom: 0.4pt + luma(90)), {
    align(center, tracked("Healing Forge", size: 8.2pt, tr: 0.22em))
    v(2pt)
    align(center, text(style: "italic", size: 10.5pt, title))
    v(6pt)
    set text(size: 10.3pt)
    set par(first-line-indent: (amount: 1.2em, all: false))
    body
  }) + if end != none { v(1.2em); align(center, text(size: 7.6pt, tracking: 0.25em, upper(end))) })
}

#let endmark(s) = {
  v(1.2em)
  align(center, text(size: 7.6pt, tracking: 0.25em, upper(s)))
}

#let contrast(head, rows) = {
  v(0.5em)
  align(center, block(width: 96%, breakable: false, table(
    columns: (1fr, 1fr),
    stroke: none,
    inset: (x: 6pt, y: 4.2pt),
    align: left,
    table.hline(stroke: 0.6pt),
    ..rows.flatten().map(c => text(size: 10pt, c)),
    table.hline(stroke: 0.6pt),
  )))
  v(0.5em)
}

#let blist(items) = {
  v(0.25em)
  pad(left: 1.2em, {
    set par(first-line-indent: 0pt, justify: false)
    for it in items {
      grid(columns: (0.9em, 1fr), gutter: 0pt, text(size: 0.8em, baseline: -0.05em, "•"), it)
      v(0.28em)
    }
  })
  v(0.15em)
}

#let phase-page(num, name, sub, tocmark) = {
  to-recto()
  tocmark
  [#metadata(none)<chapter-start>]
  v(1.9in)
  align(center, tracked(num, size: 10.5pt, tr: 0.25em))
  v(14pt)
  align(center, text(size: 26pt, tracking: 0.12em, upper(name)))
  v(12pt)
  align(center, text(style: "italic", size: 11.5pt, sub))
  pagebreak(to: "odd")
}
'''

def render_blocks(bl, in_day=False):
    out = []
    i = 0
    after_head = True
    while i < len(bl):
        b = bl[i]
        k = b[0]
        if k == "h":
            title = b[2]
            if title.startswith("Healing Forge:"):
                # samle resten av dagen fram til sluttmerket
                body, j = [], i + 1
                while j < len(bl) and not (bl[j][0] == "p" and re.fullmatch(r"\*End of Day \d+\*", bl[j][1])):
                    body.append(bl[j]); j += 1
                sub = title.split(":", 1)[1].strip()
                endtxt = "none"
                if j < len(bl):
                    m2 = re.fullmatch(r"\*End of Day (\d+)\*", bl[j][1]); endtxt = json.dumps(f"End of Day {m2.group(1)}"); j += 1
                out.append("#healing(end: " + endtxt + ")[" + esc(sub) + "][\n" + render_blocks(body) + "\n]")
                i = j; continue
            if b[1] == 3 or (b[1] == 2 and in_day):
                out.append(f"#section[{esc(title)}]")
            else:
                out.append(f"#section[{esc(title)}]")
            after_head = True; i += 1; continue
        if k == "p":
            t = b[1]
            m = re.fullmatch(r"\*End of Day (\d+)\*", t)
            if m:
                out.append(f'#endmark("End of Day {m.group(1)}")'); i += 1; continue
            if re.fullmatch(r"\*[^*]+\*", t) and len(t) < 80 and not in_day and t.startswith("*Sverre"):
                out.append("#v(0.8em)\n#align(right, text(style: \"italic\", " + json.dumps(t.strip('*')) + "))")
                i += 1; continue
            if t.startswith("MantleOfElias:"):
                out.append("#v(0.6em)\n#par(first-line-indent: 0pt, text(size: 9.5pt, " + json.dumps(t) + "))")
                i += 1; continue
            body = inline(t)
            if after_head:
                out.append("#par(first-line-indent: 0pt)[" + body + "]")
            else:
                out.append(body)
            out.append("")
            after_head = False; i += 1; continue
        if k == "list":
            items = ", ".join("[" + inline(x) + "]" for x in b[1])
            out.append(f"#blist(({items},))")
            after_head = True; i += 1; continue
        if k == "table":
            head = b[1][0]; rows = b[1][1:]
            h = ", ".join("[" + inline(c) + "]" for c in head)
            r = ", ".join("(" + ", ".join("[" + inline(c) + "]" for c in row) + ",)" for row in rows)
            out.append(f"#contrast(({h},), ({r},))")
            after_head = True; i += 1; continue
        if k == "quote":
            out.append("#epigraph[" + inline(b[1][0]) + "][" + esc(b[1][-1]) + "]")
            after_head = True; i += 1; continue
        i += 1
    return "\n".join(out)

ALSO_BY = '''
#to-recto()
#[#metadata((kind: "chapter", text: "Also by Elias Solbak Årnes", front: false))<toc>]
#simple-title("Also by Elias Solbak Årnes")
#align(center, text(style: "italic", "The Foundation of Knowing: A Philosophical Inquiry"))
#v(6pt)
#align(center, text(style: "italic", "The Supervised Hours: A Novel"))
'''

ROMAN = ["I", "II", "III", "IV", "V"]

def build(md, trim, blanks=()):
    ch = parse(md)
    T = TRIMS[trim]
    s = [PREAMBLE.replace("(TRIM)", "(" + ", ".join(f"{k}: {v}" for k, v in T.items()) + ")").replace("(BLANKLIST)", "(" + "".join(f"{b}, " for b in blanks) + ")")]

    # ---- forsats ----
    s.append('#counter(page).update(1)')
    s.append('''
#[#metadata(none)<no-folio>]
#v(1.55in)
#align(center, text(size: 30pt, tracking: 0.32em, "FORGED"))
#v(10pt)
#align(center, text(style: "italic", size: 12pt, "A 40-Day Path to Durable Faith for Young Men"))
#v(0.62in)
#align(center, tracked("Elias Solbak Årnes", size: 12pt, tr: 0.22em))
#pagebreak()
#[#metadata(none)<no-folio>]
#set par(justify: false, first-line-indent: 0pt, spacing: 0.75em)
#set text(size: 8.6pt, number-type: "lining")
#v(0.25in)
#align(center, tracked("Forged", size: 9pt, tr: 0.2em))
#v(10pt)
Copyright © 2026 Elias Solbak Årnes. All rights reserved.

First edition, 2026 · Independently published

No part of this publication may be reproduced, stored in a retrieval system, or transmitted in any form or by any means without prior written permission, except for brief quotations used in reviews, scholarship, or other uses permitted by law.

Foreword © 2026 Sverre Johannes Langeland. Used by permission.

Scripture quotations are from the ESV® Bible (The Holy Bible, English Standard Version®), © 2001 by Crossway, a publishing ministry of Good News Publishers. ESV Text Edition: 2025. The ESV text may not be quoted in any publication made available to the public by a Creative Commons license. The ESV may not be translated in whole or in part into any other language. Used by permission. All rights reserved.

The scenarios in this book are drawn from lived experience; names and identifying details have been changed.

This is a work of spiritual formation. It is not medical, psychological, or legal advice.

Set in EB Garamond 11.5 pt. 6 x 9 inches.
#set text(size: T.size * 1pt, number-type: "old-style")
#set par(justify: true, first-line-indent: (amount: 1.5em, all: false), spacing: T.lead * 1pt - 0.65em)
#pagebreak()
'''.replace("6 x 9 inches", "6 x 9 inches" if trim == "6x9" else "5 x 8 inches").replace("11.5 pt", f"{T['size']} pt"))

    front = [c for c in ch if c["kind"] == "chapter" and c["title"] in ("To the One Giving This Book",)]
    for c in front:
        s.append("#simple-title(" + json.dumps(c["title"]) + ")")
        s.append(render_blocks(c["blocks"]))
        s.append("#to-recto()")

    # ---- innhold ----
    s.append('''
#simple-title("Contents")
#context {
  set par(justify: false, first-line-indent: 0pt, spacing: 0pt, leading: 0.42em)
  set text(size: 9.8pt, number-type: "lining")
  let entries = query(<toc>)
  for e in entries {
    let ent = e.value
    let pg = counter(page).at(e.location()).first()
    let num = if ent.at("front", default: false) { numbering("i", pg) } else { str(pg) }
    if ent.kind == "phase" {
      v(7pt)
      grid(columns: (1fr, auto), align: (left, right), text(tracking: 0.14em, size: 8.8pt, upper(ent.text)), text(size: 9pt, num))
      v(3pt)
    } else {
      let ind = if ent.kind == "day" { 1.1em } else { 0em }
      pad(left: ind, grid(columns: (auto, 1fr, auto), column-gutter: 4pt, align: (left, bottom, right),
        ent.text, box(width: 1fr, repeat(text(fill: luma(110), size: 7pt, " . "))), num))
      v(5.2pt)
    }
  }
}
''')
    s.append("#to-recto()")

    def toc(kind, text, front=False):
        return f'#[#metadata((kind: "{kind}", text: {json.dumps(text)}, front: {"true" if front else "false"}))<toc>]'

    started_body = False
    phase_i = 0
    for c in ch:
        if c in front:
            continue
        t = c["title"]
        if c["kind"] == "chapter" and t == "Foreword":
            s.append(toc("front", "Foreword", True))
            s.append("#simple-title(\"Foreword\")")
            s.append(render_blocks(c["blocks"]))
            s.append("#to-recto()")
            continue
        if not started_body:
            s.append('#in-front.update(false)\n#counter(page).update(1)')
            started_body = True
        if c["kind"] == "phase":
            num, name = t.split(":", 1)
            sub = c["blocks"][0][1].strip("*") if c["blocks"] and c["blocks"][0][0] == "p" else ""
            mark = toc("phase", t.replace(":", " ·", 1))[1:]
            s.append(f'#phase-page({json.dumps(num.strip())}, {json.dumps(name.strip())}, {json.dumps(sub)}, {mark})')
            continue
        if c["kind"] == "day":
            n, title = re.match(r"Day (\d+): (.+)", t).groups()
            s.append("#pagebreak(weak: true)")
            s.append(toc("day", f"Day {n} · {title}"))
            s.append(f'#chapter-title("Day {n}", {json.dumps(title)})')
            s.append(render_blocks(c["blocks"], in_day=True))
            continue
        if t == "About the Author":
            s.append(ALSO_BY)
        # øvrige kapitler (Introduction, Conclusion, Appendix, About)
        if t.startswith("Introduction"):
            s.append("#pagebreak(weak: true)")
        else:
            s.append("#to-recto()")
        label, title = None, t
        if t.startswith("Appendix"):
            label, title = t.split(":", 1)
            title = title.strip()
        elif t.startswith("Conclusion"):
            label, title = "Conclusion", t.split(":", 1)[1].strip()
        s.append(toc("chapter", t.replace(": ", " · ", 1) if t.startswith(("Appendix", "Conclusion")) else t))
        if label:
            s.append(f'#chapter-title({json.dumps(label)}, {json.dumps(title)})')
        else:
            s.append(f'#simple-title({json.dumps(title)})')
        bl = c["blocks"]
        if t.startswith("Appendix") and bl and bl[0][0] == "p" and re.fullmatch(r"\*[^*]+\*", bl[0][1]):
            s.append('#align(center, text(style: "italic", size: 10.5pt, ' + json.dumps(bl[0][1].strip("*")) + '))\n#v(0.25in)')
            bl = bl[1:]
        s.append(render_blocks(bl))

    return "\n".join(s)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("md"); ap.add_argument("pdf")
    ap.add_argument("--trim", default="6x9", choices=list(TRIMS))
    ap.add_argument("--typ")
    a = ap.parse_args()
    md = pathlib.Path(a.md).read_text(encoding="utf-8")
    import typst, subprocess
    typ = pathlib.Path(a.typ or (pathlib.Path(a.pdf).with_suffix(".typ")))
    blanks = ()
    for runde in (1, 2):
        typ.write_text(build(md, a.trim, blanks), encoding="utf-8")
        pdf = typst.compile(str(typ), font_paths=[FONTS], ignore_system_fonts=True)
        pathlib.Path(a.pdf).write_bytes(pdf)
        if runde == 1:
            txt = subprocess.run(["pdftotext", "-layout", a.pdf, "-"], capture_output=True, text=True).stdout.split("\f")
            found = []
            for i, pg in enumerate(txt[:-1], start=1):
                body = [l.strip() for l in pg.splitlines() if l.strip()]
                body = [l for l in body if l not in ("F O R G E D", "E L I A S S O L B A K Å R N E S", "FORGED", "ELIAS SOLBAK ÅRNES") and not re.fullmatch(r"[ivxlc]+|\d+", l)]
                if not body:
                    found.append(i)
            blanks = tuple(found)
    # Partall sider: legg til en helt tom venstreside til slutt ved behov.
    import pymupdf
    doc = pymupdf.open(a.pdf)
    if len(doc) % 2:
        r = doc[-1].rect
        doc.new_page(width=r.width, height=r.height)
        blanks = tuple(blanks) + (len(doc),)
        tmp = pathlib.Path(a.pdf).with_suffix(".tmp.pdf")
        doc.save(str(tmp), garbage=3, deflate=True); doc.close(); tmp.replace(a.pdf)
    else:
        doc.close()
    print("skrev", a.pdf, "tomme sider:", list(blanks))

if __name__ == "__main__":
    main()
