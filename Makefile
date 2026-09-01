# ============================================================
#  Trening Mózgu
#
#  ONE artifact: the Stroud A4 book, pdfLaTeX, book/main-pl-a4.tex.
#
#  #16 is decided -- the book is what this repository publishes. The Beamer
#  deck is archived under deck-archive/ and is not built; it never built (#21).
#
#  The unit is a SET: a run of exercises on a page, timed and scored as a whole,
#  with every answer in one appendix at the back. Arithmetic sets are generated
#  by tools/gen_sets.py -- the book is scored on volume, and hundreds of
#  hand-written sums is where arithmetic slips hide. Hand-written sets (logic,
#  sequences, tricks) live in book/sets/ and the generator never touches them.
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

.PHONY: all book book-only check drift answers sets clean help

all: book

## book: build the A4 book and gate on its log
book: book-only check

## book-only: build without the gate (use when iterating on layout)
book-only:
	cd $(BOOKDIR) && $(LATEXMK) $(BOOKMAIN).tex || true

## check: read the log properly -- NOT `grep '^!'`, NOT the exit code
check: drift answers
	python3 tools/checklog.py $(BOOKLOG)

## drift: generated sets must match tools/gen_sets.py
#
# The promise is exactly as wide as the gate: without this, an exercise edited
# in areas/ and never re-converted leaves the book quietly showing the old one,
# and every other check stays green because both files are individually valid.
#
# It also guards the include lists: a set added to gen_sets.py and forgotten in
# sets/generated/_blok-N.tex would be a set nobody ever sees, with every other
# check green, so those lists are generated alongside the sets and compared
# here -- one per block, because a block is a chapter.
drift:
	python3 tools/gen_sets.py --check

## answers: re-compute every printed answer from the printed question
#
# The generator works each answer out from the values it printed, so the two
# cannot disagree -- but a builder that is consistently wrong prints a matching
# pair. This parses the .tex the build consumes and evaluates it by a second
# route, and it refuses to pass over a question shape it does not recognise.
answers:
	python3 tools/checkanswers.py

## sets: regenerate the drill sets
sets:
	python3 tools/gen_sets.py

## clean: remove build artifacts
clean:
	cd $(BOOKDIR) && latexmk -C $(BOOKMAIN).tex 2>/dev/null || true
	rm -f $(BOOKDIR)/*.aux $(BOOKDIR)/chapters/*.aux $(BOOKDIR)/frontmatter/*.aux

## help: list targets
help:
	@grep -E '^## ' $(MAKEFILE_LIST) | sed 's/## //'
