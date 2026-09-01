# ============================================================
#  Trening Mózgu
#
#  Two artifacts live in this repository while the book is being ported
#  (issue #14):
#
#    book   -- the Stroud A4 book, pdfLaTeX, book/main-pl-a4.tex
#    deck   -- the original Beamer deck, XeLaTeX, main.tex
#
#  Which of the two is the source of truth is issue #16 and is NOT decided
#  here; until it is, both build and neither is generated from the other.
#
#  NOTE ON THE GATE. `book` runs tools/checklog.py and fails on what it finds.
#  latexmk's own exit code is not sufficient: under -interaction=nonstopmode a
#  failed run still writes a PDF, and with -file-line-error an error line
#  starts with a path rather than "!", so `grep '^!'` misses it too.
# ============================================================

BOOKDIR   := book
BOOKMAIN  := main-pl-a4
BOOKLOG   := $(BOOKDIR)/$(BOOKMAIN).log
BOOKPDF   := $(BOOKDIR)/$(BOOKMAIN).pdf
LATEXMK   := latexmk -pdf -interaction=nonstopmode -file-line-error

.PHONY: all book book-only check deck clean help

all: book

## book: build the A4 book and gate on its log
book: book-only check

## book-only: build without the gate (use when iterating on layout)
book-only:
	cd $(BOOKDIR) && $(LATEXMK) $(BOOKMAIN).tex || true

## check: read the log properly -- NOT `grep '^!'`, NOT the exit code
check:
	python3 tools/checklog.py $(BOOKLOG)
	python3 tools/checkbadges.py $(BOOKPDF)

## deck: build the original Beamer deck (XeLaTeX)
deck:
	latexmk -xelatex -interaction=nonstopmode -file-line-error main.tex

## clean: remove build artifacts from both builds
clean:
	cd $(BOOKDIR) && latexmk -C $(BOOKMAIN).tex 2>/dev/null || true
	latexmk -C main.tex 2>/dev/null || true
	rm -f $(BOOKDIR)/*.aux $(BOOKDIR)/chapters/*.aux $(BOOKDIR)/frontmatter/*.aux

## help: list targets
help:
	@grep -E '^## ' $(MAKEFILE_LIST) | sed 's/## //'
