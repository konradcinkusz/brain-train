# CLAUDE.md — working on this repository

Context for continuing *Trening Mózgu*. Read this before touching the book.

---

## Status

| | Done | Remaining |
|---|---|---|
| Book (A4) | 29 sets, 1064 exercises, front matter, TOC, answer appendix | — |
| Build | `make book`, three gates, CI on every push and PR, tag-driven release | — |
| Deck (Beamer) | Archived under `deck-archive/`, not built (#16, #21) | — |
| Docs | README, `CONTRIBUTING.md`, this file | — |

The book is **27 pages, 29 sets, 1064 exercises, zero errors, zero unresolved
references, zero overfull boxes**.

**Re-measure those numbers from the build in front of you.** Page counts and
the overfull multiset are functions of the layout constants and do not survive
being carried across a change.

---

## What this book is

A **drill book**. The unit is a **set**: a page of short exercises listed one
under another, done in one go against a stopwatch, scored as a whole. Every
answer is in one appendix at the **back**. Every arithmetic set is the same
length -- the count lives in `N` in `tools/gen_sets.py` and nowhere else --
because two times only compare if they measure the same work.

**What it measures is throughput, not the correctness of any one exercise.** How
many you got through, how fast, and whether that improves when you come back to
the same set a week later — which is why every set has a Czas / Poprawne / Data
box under it.

### The design this replaced, and why

The first version gave every exercise its own **frame**, with the answer opening
the next one — Stroud's programmed-instruction layout, ported from
[`math-for-ai-engineers`](https://github.com/konradcinkusz/math-for-ai-engineers).
It was carefully built and it was the wrong shape for this book. That layout
exists to teach a step. Here it put **two exercises on a page**, made the page
ceremony rather than work, and dropped an answer into the middle of a run the
reader is being timed on. 52 exercises took 26 pages; the same book now carries
over a thousand in 27.

Nothing of it is kept. It is in `deck-archive/` with its own note.

## Non-negotiable conventions

**No instruction may depend on where the page breaks.** Write *zanim
przeczytasz dalej*, never *zanim odwrócisz stronę*. Where a page breaks is a
property of the format; an instruction naming a page turn is true in one build
and false in another. *Zakryj dłonią stronę poniżej* is fine — it names the
reader's hand, not the leaf.

**The gate is `tools/checklog.py`, never latexmk's exit code and never
`grep '^!'`.** Under `-interaction=nonstopmode` a failed run still writes a
PDF, and with `-file-line-error` an error line begins with a path rather than
`!`. A build can be broken, silent and green all at once — that is exactly how
v1.0.0 shipped with no PDF (#21).

**`book/sets/generated/` is generated. Do not edit it.** It comes from
`tools/gen_sets.py`; edit the generator and run `make sets`. `make drift` fails
when the two disagree, and CI runs it before the build. It fails on a file the
generator no longer produces, too: renaming a set otherwise leaves the old one
in the tree, out of `_all.tex` and out of `SETS`, where nothing looks at it
again and it still reads like a set the book contains.

**No two exercises in a set are the same.** Forty draws from the sixty-four
multiplication-table pairs collide about nine times; `distinct()` in the
generator is what stops it, and its attempt bound is what makes a builder whose
range is too narrow fail loudly instead of spinning forever.

**A seed belongs to a set forever.** Reordering and renaming the `SETS` list is
free. Changing a seed silently replaces forty exercises, and a reader comparing
this month's time against last month's is then comparing two different sets --
which is the one thing this book exists to make possible.

**Arithmetic is generated; puzzles are not.** The book is scored on volume, and
several hundred hand-typed sums is where arithmetic slips hide — the generator
computes each answer with the same three lines that lay out its question, so a
printed answer cannot disagree with its printed question. A word trap is a joke
and a joke has an author, so those stay hand-written in `book/sets/`.

**The generator is deterministic.** Every set seeds its own `Random` with a
fixed integer. A drill book whose pages change under you cannot be re-run to
compare times, which is the one thing this book is for.

**A digit stays a digit, and diacritics are copied as found.** The deck mixes
UTF-8 (`Kolejność`) with TeX escapes (`Mno\. zenie`); both reach the same glyph
and normalising one into the other is a silent edit to 38 exercises.

**An answer shows the result plus at most a one-line hint.** No step-by-step,
no teaching — the repo's own rule, from commit `01c9d37`.

**Never state a count of occurrences in prose.** A tally decays silently and no
check can see it. Name the rule and the places it applies.

---

## The layout, and why its numbers are what they are

Everything below is in `book/preamble.tex` beside the code it governs.

- **Margins are tight (1.5--1.8 cm).** The page is a worksheet; every millimetre
  of margin is an exercise that did not fit. Nothing lives in the margins any
  more, so nothing needs room out there.

- **Stars and the target time print once, at the head of the set.** They are
  properties of the set, not of an exercise. Repeating them on every line would
  be noise that costs exercises.

- **A set is one unbreakable block, and columns are boxes rather than
  `multicols`.** multicol cannot be put in a box -- it refuses -- so a set built
  with it is always splittable, and once sets reached forty exercises the page
  breaks started landing between the last exercise and the Czas / Poprawne /
  Data box. That box is the product; on the far side of a page turn it is
  useless. A set is now a row of minipages, which is one horizontal box and
  cannot break, with `\nobreak` before every internal `\vspace` in the head and
  foot -- **`\par\vspace{4pt}` puts glue straight after a line box, which is a
  legal breakpoint, and that is the one the page-breaker actually took.** The
  generator emits `\btnc` where each column ends, which also balances them
  exactly (14/13/13, against multicol's 14/14/12 under `\raggedcolumns`).

- **The answer appendix boxes each set's block too.** A page that begins in the
  middle of a list begins with numbers and no heading, and this appendix is a
  lookup table.

- **Answers reach the back through a global macro store**, not the `.aux`.
  Material written to an aux-style file is expanded at shipout, where a fragile
  command breaks with an error naming neither the answer nor the set it came
  from. `\include` is sequential within a run, so a macro defined globally while
  typesetting set 3 is still defined when the appendix is set. `\csxappto`
  freezes the exercise number at store time while `\unexpanded` keeps the
  answer's own tokens literal, so `$` and `\frac` survive to the back page.

- **The answer separator is `\btsep`, never `\quad`.** An answer list is a long
  run of short unbreakable items with no hyphenation anywhere in it, so a rigid
  separator leaves TeX no affordable breakpoint and every line comes out
  overfull — measured at 12.0 pt, seventeen times, on this appendix's first
  build. `\btsep` carries a `\penalty0` and stretch; the appendix is also set
  `\raggedright`, because it is a lookup table and there is nothing to gain from
  justifying it.

- **`\zz`'s parbox reserves 5.6em, not 3.6em.** It must leave room for
  *everything* beside it: the 2.1em number box before and the 2.6em answer rule
  after. Reserving 3.6em for 4.7em of furniture overflowed every wide line by
  exactly the missing 1.1em. **The constant 12.045 pt across sixteen boxes is
  what said it was arithmetic rather than bad line breaking** — a varying
  overflow is a paragraph problem, an identical one is a sum that does not add
  up.

- **Internal macros carry no `@`.** `@` is not a letter outside
  `\makeatletter`, so `\newcommand{\bt@foo}` splits and the build dies with
  *You already have nine parameters* pointing at the wrong line. This preamble
  was bitten by that twice; a `bt` prefix marks a macro internal without needing
  a catcode change.


## Traps already hit

- **Do not load `newtx`.** The source repository probes for it and degrades,
  which made its TS1 font map a trap on a half-installed machine. This preamble
  simply never asks.
- **XeLaTeX with `[T1]{fontenc}` + `inputenc` has no Polish glyphs.** That is
  #21: the deck is built that way and every diacritic is silently dropped.
  The book uses pdfLaTeX, where that stack is correct.
- **latexmk caches a failed run.** After fixing something *outside* the source
  tree (an installed package), latexmk reports "Nothing to do" and the stale
  log then drives the gate. Delete `.fdb_latexmk` and the log.
- **A killed latexmk can leave a NUL-filled `.out`,** and the next run dies with
  *Text line contains an invalid character* in a file nobody edited. The tell is
  that the error names an `.out`, `.aux` or `.toc` rather than a `.tex`.
- **Do not judge layout from a low-resolution render.** Twice an 80 dpi PNG
  suggested a box was misplaced; measured at 150 dpi it was exactly right both
  times. Measure, or say you have not.
- **A constant overfull width is arithmetic, not line breaking.** Sixteen boxes
  at an identical 12.045 pt was the tell; see the `zz` parbox above.

---

## Prove a new check fires before trusting it

`make drift` was verified by editing the generator without regenerating
(`STALE`, exit 1). The split-set check was verified by putting a `\newpage`
between a set's grid and its foot: every set reported `Zestaw N is split`, and
`make book` exited 1. A check that has never failed may be measuring nothing.

**And retire a check that has stopped measuring.** `checkbadges.py` guarded
frame numbers in the outer margin. There are no margin numbers now, so it would
pass forever on a book it no longer describes; it is archived rather than left
in the gate looking like coverage.

---

## Releasing, and the one thing a web session cannot do

**A tag cannot be pushed from a Claude Code web session.** `git push origin
<tag>` returns HTTP 403 through the sandbox's git proxy, and every release tool
available there is read-only, so a session can prepare a release and cannot cut
one. Tag from a local clone:

```bash
git checkout main && git pull
git tag -a v2.0.0 -m "..." && git push origin v2.0.0
```

The tag is the only manual step. `ci.yml` does the rest and cannot publish an
empty release: the artifact upload is `if-no-files-found: error`, the release
step is `fail_on_unmatched_files`, and a `test -s` stands between them.

**Verify a release by looking at its assets, not at the workflow going green.**
v1.0.0 is the worked example of why — it exists, it is not a draft, and it
carries nothing.

## Build

```bash
make book      # build + all three gates
make sets      # regenerate the drill sets
make drift     # are they in sync?
make clean
```

After any change: `make clean && make book`, and re-read the page count and the
overfull multiset rather than carrying the old ones across.

---

## Open decisions, not to be re-litigated from a search result

Three decisions are CLOSED and should not be re-litigated from a search result:

- **#16 — the book is what this repository publishes.** The deck is archived
  under `deck-archive/` and not built. It never built: its only CI run failed
  and v1.0.0 shipped with no assets (#21). `areas/` remains the authoring
  source for the reason given above.
- **#8 — the title carries no year.** `BrainTrain 2025` read as abandoned in
  late 2026. Adding a year back is one line in three places if that changes.
- **#13 — the sixth area is *Szybkie Triki Liczbowe*.** *Pamięć* was the other
  serious candidate and was rejected on a structural ground worth keeping: this
  format cannot hide what is above the reader's hand, so a memory exercise can
  always be re-read rather than recalled. The format fights that area; it does
  not fight shortcuts.
