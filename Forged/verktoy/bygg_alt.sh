#!/usr/bin/env bash
# Bygger alle leveranser fra manus/0*.md. Kjør fra Forged/bok:  bash ../verktoy/bygg_alt.sh
# Valgfritt: EZRA=/sti/til/slop_scan.py  EPUBCHECK=/sti/til/epubcheck.jar
set -e
cd "$(dirname "$0")/../bok"
(cd manus && python3 ../../verktoy/bygg_manus.py .)
python3 ../verktoy/antitese_scan.py manus/FORGED_manus.md --allow ../verktoy/antitese_unntak.txt | tail -2
if [ -n "$EZRA" ]; then python3 "$EZRA" manus/FORGED_manus.md --lang en --gate --quiet && echo "Ezra-sperren: exit 0"; fi
python3 ../verktoy/lesbarhet.py manus/FORGED_manus.md
python3 ../verktoy/sett_bok.py manus/FORGED_manus.md ut/FORGED_Interior_6x9_KDP.pdf
python3 ../verktoy/sett_bok.py manus/FORGED_manus.md ut/FORGED_Interior_5x8_KDP.pdf --trim 5x8
rm -f ut/*.typ
python3 ../verktoy/sjekk_innhold.py ut/FORGED_Interior_6x9_KDP.pdf | tail -1
python3 ../verktoy/sjekk_innhold.py ut/FORGED_Interior_5x8_KDP.pdf | tail -1
python3 ../verktoy/bygg_epub.py manus/FORGED_manus.md ut/FORGED_Kindle.epub
if [ -n "$EPUBCHECK" ]; then java -jar "$EPUBCHECK" ut/FORGED_Kindle.epub 2>&1 | grep Messages; fi
python3 ../verktoy/bygg_docx.py manus/FORGED_manus.md ut/FORGED_manus.docx
cp manus/FORGED_manus.md ut/FORGED_manus.md
python3 ../verktoy/bygg_gdoc_rtf.py manus/FORGED_manus.md ut/FORGED_GoogleDocs.rtf
cp manus/FORGED_manus.md 04-forged-redigert.md
python3 ../verktoy/lag_videogrunnlag.py kilder/videomanus_2026-08-05.json manus/FORGED_manus.md 15-vedlegg-videomanus-mot-bok.md
