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
ADVMAIN   := main-pl-a4-adv
LATEXMK   := latexmk -pdf -interaction=nonstopmode -file-line-error

.PHONY: all book book-adv books book-only adv-only check drift answers \
        sets plan clean help

all: books

## books: build BOTH volumes and gate on both logs
books: book-only adv-only check

## book: the basic volume alone, gated
book: book-only drift answers
	python3 tools/checklog.py $(BOOKDIR)/$(BOOKMAIN).log

## book-adv: the advanced volume alone, gated
book-adv: adv-only drift answers
	python3 tools/checklog.py $(BOOKDIR)/$(ADVMAIN).log

## book-only: build the basic volume without the gate
book-only:
	cd $(BOOKDIR) && $(LATEXMK) $(BOOKMAIN).tex || true

## adv-only: build the advanced volume without the gate
adv-only:
	cd $(BOOKDIR) && $(LATEXMK) $(ADVMAIN).tex || true

## check: read BOTH logs properly -- NOT `grep '^!'`, NOT the exit code
#
# Both, always. A gate scoped to one volume is a promise scoped to one volume,
# and the other would go on shipping whatever it liked with every check green.
check: drift answers
	python3 tools/checklog.py $(BOOKDIR)/$(BOOKMAIN).log
	python3 tools/checklog.py $(BOOKDIR)/$(ADVMAIN).log

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
	python3 tools/gen_sets_adv.py --check
	python3 tools/gen_plan.py --check
	python3 tools/gen_plan.py --check --volume adv

## answers: re-compute every printed answer from the printed question
#
# The generator works each answer out from the values it printed, so the two
# cannot disagree -- but a builder that is consistently wrong prints a matching
# pair. This parses the .tex the build consumes and evaluates it by a second
# route, and it refuses to pass over a question shape it does not recognise.
answers:
	python3 tools/checkanswers.py

## sets: regenerate the drill sets AND the plan
#
# Both, always. The plan is a pure function of the set list -- it names sets by
# the number they carry in the book -- so a regenerated set list with a stale
# plan is a plan pointing at the wrong sets. `make plan` alone is for when only
# the schedule changed.
sets:
	python3 tools/gen_sets.py
	python3 tools/gen_sets_adv.py
	python3 tools/gen_plan.py
	python3 tools/gen_plan.py --volume adv

## plan: regenerate both volumes' plans only
plan:
	python3 tools/gen_plan.py
	python3 tools/gen_plan.py --volume adv

## clean: remove build artifacts
clean:
	cd $(BOOKDIR) && latexmk -C $(BOOKMAIN).tex 2>/dev/null || true
	cd $(BOOKDIR) && latexmk -C $(ADVMAIN).tex 2>/dev/null || true
	rm -f $(BOOKDIR)/*.aux $(BOOKDIR)/chapters/*.aux $(BOOKDIR)/frontmatter/*.aux

## help: list targets
help:
	@grep -E '^## ' $(MAKEFILE_LIST) | sed 's/## //'
