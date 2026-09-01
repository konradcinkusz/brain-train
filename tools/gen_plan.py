#!/usr/bin/env python3
"""Lay the book's sets over thirteen weeks of daily training.

WHY THIS IS GENERATED AND NOT TYPED. A plan is a table of ninety-one rows, each
naming a set by a number that comes from where that set sits in the book. Typed
out by hand it is ninety-one chances to name a set that moved, and every one of
them would print without complaint -- a plan that sends the reader to Zestaw 41
on a Tuesday is wrong in a way no build can see. Here the numbers come from
tools/gen_sets.py's own book_order(), so the plan cannot name a set the book
does not have, and `--manifest` closes the other half by checking those numbers
against the ones LaTeX actually printed.

    tools/gen_plan.py                 # write book/plan/generated/
    tools/gen_plan.py --check         # fail if the tree is stale

The other half -- that the number the plan prints is the number LaTeX steps to
-- is closed in the book rather than here: the generated include lists emit
\\btexpect{n} before every set, and a set that comes up under a different
number stops the build. A check that lives where the mistake happens beats one
that reads a file afterwards.

THE THREE THINGS THE SCHEDULE IS BUILT ON, none of them invented here:

  Progressive overload. Blok I for four weeks, Blok II for five, Blok III for
  four. A month of two-digit addition is what makes three-digit addition a
  question of speed rather than of method.

  Interleaving. Consecutive days do not repeat a family, which is why every set
  declares one. Blocked practice -- six addition sets in six days -- reads as
  faster while you do it and is worse a week later. This costs nothing to
  arrange and the reader never sees it.

  Spaced repetition. Every day after the first week re-does the set from seven
  days earlier, against the time already written under it. That is the one
  measurement this book exists to produce, and until now nothing told the
  reader when to take it.

Every seventh day is a POMIAR KONTROLNY: the benchmark set of the current
block, done again, with five scoring rows on its own page. Weekly, over four or
five weeks, on identical work -- which is a progress curve rather than an
impression of one.
"""
from __future__ import annotations

import argparse
import sys
from collections import defaultdict, deque
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gen_sets import BLOCK_TITLES, book_order  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "book" / "plan" / "generated"

WEEKS = 13
DAYS = 7                      # a training week, rest days included by the reader
BENCH_DAY = 7                 # the last day of each week is a measurement
# Which block each week trains. Four, five, four: Blok II is the working range
# and the one worth the extra week.
PHASE = {**{w: 1 for w in range(1, 5)},
         **{w: 2 for w in range(5, 10)},
         **{w: 3 for w in range(10, 14)}}


def interleave(items):
    """Order a pool so that no two consecutive sets drill the same family.

    Greedy and deterministic: always take from the family with the most left,
    never the family just taken. Ties break on the family name rather than on
    dictionary order, because a plan that changes when Python's hashing changes
    is not a plan anybody can re-run.
    """
    pool = defaultdict(deque)
    for it in items:
        pool[it.family].append(it)
    out, last = [], None
    while any(pool.values()):
        fams = sorted((f for f, q in pool.items() if q),
                      key=lambda f: (-len(pool[f]), f))
        pick = next((f for f in fams if f != last), fams[0])
        out.append(pool[pick].popleft())
        last = pick
    return out


def select(items, k):
    """The k sets a phase actually uses, covering every family it has before
    any family gets a second set.

    The naive answer -- interleave, then take the first k -- drops the tail,
    and the tail of a greedy interleave is the SMALL families: the one set of
    roman numerals, the one on means, the one on fractions, while a third set
    of two-digit addition stays in. That is exactly backwards. Round-robin by
    family name until the quota is filled, so what falls out is the redundant
    copy rather than the only copy.
    """
    pool = defaultdict(deque)
    for it in items:
        pool[it.family].append(it)
    picked = []
    while len(picked) < k and any(pool.values()):
        for f in sorted(pool):
            if pool[f]:
                picked.append(pool[f].popleft())
                if len(picked) == k:
                    break
    taken = {id(x) for x in picked}
    return picked, [x for x in items if id(x) not in taken]


