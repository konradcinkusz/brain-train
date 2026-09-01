# CLAUDE.md — working on this repository

Context for continuing *Trening Mózgu*. Read this before touching the book.

---

## Status

| | Done | Remaining |
|---|---|---|
| Book (A4, Stroud) | Frame machinery, all 38 exercises, front matter, TOC, chapter frame ranges | A sixth area (#13); difficulty balance (#10, #11) |
| Build | `make book`, three gates, CI on every push and PR, tag-driven release | — |
| Deck (Beamer) | Archived under `deck-archive/`, not built (#16, #21) | — |
| Docs | README, `CONTRIBUTING.md`, this file | — |

The book is **20 pages, 43 frames, zero errors, zero unresolved references,
zero overfull boxes**, with all 43 margin badges in the correct outer margin.

**Re-measure those numbers from the build in front of you.** Page counts and
the overfull multiset are functions of the layout constants and do not survive
being carried across a change.

---

## What this book is

One exercise per **frame** — a slice of page between two hairlines, with its
number in the outer margin. The answer to an exercise does not sit under it: it
opens the **next** frame. The reader covers the page below the rule, works the
exercise against a stopwatch, then reads on.

That single rule is the whole format, and it is why the book is not just the
deck reflowed. A slide deck can put an answer on its own slide because the
reader cannot see it until they advance. A book cannot.

The layout is ported from
[`konradcinkusz/math-for-ai-engineers`](https://github.com/konradcinkusz/math-for-ai-engineers),
whose **code is MIT** (only that book's prose is CC BY-NC-SA).

---

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

**`book/chapters/` is generated. Do not edit it.** It comes from `areas/` via
`tools/convert_deck.py`; edit `areas/` and run `make convert`. `make drift`
fails when the two disagree, and CI runs it before the build.

The generator survived #16 retiring the deck, and the reason is worth keeping:
in `areas/` an exercise sits beside **its own** answer, while in the book the
answer opens the *next* frame and so sits beside the *next* exercise. Authoring
straight into the book format means shifting every answer by one by hand. The
converter does that shift; the gate proves it was not skipped.

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

- **`\begin{fr}`** reserves room before it will typeset, or the rule and its
  margin badge end up as the last things on a page with the frame's body
  overleaf. `\nobreak` cannot prevent this: a frame opening with an unbreakable
  tcolorbox moves itself and leaves the rule behind. `\pagegoal` is `\maxdimen`
  on a fresh page, meaning *unlimited*, not *no room*.
  **The reservation is 5 `\baselineskip` and is PROVISIONAL** — reasoned, not
  swept. A real sweep needs a `checkpdf` port to sweep against. Do not treat it
  as measured until that table exists, and when it does, replace the comment
  with it: a sweep table naming a constant the code no longer uses reads as
  evidence and is worse than none.

- **The badge is a `\marginnote`, never a `\marginpar`.** `\marginpar` floats,
  takes one note per line and defers the rest; at four to eight frames a page
  that is the normal case, and a badge that has moved no longer names the frame
  it belongs to. Loaded `[quiet,noadjust]` — under the default it emits a
  `\strut` into the rule's line. **Nothing may set `\reversemarginpar`**;
  marginnote honours it and would silently move every badge to the inner
  margin. `tools/checkbadges.py` reads the finished PDF and fails on exactly
  that.

- **`\makeatletter` must span the `fr` definition.** `@` is not a letter when
  the environment body is tokenised, so `\bt@framerule` splits and the build
  dies naming `\begin{fr}` rather than the macro. Hit once.

- **`\ans` and `\exercise` take LONG arguments (`+m`).** 20 of the 38 exercises
  set multi-line problems with an explicit `\par`, and an xparse argument is
  short unless asked otherwise. The failure names the macro, not the `\par`.

- **`halign=flush center`, not `halign=center`,** on the answer box. `center`
  stretches glue to fill the measure, so an over-wide answer is hidden by loose
  spacing instead of overflowing where the log can see it.

- **The chapter frame range is a two-pass value** carried in the `.aux`, written
  when the *following* chapter starts (there is no end-of-chapter hook) and read
  back next run. A chapter with no recorded total prints **nothing**, never
  `??`: on a first run every opener would carry the marker, teaching the reader
  to ignore it. Test emptiness with `\ifdefempty`, not
  `\ifx\...\@empty` — `\newcommand` declares a `\long` macro and `\@empty` is
  not one, so `\ifx` compares unequal even with both bodies empty.

---

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
- **Do not judge layout from a low-resolution render.** Twice now an 80 dpi PNG
  suggested the answer box was flush left or its borders asymmetric; at 150 dpi,
  measured in pixels, it was exactly the centred `0.86\linewidth` both times.
  Measure, or say you have not.

---

## Prove a new check fires before trusting it

Both PDF-reading checks were verified by introducing the defect they guard:
`checkbadges.py` against a build with `\reversemarginpar` (24 badges flagged,
exit 1), and `make drift` against an answer edited in `areas/` and not
re-converted (`STALE`, exit 1). A check that has never failed may be measuring
nothing — and both of these read a finished artifact, where a silent pass looks
identical to a real one.

---

## Build

```bash
make book      # build + all three gates
make convert   # areas/ -> book/chapters/
make drift     # are they in sync?
make clean
```

After any change: `make clean && make book`, and re-read the page count and the
overfull multiset rather than carrying the old ones across.

---

## Open decisions, not to be re-litigated from a search result

- **#13 — a sixth area**, authored in `areas/`, shipped as v2.0.0.

Two decisions are CLOSED and should not be re-litigated from a search result:

- **#16 — the book is what this repository publishes.** The deck is archived
  under `deck-archive/` and not built. It never built: its only CI run failed
  and v1.0.0 shipped with no assets (#21). `areas/` remains the authoring
  source for the reason given above.
- **#8 — the title carries no year.** `BrainTrain 2025` read as abandoned in
  late 2026. Adding a year back is one line in three places if that changes.
