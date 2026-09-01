#!/usr/bin/env python3
"""Decide whether a LaTeX run actually succeeded.

Ported from konradcinkusz/math-for-ai-engineers (MIT), trimmed to what this
book has. The reason it exists is mechanical and applies to any LaTeX project:

  * with -file-line-error, an error line begins with a PATH, not with `!`
    (`./preamble.tex:735: Illegal parameter number ...`), so the usual
    `grep '^!' main.log` cannot see it;
  * -interaction=nonstopmode recovers from errors and still writes a PDF, so
    the exit code and the existence of the PDF both say "fine".

Between them a build can be broken, silent, and green. In the source
repository that combination hid a package that had stopped loading at all,
through a whole draft. Neither latexmk's exit code nor a grep is the gate;
this is.

Usage:
    tools/checklog.py book/main-pl-a4.log
    tools/checklog.py --summary book/main-pl-a4.log   # one-liner, for CI

Exit code is non-zero if any log carries an error, an unresolved reference, an
overfull vbox, an hbox over the budget, or a sign that the run never converged
-- the things that must never reach a reader.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

RE_BANG = re.compile(r"^! (.*)$", re.M)
RE_FILELINE = re.compile(r"^(?:\./|/)[^\s:]+:\d+: (.*)$", re.M)
RE_UNDEF_REF = re.compile(r"Reference `([^']+)' on page \d+ undefined", re.M)
RE_UNDEF_CIT = re.compile(r"Citation `([^']+)' on page \d+ undefined", re.M)
RE_HBOX = re.compile(r"Overfull \\hbox \(([\d.]+)pt")
RE_VBOX = re.compile(r"Overfull \\vbox \(([\d.]+)pt")
# WHERE a vbox happened, and it matters that TeX says this two different ways:
#
#   Overfull \vbox (12.3pt too high) has occurred while \output is active [456]
#   Overfull \vbox (5.0pt too high) detected at line 1234
#
# The first is a PAGE that came out too tall, and its position moves when
# anything before it moves. The second is a FIXED BOX -- a \parbox, a minipage,
# a tcolorbox -- that is too tall for the space it was given, and it is
# invariant under repagination. Reporting only the size makes the two
# indistinguishable, and this repository lost a cycle to exactly that: a glue
# change moved the whole book and the two reported sizes came back identical,
# which was the tell that at least one of them was not a page at all.
#
# The source file is tracked too, because "detected at line 1234" without a
# file is not a location. TeX brackets each file it opens, so the innermost
# unclosed `(` at the point of the complaint is the file being read.
RE_SHIPOUT = re.compile(r"\[(\d+)[^\]]*\]")
RE_VBOX_WHERE = re.compile(
    r"has occurred while \\output is active|detected at line (\d+)")
# Document content only. A .sty or .cls is read in the preamble and can
# never be where a typeset box was built, so matching them would report the
# last package loaded and nothing useful.
RE_FILE_OPEN = re.compile(r"\((\.{0,2}/[^\s()]*\.(?:tex|ind|toc))")
RE_PAGES = re.compile(r"Output written on \S+ \((\d+) pages")
# Warnings that are always worth surfacing. Font substitution noise is not.
RE_WARN = re.compile(r"^(?:LaTeX|Package|Class) (\w+ )?Warning: (.*)$", re.M)
WARN_IGNORE = ("Font shape", "Some font shapes", "Size substitutions",
               "Token not allowed", "There were undefined references")

# Warnings that must FAIL a build rather than be printed and shrugged at.
#
# A non-converged build exits 0 with a stale number on the page, and report()
# does not fail on an ordinary warning -- so the warnings that mean "the .aux
# was still moving when I stopped" have to be named here or they are shrugged
# at.
#
# This matters for this book specifically. marginnote records which margin each
# frame badge belongs in through the .aux, so a run that stops early can put a
# badge in the inner margin, or against the wrong line, and NOTHING else will
# say so: the failure is a badge in the wrong place, not a missing one. The
# frame number is the whole of this book's navigation, which makes that a
# content defect rather than a cosmetic one.
#
# "Marginpar on page N moved" cannot fire while the design uses \marginnote
# rather than \marginpar. It stays as a tripwire: if somebody ever swaps the
# badge back to \marginpar, the build says so instead of quietly deferring
# every badge on a busy page.
HARD_WARN = ("Label(s) may have changed", "Rerun to get", "Marginpar on page",
             "Consecutive odd pages", "Consecutive even pages")

HBOX_BUDGET = 15.0   # pt. Anything above this visibly runs into the margin.


def _vbox_where(text: str, pos: int) -> str:
    """Describe where an overfull vbox at `pos` happened, as TeX reported it.

    Returns "PDF page N" for a page that came out too tall, or
    "<file> line N" for a fixed box that did not fit the space it was given.
    The two need different fixes and only TeX knows which is which.
    """
    tail = text[pos:pos + 300].replace("\n", "")
    m = RE_VBOX_WHERE.search(tail)
    if m and m.group(1):
        return f"line {m.group(1)}, {_open_file(text, pos)}"
    page = RE_SHIPOUT.search(tail)
    return f"on PDF page {page.group(1)}" if page else "at an unknown location"


def _open_file(text: str, pos: int) -> str:
    """The last file TeX opened before `pos`.

    Deliberately NOT a bracket-matching stack. A TeX log is full of unmatched
    parentheses in ordinary prose and in package chatter, so a stack empties
    itself within a few thousand characters and then reports nothing -- which
    was tried, and did. The last file opened is a starting point rather than a
    guarantee, and the report says so rather than claiming more than it knows.
    """
    opens = list(RE_FILE_OPEN.finditer(text, 0, pos))
    return (f"in or after {opens[-1].group(1)}" if opens
            else "in a file TeX did not name")


def analyse(path: Path) -> dict:
    text = path.read_text(encoding="utf8", errors="replace")
    errors = RE_BANG.findall(text) + RE_FILELINE.findall(text)
    warns = [
        f"{m.group(1) or ''}{m.group(2)}".strip()
        for m in RE_WARN.finditer(text)
        if not any(s in m.group(2) for s in WARN_IGNORE)
    ]
    h = sorted((float(x) for x in RE_HBOX.findall(text)), reverse=True)
    v = sorted((float(x) for x in RE_VBOX.findall(text)), reverse=True)
    v_pages = [(float(m.group(1)), _vbox_where(text, m.end()))
               for m in RE_VBOX.finditer(text)]
    v_pages.sort(key=lambda t: -t[0])
    pages = RE_PAGES.search(text)
    return {
        "file": path.name,
        "errors": errors,
        "warnings": warns,
        "hard_warnings": [w for w in warns if any(s in w for s in HARD_WARN)],
        "undef_refs": RE_UNDEF_REF.findall(text),
        "undef_cits": RE_UNDEF_CIT.findall(text),
        "hbox": h,
        "vbox": v,
        "vbox_pages": v_pages,
        "over_budget": [x for x in h if x > HBOX_BUDGET],
        "pages": int(pages.group(1)) if pages else None,
    }


def report(r: dict) -> bool:
    ok = True
    print(f"== {r['file']} ==")
    print(f"  pages           : {r['pages']}")
    if r["errors"]:
        ok = False
        print(f"  ERRORS          : {len(r['errors'])}")
        for e in r["errors"][:12]:
            print(f"      {e}")
    else:
        print("  errors          : 0")
    if r["undef_refs"] or r["undef_cits"]:
        ok = False
        print(f"  UNRESOLVED REFS : {sorted(set(r['undef_refs'] + r['undef_cits']))}")
    else:
        print("  unresolved refs : 0")
    print(f"  overfull hbox   : {len(r['hbox'])} "
          f"{[round(x, 1) for x in r['hbox'][:8]]}")
    if r["over_budget"]:
        ok = False
        print(f"  OVER {HBOX_BUDGET:.0f} pt BUDGET : {[round(x, 1) for x in r['over_budget']]}")
    if r["vbox"]:
        ok = False
        print(f"  OVERFULL VBOX   : {len(r['vbox'])} {[round(x, 1) for x in r['vbox'][:5]]}")
        for size, where in r["vbox_pages"][:5]:
            print(f"      {size:6.1f} pt too high, {where}")
        print("      A vbox means a block grew past the space it had and could")
        print("      not break. Split the table; do not shrink the text.")
        print("      READ THE LOCATION: `PDF page N` is a page that came out")
        print("      too tall and moves when anything before it moves; a file")
        print("      and line is a FIXED box -- a parbox, a minipage, a")
        print("      tcolorbox -- that does not. They need different fixes.")
        print("      It is printed because a local TeX install and CI's do not")
        print("      paginate alike, so the machine that must fix it is often")
        print("      not the one that saw it.")
    else:
        print("  overfull vbox   : 0")
    if r["hard_warnings"]:
        ok = False
        print(f"  NON-CONVERGENCE : {len(r['hard_warnings'])}")
        for w in r["hard_warnings"][:6]:
            print(f"      {w}")
        print("      The build stopped rerunning while the .aux was still")
        print("      moving. A frame badge may be in the wrong margin or")
        print("      against the wrong line. Run latexmk again.")
    if r["warnings"]:
        print(f"  warnings        : {len(r['warnings'])}")
        for w in r["warnings"][:6]:
            print(f"      {w}")
    return ok


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("logs", nargs="+", type=Path)
    p.add_argument("--summary", action="store_true")
    a = p.parse_args()
    ok = True
    for path in a.logs:
        if not path.exists():
            print(f"== {path} == MISSING")
            ok = False
            continue
        r = analyse(path)
        if a.summary:
            print(f"{r['file']}: pages={r['pages']} errors={len(r['errors'])} "
                  f"refs={len(set(r['undef_refs']))} hbox={len(r['hbox'])} "
                  f"vbox={len(r['vbox'])} warn={len(r['warnings'])}")
            ok &= not (r["errors"] or r["undef_refs"] or r["vbox"]
                       or r["over_budget"] or r["hard_warnings"])
        else:
            ok &= report(r)
    return 0 if ok else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        # `checklog.py ... | head` closes the pipe. Exiting quietly is the
        # right behaviour; a traceback here reads as a failure of the check.
        sys.exit(0)
