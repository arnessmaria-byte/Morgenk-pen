"""Lager reference.docx (EB Garamond, 6 x 9, bokens marger) for pandoc-eksport av manus."""
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import subprocess, pathlib
here = pathlib.Path(__file__).parent
subprocess.run(["pandoc", "-o", str(here / "ref_default.docx"), "--print-default-data-file", "reference.docx"], check=True)
d = Document(here / "ref_default.docx")
FONT = "EB Garamond"
ST = {s.name.lower(): s for s in d.styles}
def S(n): return ST[n.lower()]
def setfont(st, size=None, italic=None, bold=None, caps=None, spacing=None):
    f = st.font; f.name = FONT
    rpr = st.element.get_or_add_rPr(); rf = rpr.find(qn('w:rFonts'))
    if rf is None: rf = OxmlElement('w:rFonts'); rpr.insert(0, rf)
    for a in ('w:ascii', 'w:hAnsi', 'w:cs', 'w:eastAsia'): rf.set(qn(a), FONT)
    for a in ('w:asciiTheme', 'w:hAnsiTheme', 'w:cstheme', 'w:eastAsiaTheme'):
        if rf.get(qn(a)) is not None: del rf.attrib[qn(a)]
    if size: f.size = Pt(size)
    if italic is not None: f.italic = italic
    if bold is not None: f.bold = bold
    if caps is not None: f.all_caps = caps
    f.color.rgb = RGBColor(0, 0, 0)
    if spacing is not None:
        sp = rpr.find(qn('w:spacing'))
        if sp is None: sp = OxmlElement('w:spacing'); rpr.append(sp)
        sp.set(qn('w:val'), str(spacing))
def para(st, align=None, before=0, after=0, indent=None, line=15.1, keep=False):
    pf = st.paragraph_format
    if align is not None: pf.alignment = align
    pf.space_before = Pt(before); pf.space_after = Pt(after)
    pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY; pf.line_spacing = Pt(line)
    if indent is not None: pf.first_line_indent = indent
    if keep: pf.keep_with_next = True
for n in ["Normal", "Body Text", "First Paragraph", "Compact", "Block Text", "Title", "Subtitle", "Author",
          "Heading 1", "Heading 2", "Heading 3", "Heading 4", "Table Caption", "Caption"]:
    setfont(S(n))
# Overskrifter: ingen farge, ingen fet (pandoc-malen har blå farge og fet)
setfont(S("Normal"), 11.5); para(S("Normal"))
setfont(S("Body Text"), 11.5); para(S("Body Text"), WD_ALIGN_PARAGRAPH.JUSTIFY, indent=Pt(17))
setfont(S("First Paragraph"), 11.5); para(S("First Paragraph"), WD_ALIGN_PARAGRAPH.JUSTIFY, indent=Pt(0))
setfont(S("Compact"), 11.5); para(S("Compact"), after=2)
setfont(S("Block Text"), 10.5, italic=True); para(S("Block Text"), WD_ALIGN_PARAGRAPH.CENTER, before=6, after=6, line=13.5)
S("Block Text").paragraph_format.left_indent = Inches(0.5); S("Block Text").paragraph_format.right_indent = Inches(0.5)
setfont(S("Heading 1"), 16, bold=False, italic=False, caps=True, spacing=60); para(S("Heading 1"), WD_ALIGN_PARAGRAPH.CENTER, before=72, after=24, line=20, keep=True)
S("Heading 1").paragraph_format.page_break_before = True
S("Heading 2").paragraph_format.page_break_before = True
setfont(S("Heading 2"), 15, bold=False, italic=False, spacing=10); para(S("Heading 2"), WD_ALIGN_PARAGRAPH.CENTER, before=60, after=18, line=19, keep=True)
setfont(S("Heading 3"), 9.5, bold=False, italic=False, caps=True, spacing=40); para(S("Heading 3"), WD_ALIGN_PARAGRAPH.CENTER, before=12, after=4, line=13, keep=True)
setfont(S("Title"), 28, bold=False, caps=True, spacing=120); para(S("Title"), WD_ALIGN_PARAGRAPH.CENTER, before=144, after=12, line=34)
setfont(S("Subtitle"), 12, italic=True); para(S("Subtitle"), WD_ALIGN_PARAGRAPH.CENTER, after=36, line=16)
setfont(S("Author"), 11, caps=True, spacing=60); para(S("Author"), WD_ALIGN_PARAGRAPH.CENTER, after=12, line=15)
for sec in d.sections:
    sec.page_width = Inches(6); sec.page_height = Inches(9)
    sec.left_margin = Inches(0.80); sec.right_margin = Inches(0.72)
    sec.top_margin = Inches(0.80); sec.bottom_margin = Inches(0.82)
from docx.enum.style import WD_STYLE_TYPE
for name, size, italic, caps, before in (("End Mark", 8.5, False, True, 10), ("Phase Subtitle", 12, True, False, 6), ("Centered", 11.5, False, False, 0)):
    st = d.styles.add_style(name, WD_STYLE_TYPE.PARAGRAPH); st.base_style = S("Normal")
    st.font.size = Pt(size); st.font.italic = italic; st.font.all_caps = caps; st.font.name = FONT
    pf = st.paragraph_format; pf.alignment = WD_ALIGN_PARAGRAPH.CENTER; pf.space_before = Pt(before); pf.space_after = Pt(6)
d.save(here / "reference.docx")
(here / "ref_default.docx").unlink()
print("skrev", here / "reference.docx")
