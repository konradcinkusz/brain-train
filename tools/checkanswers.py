#!/usr/bin/env python3
"""Re-compute every printed answer from the printed question.

WHY THIS EXISTS, GIVEN THE GENERATOR ALREADY GUARANTEES IT. tools/gen_sets.py
computes each answer from the same values it lays out, so a printed answer
cannot disagree with its printed question -- that is the repository's own
argument for generating the arithmetic, and it holds. What it does not cover is
a builder that is CONSISTENTLY wrong: a `-` where the code means `+`, a
formatter that drops a thousands separator, a percentage applied to the wrong
operand. Both halves would come out of one mistake, agree perfectly, and print.

So this reads the .tex the build actually consumes, parses the question a reader
sees, and works the answer out by a second route. It is the only check here that
looks at the page rather than at the code that made it.

    tools/checkanswers.py           # every generated set
    tools/checkanswers.py --list    # what each shape parses to, for a new builder

AN UNKNOWN SHAPE IS A FAILURE, not a skip. A checker that silently passes over
what it does not recognise stops measuring the moment somebody adds a builder,
and it would go on printing a green line about the sets it still understands.
Adding a builder therefore means adding its shape here, which is the cost of
having the check mean anything.

Hand-written sets under book/sets/ are not read: a logic puzzle's answer is a
judgement and there is no second route to it.
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from fractions import Fraction
from math import gcd, isqrt
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GEN = ROOT / "book" / "sets" / "generated"

ROMAN_V = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
ROMAN_W = ((100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
           (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"))
UNIT_K = {("km", "m"): 1000, ("m", "cm"): 100, ("cm", "mm"): 10,
          ("kg", "g"): 1000, ("t", "kg"): 1000, ("l", "ml"): 1000,
          ("h", "min"): 60, ("min", "s"): 60}


def from_roman(s: str) -> int:
    t = 0
    for i, c in enumerate(s):
        v = ROMAN_V[c]
        t += -v if i + 1 < len(s) and ROMAN_V[s[i + 1]] > v else v
    return t


def to_roman(n: int) -> str:
    out = ""
    for v, s in ROMAN_W:
        while n >= v:
            out, n = out + s, n - v
    return out


def n(s: str) -> Fraction:
    """A printed integer. The thousands separator is a BACKSLASH-comma; a bare
    comma is a decimal point, and confusing the two is how `7,2` becomes 72."""
    s = s.replace("\\,", "").replace(" ", "")
    return Fraction(s.replace(",", ".")) if "," in s else Fraction(s)


def canon(a: str):
    """The printed answer as something comparable: a number where it is one, and
    otherwise the string itself -- `tak`, `CXCVIII`, `9 r. 2`, `25\\%`."""
    a = a.strip()
    neg = False
    if re.fullmatch(r"\$-[\d\\,]+\$", a):
        a, neg = a.strip("$")[1:], True
    bare = a.replace("\\,", "")
    if re.fullmatch(r"\d+(,\d+)?", bare):
        v = n(bare)
        return -v if neg else v
    if re.fullmatch(r"\d+/\d+", bare):
        return Fraction(bare)
    return a


# ------------------------------------------------------------------
#  One rule per question shape. Each returns what the answer SHOULD be,
#  in canon()'s vocabulary, or raises to say the shape did not match.
# ------------------------------------------------------------------
PURE = re.compile(r"^[\d\s+\-*/().^]+$")


def expr(q: str):
    """The arithmetic shapes -- sums, products, brackets, powers, decimals --
    evaluated over the rationals, so `\\div` is exact division rather than a
    float and `1{,}5` is three halves rather than the nearest double."""
    e = (q.replace("$", "").replace("\\,", "")
          .replace("\\times", "*").replace("\\div", "/"))
    e = re.sub(r"\{,\}", ".", e)
    e = re.sub(r"\^\{?(\d+)\}?", r"**\1", e)
    if not PURE.fullmatch(e.strip()):
        raise ValueError
    e = re.sub(r"(\d+\.\d+|\d+)", r"Fraction('\1')", e)
    return eval(e, {"Fraction": Fraction, "__builtins__": {}})


def rule(pattern):
    def deco(fn):
        RULES.append((re.compile(pattern), fn))
        return fn
    return deco


RULES: list = []


@rule(r"^\$(\d+)\\%\$ z \$([\d\\,]+)\$$")
def _procent(m):
    return n(m[2]) * int(m[1]) / 100


@rule(r"^\$(\d+)/(\d+)\$ z \$([\d\\,]+)\$$")
def _czesc(m):
    return n(m[3]) * Fraction(int(m[1]), int(m[2]))


@rule(r"^reszta z \$([\d\\,]+) \\div (\d+)\$$")
def _reszta(m):
    return Fraction(int(n(m[1])) % int(m[2]))


@rule(r"^\$([\d\\,]+) \\div (\d+)\$ \(całość i reszta\)$")
def _reszta2(m):
    a, b = int(n(m[1])), int(m[2])
    return f"{a // b} r. {a % b}"


@rule(r"^pierwiastek z \$([\d\\,]+)\$$")
def _pierwiastek(m):
    v = int(n(m[1]))
    root = isqrt(v)
    if root * root != v:
        raise ValueError(f"{v} nie jest kwadratem")
    return Fraction(root)


@rule(r"^podw\\'\{o\}j \$([\d\\,]+)\$$")
def _podwoj(m):
    return n(m[1]) * 2


@rule(r"^po\\l\{\}owa z \$([\d\\,]+)\$$")
def _polowa(m):
    return n(m[1]) / 2


@rule(r"^suma cyfr \$([\d\\,]+)\$$")
def _suma_cyfr(m):
    return Fraction(sum(int(c) for c in m[1].replace("\\,", "")))


@rule(r"^od (\d+):(\d+) do (\d+):(\d+)$")
def _czas(m):
    a = int(m[1]) * 60 + int(m[2])
    b = int(m[3]) * 60 + int(m[4])
    return Fraction(b - a)


@rule(r"^czy \$([\d\\,]+)\$ dzieli się przez \$(\d+)\$\?$")
def _podzielnosc(m):
    return "tak" if int(n(m[1])) % int(m[2]) == 0 else "nie"


@rule(r"^\$([\d\\,]+)\$ to ile \\% z \$([\d\\,]+)\$$")
def _procent_ile(m):
    return f"{int(n(m[1]) * 100 / n(m[2]))}\\%"


@rule(r"^\$(\d+)\\%\$ liczby to \$([\d\\,]+)\$$")
def _procent_bazy(m):
    return n(m[2]) * 100 / int(m[1])


@rule(r"^\$([\d\\,]+)\$ w (górę|dół) o \$(\d+)\\%\$$")
def _podwyzka(m):
    base, p = n(m[1]), int(m[3])
    d = base * p / 100
    return base + d if m[2] == "górę" else base - d


@rule(r"^średnia z \$(\d+)\$(?:, \$(\d+)\$)+$")
def _srednia(m):
    xs = [int(x) for x in re.findall(r"\$(\d+)\$", m.string)]
    return Fraction(sum(xs), len(xs))


@rule(r"^NWD\$\((\d+), (\d+)\)\$$")
def _nwd(m):
    return Fraction(gcd(int(m[1]), int(m[2])))


@rule(r"^NWW\$\((\d+), (\d+)\)\$$")
def _nww(m):
    a, b = int(m[1]), int(m[2])
    return Fraction(a * b // gcd(a, b))


@rule(r"^\$([\d\\,]+)\$ (\w+) \$\\rightarrow\$ (\w+)$")
def _jednostki(m):
    v, src, dst = n(m[1]), m[2], m[3]
    if (src, dst) in UNIT_K:
        return v * UNIT_K[(src, dst)]
    if (dst, src) in UNIT_K:
        return v / UNIT_K[(dst, src)]
    raise ValueError(f"nieznana para jednostek {src}->{dst}")


@rule(r"^\$([\d\\,]+)\$ do (dziesiątek|setek|tysięcy)$")
def _zaokraglanie(m):
    place = {"dziesiątek": 10, "setek": 100, "tysięcy": 1000}[m[2]]
    v = int(n(m[1]))
    lo = (v // place) * place
    return Fraction(lo if v - lo < place / 2 else lo + place)


@rule(r"^\$x \+ (\d+) = ([\d\\,]+)\$$")
def _rown_plus(m):
    return n(m[2]) - int(m[1])


@rule(r"^\$x - (\d+) = ([\d\\,]+)\$$")
def _rown_minus(m):
    return n(m[2]) + int(m[1])


@rule(r"^\$(\d+)x = ([\d\\,]+)\$$")
def _rown_razy(m):
    return n(m[2]) / int(m[1])


@rule(r"^\$x \\div (\d+) = ([\d\\,]+)\$$")
def _rown_dziel(m):
    return n(m[2]) * int(m[1])


@rule(r"^\$(\d+)\$ rzymskimi$")
def _na_rzymskie(m):
    return to_roman(int(m[1]))


@rule(r"^[IVXLCDM]+$")
def _z_rzymskich(m):
    return Fraction(from_roman(m.string))


@rule(r"^\$([\d\\,]+(?:, [\d\\,]+)+), \\ldots\$$")
def _ciag(m):
    """A sequence is the one shape whose answer is not a computation but an
    inference, so the check is different in kind: try every rule the builder
    can produce and require that exactly the printed continuation follows from
    one of them. A term that fits none of them is a defect whatever it is."""
    xs = [int(n(x)) for x in m[1].split(", ")]
    d = [b - a for a, b in zip(xs, xs[1:])]
    cands = set()
    if len(set(d)) == 1:                                    # arithmetic
        cands.add(xs[-1] + d[0])
    if all(a and b % a == 0 for a, b in zip(xs, xs[1:])) \
            and len({b // a for a, b in zip(xs, xs[1:])}) == 1:
        cands.add(xs[-1] * (xs[1] // xs[0]))                # geometric
    roots = [isqrt(x) for x in xs]
    if all(r * r == x for r, x in zip(roots, xs)) and len(set(d)) > 1:
        if len({b - a for a, b in zip(roots, roots[1:])}) == 1:
            cands.add((roots[-1] + roots[1] - roots[0]) ** 2)   # squares
    if len(xs) > 2 and all(xs[i] == xs[i - 1] + xs[i - 2] for i in range(2, len(xs))):
        cands.add(xs[-1] + xs[-2])                          # Fibonacci-like
    if len({b - a for a, b in zip(d, d[1:])}) == 1:         # second difference
        cands.add(xs[-1] + d[-1] + (d[1] - d[0]))
    if not cands:
        raise ValueError("żadna reguła nie pasuje do ciągu")
    return cands


def expected(q: str):
    for pat, fn in RULES:
        m = pat.match(q)
        if m:
            return fn(m)
    return expr(q)          # raises ValueError if it is not arithmetic either


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--list", action="store_true",
                   help="print one worked example per shape and stop")
    a = p.parse_args()

    checked, bad, unknown = 0, [], Counter()
    shown = {}
    for f in sorted(GEN.glob("*.tex")):
        if f.name.startswith("_"):
            continue
        text = f.read_text(encoding="utf8")
        for q, ans in re.findall(r"\\zz?\{(.*?)\}\{(.*?)\}\n", text):
            try:
                want = expected(q)
            except Exception:
                unknown[re.sub(r"[\d\\,.]+", "#", q)[:44]] += 1
                continue
            checked += 1
            got = canon(ans)
            ok = (got in want) if isinstance(want, set) else (got == want)
            if not ok:
                # A negative answer written `-8` is a hyphen in the text-mode
                # appendix, not a minus, so it never parses as a number here.
                # Naming that separately matters: the mismatch it produces
                # otherwise reads as arithmetic ("printed -8, computed -8").
                if isinstance(got, str) and re.fullmatch(r"-[\d\\,]+", got):
                    bad.append(f"{f.name}: {q}  ->  ujemna odpowiedź {ans!r} "
                               f"zapisana dywizem; ma być $-n$ (użyj sgn())")
                else:
                    bad.append(f"{f.name}: {q}  ->  wydrukowano {ans!r}, "
                               f"wyliczono {want}")
            shown.setdefault(re.sub(r"[\d\\,.]+", "#", q)[:44], (q, ans))

    if a.list:
        for k, (q, ans) in sorted(shown.items()):
            print(f"  {q:<44} -> {ans}")
        return 0

    for b in bad[:20]:
        print(f"  BŁĄD  {b}")
    if unknown:
        print("  Kształty, których ten checker nie zna -- naucz go ich:")
        for k, c in unknown.most_common():
            print(f"      {c:>5}  {k}")

    print(f"  {checked} odpowiedzi przeliczonych niezależnie, "
          f"{len(bad)} błędnych, {sum(unknown.values())} nierozpoznanych")
    return 1 if bad or unknown else 0


if __name__ == "__main__":
    sys.exit(main())
