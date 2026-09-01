# ============================================================
#  Trening Mózgu
#
#  ONE artifact: the Stroud A4 book, pdfLaTeX, book/main-pl-a4.tex.
#
#  #16 is decided -- the book is what this repository publishes. The Beamer
#  deck is archived under deck-archive/ and is not built; it never built (#21).
#
#  areas/ is still the AUTHORING source and book/chapters/ is generated from
#  it, and that is not leftover plumbing: in areas/ an exercise sits next to
#  ITS OWN answer, while in the book the answer belongs to the PREVIOUS frame.
#  Authoring straight into the book format means offsetting every answer by one
#  by hand, which is exactly the mistake convert_deck.py exists to prevent.
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

.PHONY: all book book-only check drift convert clean help

all: book

## book: build the A4 book and gate on its log
book: book-only check

## book-only: build without the gate (use when iterating on layout)
book-only:
	cd $(BOOKDIR) && $(LATEXMK) $(BOOKMAIN).tex || true

## check: read the log properly -- NOT `grep '^!'`, NOT the exit code
check: drift
	python3 tools/checklog.py $(BOOKLOG)
	python3 tools/checkbadges.py $(BOOKPDF)

## drift: book/chapters/ must match areas/ -- they are generated from it
#
# The promise is exactly as wide as the gate: without this, an exercise edited
# in areas/ and never re-converted leaves the book quietly showing the old one,
# and every other check stays green because both files are individually valid.
#
# #16 is decided and this gate SURVIVES it. The deck is retired, but areas/ is
# still where exercises are authored, for the reason in the header: the answer
# shift is a presentation detail and doing it by hand is the error this gate
# and the converter exist to prevent. What changed is the reason -- it is no
# longer bridging two outputs, it is guarding one generation step.
drift:
	python3 tools/convert_deck.py --check

## convert: regenerate book/chapters/ from areas/
convert:
	python3 tools/convert_deck.py

## clean: remove build artifacts
clean:
	cd $(BOOKDIR) && latexmk -C $(BOOKMAIN).tex 2>/dev/null || true
	rm -f $(BOOKDIR)/*.aux $(BOOKDIR)/chapters/*.aux $(BOOKDIR)/frontmatter/*.aux

## help: list targets
help:
	@grep -E '^## ' $(MAKEFILE_LIST) | sed 's/## //'
