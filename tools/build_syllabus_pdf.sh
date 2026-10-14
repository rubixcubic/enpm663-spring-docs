#!/usr/bin/env bash
# Build syllabus.pdf from syllabus.md as a tagged, accessible PDF (PDF/UA-2).
#
# pandoc's LaTeX template has no hook before \documentclass, so this script
# takes pandoc's own default template and adds \DocumentMetadata in front of
# \documentclass. LaTeX then tags the PDF itself (headings, tables, links,
# language, title). Run from the repository root:  tools/build_syllabus_pdf.sh
# Needs pandoc and TeX Live 2026 (LuaLaTeX). Check the result with veraPDF:
#   ~/.local/opt/verapdf/verapdf --flavour ua2 --format text syllabus.pdf
set -euo pipefail
export PATH=/usr/local/texlive/2026/bin/x86_64-linux:$PATH
tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT

pandoc -D latex > "$tmp/default.latex"
/usr/bin/python3 - "$tmp" <<'PY'
import sys
folder = sys.argv[1]
text = open(f"{folder}/default.latex").read()
start = text.index("\\documentclass[")
meta = ("\\DocumentMetadata{lang=en-US, pdfversion=2.0, pdfstandard=ua-2, "
        "testphase={phase-III,math,title,table,firstaid}}\n")
open(f"{folder}/tagged.latex", "w").write(text[:start] + meta + text[start:])
PY

# toccolor: the template sets an empty link color for the table of contents,
# which the tagging code rejects; black is what the empty color looked like.
# title-meta and author-meta set the PDF's title and author without adding a
# title block to the first page.
pandoc syllabus.md -o syllabus.pdf --template="$tmp/tagged.latex" \
  --pdf-engine=lualatex \
  -V title-meta="ENPM663 Syllabus: Agentic Physical AI for Manufacturing Robotics, Spring 2027" \
  -V author-meta="Zeid Kootbally" \
  -V geometry:margin=1in -V fontsize=11pt -V documentclass=article \
  -V colorlinks=true -V linkcolor=RoyalBlue -V urlcolor=RoyalBlue -V toccolor=black \
  --toc --toc-depth=2
pdfinfo syllabus.pdf | grep -E "^(Title|Tagged|Pages):"