def schedule():
    """Ninety-one days, and the spare sets the plan did not need."""
    order = book_order()
    bench = {i.stars: i for i in order if i.block == 5}
    # Blok III shares its weeks with the hand-written puzzle sets: they are the
    # longest and least mechanical in the book, so they belong where the reader
    # is strongest rather than in week two. They go through interleave() WITH
    # the block rather than after it -- appended, all four landed on
    # consecutive days at the very end, which is the blocked practice this
    # whole ordering exists to avoid.
    phase = {p: [i for i in order if i.block == p] for p in (1, 2, 3)}
    phase[3] += [i for i in order if i.block == 4]

    # How many days each phase has to fill, which is what decides how many of
    # its sets are used at all.
    need = {p: sum(DAYS - 1 for w, q in PHASE.items() if q == p) for p in (1, 2, 3)}
    pools, spare = {}, []
    for p, xs in phase.items():
        picked, left = select(xs, need[p])
        pools[p], spare = deque(interleave(picked)), spare + left

    days = []
    for week in range(1, WEEKS + 1):
        p = PHASE[week]
        for d in range(1, DAYS + 1):
            n = (week - 1) * DAYS + d
            if d == BENCH_DAY:
                days.append((n, week, bench[p], True))
            else:
                days.append((n, week, pools[p].popleft(), False))

    # The repeat is the set from seven days earlier. On a day whose predecessor
    # a week back was itself a measurement, step one further: re-doing the
    # benchmark off-schedule would put a sixth measurement in a five-row box.
    byday = {n: (item, is_bench) for n, _, item, is_bench in days}
    repeats = {}
    for n, _, _, is_bench in days:
        if is_bench or n <= DAYS:
            continue
        back = n - DAYS
        if byday[back][1]:
            back -= 1
        repeats[n] = byday[back][0]
    return days, repeats, spare


def esc(s: str) -> str:
    return s.replace("—", "---")


def render(days, repeats, spare) -> str:
    out = ["% GENERATED by tools/gen_plan.py -- do not edit.\n"]
    for week in range(1, WEEKS + 1):
        rows = [d for d in days if d[1] == week]
        out.append(f"\n\\btweek{{{week}}}{{Blok "
                   f"{'I' * PHASE[week]} --- {BLOCK_TITLES[PHASE[week]]}}}\n")
        # \noindent: a tabular opens a paragraph, and without this every
        # table in the plan sits one \parindent to the right of the rule above
        # it.
        out.append("\\noindent\\begin{tabular}{@{}r@{\\ \\ }p{6.4cm}"
                   "c@{\\quad}c@{\\quad}l@{\\quad}l@{\\quad}l@{}}\n")
        out.append("  \\btplanhead\n")
        for n, _, item, is_bench in rows:
            # The number alone, not `Zestaw 41`: the column is headed
            # `Zestaw dnia`, and repeating the word in ninety-one rows is what
            # was pushing every title onto a second line.
            # A middle dot, not a dash: seven of the titles carry a dash of
            # their own, and `24 --- Mieszane --- start` reads as three things.
            label = (f"\\textbf{{{item.num}}}~\\textperiodcentered\\ "
                     f"{esc(item.title)}")
            rep = repeats.get(n)
            out.append(f"  {n} & {label} & {item.target} & "
                       f"{rep.num if rep else '---'} & "
                       f"\\btline{{1.5cm}} & \\btline{{1.2cm}} & "
                       f"\\btline{{1cm}}\\,/\\,{item.count} \\\\\n")
        out.append("\\end{tabular}\n")

    out.append("\n\\btweek{Zapas}{poza planem}\n")
    out.append("Plan nie zużywa całej książki. Te zestawy zostają na czwarty "
               "miesiąc albo na dodatkową powtórkę w dniu, w którym zostało "
               "Ci jeszcze pięć minut:\n\n")
    out.append("\\begin{itemize}\\setlength{\\itemsep}{0pt}\n")
    for i in spare:
        out.append(f"  \\item Zestaw {i.num} --- {esc(i.title)} "
                   f"({i.target})\n")
    out.append("\\end{itemize}\n")
    return "".join(out)


def write(text: str, name: str, check: bool) -> bool:
    OUT.mkdir(parents=True, exist_ok=True)
    dest = OUT / name
    cur = dest.read_text(encoding="utf8") if dest.exists() else None
    if cur == text:
        return False
    if check:
        print(f"  STALE   {dest.relative_to(ROOT)}")
        return True
    dest.write_text(text, encoding="utf8")
    return False


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--check", action="store_true")
    a = p.parse_args()

    days, repeats, spare = schedule()
    stale = write(render(days, repeats, spare), "plan.tex", a.check)
    if stale:
        print("\nPlan out of date. Run `make plan`.")
        return 1

    runs, longest, prev = 1, 1, None
    for _, _, item, is_bench in days:
        if not is_bench:
            runs = runs + 1 if item.family == prev else 1
            longest, prev = max(longest, runs), item.family
    print(f"  {len(days)} dni · {WEEKS} tygodni · "
          f"{sum(1 for d in days if d[3])} pomiarów kontrolnych · "
          f"{len(repeats)} powtórek · {len(spare)} zestawów w zapasie")
    print(f"  najdłuższa seria tej samej rodziny pod rząd: {longest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
