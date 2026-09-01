#!/usr/bin/env python3
"""Check that every frame badge sits in the OUTER margin.

The frame number is this book's whole navigation: a reader thumbing for
exercise 37 runs a finger down the edge of the block. That only works if the
badge follows the spread -- right on a recto, left on a verso -- and it is
exactly the kind of defect that produces no error, no warning and no overfull
box, so no log gate can see it.

Two ways it goes wrong, both silent:

  * something sets \\reversemarginpar, and every badge moves to the INNER
    margin, against the gutter, where a thumb cannot reach it;
  * the run stops before the .aux converges, and marginnote places a badge from
    a stale record of which page parity it was on.

Both leave a PDF that builds clean and reads wrong. This reads the finished
PDF instead: anything printed outside the text block is margin content, and
the side it is on must match the page's parity.

Usage:
    tools/checkbadges.py book/main-pl-a4.pdf
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

# A4 at the geometry set in book/preamble.tex, in PostScript points.
PAGE_W = 595.276
INNER = 96.75   # 3.4 cm
OUTER = 79.67   # 2.8 cm

RE_PAGE = re.compile(r'<page width="([\d.]+)"')
RE_WORD = re.compile(
    r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">'
    r'([^<]*)</word>')


def text_block(page_no: int) -> tuple[float, float]:
    """(left, right) of the text block. Page 1 is a recto."""
    if page_no % 2 == 1:                      # recto: inner margin on the left
        return INNER, PAGE_W - OUTER
    return OUTER, PAGE_W - INNER              # verso: outer margin on the left


def check(pdf: Path) -> bool:
    xml = subprocess.run(["pdftotext", "-bbox", str(pdf), "-"],
                         capture_output=True, text=True, check=True).stdout
    ok, seen, bad = True, 0, []
    # Split on page boundaries, keeping order; page 1 is the first chunk.
    for page_no, chunk in enumerate(xml.split("<page ")[1:], start=1):
        left, right = text_block(page_no)
        for m in RE_WORD.finditer(chunk):
            x0, x1, word = float(m.group(1)), float(m.group(3)), m.group(5)
            # Margin content only. A 2pt tolerance keeps a glyph that just
            # kisses the measure from being read as a margin note.
            if x0 >= left - 2 and x1 <= right + 2:
                continue
            if not word.strip().isdigit():
                continue                       # not a badge; nothing to say
            seen += 1
            in_right = x0 > right
            wants_right = page_no % 2 == 1     # recto -> outer is the right
            if in_right != wants_right:
                ok = False
                side = "right" if in_right else "left"
                bad.append(f"      badge {word.strip()} on page {page_no} "
                           f"({'recto' if page_no % 2 else 'verso'}) "
                           f"is in the {side} margin at x={x0:.1f}")
    print(f"== {pdf.name} ==")
    print(f"  margin badges   : {seen}")
    if not seen:
        print("  NO BADGES FOUND : the check measured nothing, which is not a")
        print("      pass. Either the PDF has no frames or the geometry in")
        print("      this script no longer matches book/preamble.tex.")
        return False
    if bad:
        print(f"  WRONG MARGIN    : {len(bad)}")
        print("\n".join(bad))
        print("      A badge in the inner margin cannot be thumbed for, which")
        print("      is the one thing it exists for. Check that nothing sets")
        print("      \\reversemarginpar, and that the run converged.")
    else:
        print("  wrong margin    : 0")
    return ok


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("pdfs", nargs="+", type=Path)
    a = p.parse_args()
    ok = True
    for pdf in a.pdfs:
        if not pdf.exists():
            print(f"== {pdf} == MISSING")
            ok = False
            continue
        ok &= check(pdf)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
