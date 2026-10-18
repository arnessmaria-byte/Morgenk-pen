#!/usr/bin/env python3
"""Lager kompakt RTF for import til Google Docs.

EB Garamond, 6 x 9 tommer med bokens marger, hver dag og hvert kapittel på ny side
(Google Docs leser sideskift fra RTF, men ignorerer dem i HTML). RTF er ren tekst,
så hele boken kan lastes opp som tekst gjennom Drive-koblingen.

Bruk: python3 bygg_gdoc_rtf.py manus/FORGED_manus.md ut/FORGED_GoogleDocs.rtf
"""
import re, sys, pathlib

md, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
L = md.read_text(encoding="utf-8").split("\n")

W = 8640 - 1152 - 1037          # tekstbredde i twips
C1 = W // 2


def esc(s):
    o = []
    for c in s:
        if c in "\\{}":
            o.append("\\" + c)
        elif ord(c) < 128:
            o.append(c)
        else:
            try:
                b = c.encode("cp1252")
                o.append("\\'%02x" % b[0])
            except UnicodeEncodeError:
                n = ord(c)
                o.append("\\u%d?" % (n if n < 32768 else n - 65536))
    return "".join(o)


def inline(s):
    s = esc(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"{\\b \1}", s)
    s = re.sub(r"(?<![\\\w])\*(.+?)\*", r"{\\i \1}", s)
    return s


BODY = "\\pard\\qj\\fi340\\sa0 "
out_ = ["{\\rtf1\\ansi\\ansicpg1252\\deff0{\\fonttbl{\\f0\\froman EB Garamond;}}",
        "\\paperw8640\\paperh12960\\margl1152\\margr1037\\margt1152\\margb1181\\widowctrl\\fs23",
        "{\\pard\\qc\\sb2400\\sa240\\fs56\\expndtw60 FORGED\\par}",
        "{\\pard\\qc\\sa720\\i\\fs24 A 40-Day Path to Durable Faith for Young Men\\par}",
        "{\\pard\\qc\\fs22\\caps\\expndtw30 " + esc("Elias Solbak Årnes") + "\\par}",
        BODY]
after_heading = False
i = 0
while i < len(L):
    l = L[i].rstrip()
    if not l.strip():
        i += 1
        continue
    if l.startswith("# "):
        out_.append("{\\pard\\pagebb\\qc\\sb1440\\sa480\\keepn\\fs32\\caps\\expndtw60 " + inline(l[2:]) + "\\par}")
        after_heading = True
    elif l.startswith("## Day "):
        m = re.match(r"## (Day \d+): (.*)", l)
        out_.append("{\\pard\\pagebb\\qc\\sb1080\\sa120\\keepn\\fs20\\caps\\expndtw50 " + m.group(1) + "\\par}")
        out_.append("{\\pard\\qc\\sa480\\keepn\\fs30 " + inline(m.group(2)) + "\\par}")
        after_heading = True
    elif l.startswith("## ") or l.startswith("### "):
        out_.append("{\\pard\\qc\\sb300\\sa100\\keepn\\fs18\\caps\\expndtw40 " + inline(l.split(" ", 1)[1]) + "\\par}")
        after_heading = True
    elif l.startswith(">"):
        block = []
        while i < len(L) and L[i].startswith(">"):
            block.append(L[i][1:].strip()); i += 1
        parts = [b for b in block if b]
        out_.append("{\\pard\\qc\\li720\\ri720\\sb120\\sa60\\i\\fs21 " + inline(parts[0]) + "\\par}")
        for p in parts[1:]:
            out_.append("{\\pard\\qc\\sa360\\fs17\\scaps\\expndtw20 " + inline(p) + "\\par}")
        after_heading = True
        continue
    elif re.fullmatch(r"\*End of Day \d+\*", l.strip()):
        out_.append("{\\pard\\qc\\sb360\\fs16\\caps\\expndtw40 End of Day " + re.search(r"\d+", l).group(0) + "\\par}")
        after_heading = False
    elif l.startswith("|"):
        rows = []
        while i < len(L) and L[i].startswith("|"):
            if not re.fullmatch(r"\|[ :\-|]+\|?", L[i].strip()):
                rows.append([c.strip() for c in L[i].strip().strip("|").split("|")])
            i += 1
        rows = rows[1:]                      # første rad er kolonneoverskrift; trykket viser den ikke
        for k, r in enumerate(rows):
            b = ""
            if k == 0:
                b += "\\clbrdrt\\brdrs\\brdrw10"
            if k == len(rows) - 1:
                b += "\\clbrdrb\\brdrs\\brdrw10"
            out_.append("{\\trowd\\trgaph100\\trkeep" + b + "\\cellx%d" % C1 + b + "\\cellx%d" % W
                        + "\\pard\\intbl\\ql\\fs20 " + inline(r[0]) + "\\cell\\pard\\intbl\\ql\\fs20 " + inline(r[1]) + "\\cell\\row}")
        out_.append("{\\pard\\sa120\\fs8\\par}")
        after_heading = True
        continue
    elif l.startswith("- "):
        out_.append("{\\pard\\ql\\li520\\fi-240\\sa40 \\'95\\tab " + inline(l[2:]) + "\\par}")
        after_heading = True
    elif re.fullmatch(r"\*[^*].*[^*]\*", l.strip()) and len(l) < 80:
        # Hel kursiv kort linje: undertittel etter overskrift, ellers signatur
        if after_heading:
            out_.append("{\\pard\\qc\\sa360\\i\\fs22 " + inline(l.strip()[1:-1]) + "\\par}")
        else:
            out_.append("{\\pard\\qr\\sb120\\i " + inline(l.strip()[1:-1]) + "\\par}")
    else:
        if after_heading:
            out_.append("{\\pard\\qj\\sa0 " + inline(l) + "\\par}")
        else:
            out_.append(inline(l) + "\\par")
        after_heading = False
    i += 1
out_.append("}")
t = "\n".join(out_)
out.write_text(t, encoding="ascii")
print("skrev", out, len(t), "tegn,", t.count("\\pagebb"), "sideskift")
