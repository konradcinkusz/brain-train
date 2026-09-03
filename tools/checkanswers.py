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
from datetime import date
from math import comb, factorial, gcd, isqrt
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# EVERY volume's generated tree, found rather than listed. A second book whose
# answers nobody re-computes is a second book with no gate on it, and the
# failure would be silent -- the check would go on printing a green line about
# the volume it does know. `book/sets*/generated` picks up a volume the day it
# is added, which is the only arrangement in which forgetting is impossible.
GEN_DIRS = sorted((ROOT / "book").glob("sets*/generated"))

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
ADV_WEEKDAYS = ["poniedziałek", "wtorek", "środa", "czwartek", "piątek",
                "sobota", "niedziela"]


def _factor(v: int):
    out, d = [], 2
    while d * d <= v:
        e = 0
        while v % d == 0:
            v //= d
            e += 1
        if e:
            out.append((d, e))
        d += 1
    if v > 1:
        out.append((v, 1))
    return out


def _dec_str(f: Fraction) -> str:
    """The same digit-by-digit rendering the advanced generator uses. Written
    out again here on purpose: a shared helper would make the two agree by
    construction, which is exactly what this checker exists NOT to do."""
    whole, rest = divmod(f.numerator, f.denominator)
    if rest == 0:
        return str(whole)
    digits = ""
    for _ in range(12):
        rest *= 10
        d, rest = divmod(rest, f.denominator)
        digits += str(d)
        if rest == 0:
            return f"{whole},{digits}"
    raise ValueError("rozwinięcie nie kończy się")


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


@rule(r"^NWD\$\(([\d\\,]+), ([\d\\,]+)\)\$$")
def _nwd(m):
    return Fraction(gcd(int(n(m[1])), int(n(m[2]))))


@rule(r"^NWW\$\(([\d\\,]+), ([\d\\,]+)\)\$$")
def _nww(m):
    a, b = int(n(m[1])), int(n(m[2]))
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


@rule(r"^\$(\d+) : (\d+) = ([\d\\,]+) : \?\$$")
def _proporcja(m):
    a, b, c = int(m[1]), int(m[2]), n(m[3])
    return b * c / a


SQ_K = {("m^2", "cm^2"): 10000, ("km^2", "m^2"): 1000000,
        ("ha", "m^2"): 10000, ("cm^2", "mm^2"): 100}


@rule(r"^pierwiastek sześcienny z \$([\d\\,]+)\$$")
def _szescienny(m):
    v = int(n(m[1]))
    root = round(v ** (1 / 3))
    for c in (root - 1, root, root + 1):      # cube root by float is off by
        if c ** 3 == v:                       # one near the boundaries
            return Fraction(c)
    raise ValueError(f"{v} nie jest sześcianem")


@rule(r"^\$(\d+)\$ h \$(\d+)\$ min \$\+\$ \$(\d+)\$ h \$(\d+)\$ min$")
def _czas_suma(m):
    t = int(m[1]) * 60 + int(m[2]) + int(m[3]) * 60 + int(m[4])
    return f"{t // 60} h {t % 60} min"


@rule(r"^\$(\d+)\$ z wagą \$(\d+)\$, \$(\d+)\$ z wagą \$(\d+)\$$")
def _wazona(m):
    v1, w1, v2, w2 = (int(x) for x in m.groups())
    return Fraction(v1 * w1 + v2 * w2, w1 + w2)


@rule(r"^\$([\d\\,]+) \\rightarrow ([\d\\,]+)\$$")
def _zmiana(m):
    a, b = n(m[1]), n(m[2])
    return f"{int(abs(b - a) * 100 / a)}\\%"


@rule(r"^\$(\d+)x ([+-]) (\d+) = (-?[\d\\,]+)\$$")
def _rown2(m):
    a, sign, b, c = int(m[1]), m[2], int(m[3]), n(m[4])
    return (c - b if sign == "+" else c + b) / a


@rule(r"^\$([\d\\,]+)\$ \$([+-])(\d+)\\%\$ \$([+-])(\d+)\\%\$$")
def _skladany(m):
    v = n(m[1])
    for sign, p in ((m[2], int(m[3])), (m[4], int(m[5]))):
        v = v * (100 + p if sign == "+" else 100 - p) / 100
    return v


@rule(r"^\$([\d\\,]+)\$ \$([a-z^0-9]+)\$ \$\\rightarrow\$ \$([a-z^0-9]+)\$$")
def _jedn_kw(m):
    v, src, dst = n(m[1]), m[2], m[3]
    if (src, dst) in SQ_K:
        return v * SQ_K[(src, dst)]
    if (dst, src) in SQ_K:
        return v / SQ_K[(dst, src)]
    raise ValueError(f"nieznana para jednostek {src}->{dst}")


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




# ------------------------------------------------------------------
#  The advanced volume's shapes.
# ------------------------------------------------------------------

@rule(r"^\$(\d+)/(\d+) \\div (\d+)/(\d+)\$$")
def _ulamki_dziel(m):
    """Dividing fractions needs its own rule and is the reason it has one:
    read as arithmetic, `4/5 \div 1/3` becomes `4/5/1/3`, which is 4/15 and
    not 12/5. Multiplication happens to survive that reading; division does
    not, and the generic evaluator reported forty wrong answers before this
    rule existed."""
    return Fraction(int(m[1]), int(m[2])) / Fraction(int(m[3]), int(m[4]))


@rule(r"^\$(\d+)/(\d+) \\times (\d+)/(\d+)\$$")
def _ulamki_razy(m):
    return Fraction(int(m[1]), int(m[2])) * Fraction(int(m[3]), int(m[4]))


@rule(r"^\$([\d\\,]+)\$ dwójkowo$")
def _na_dwojkowy(m):
    return f"{int(n(m[1])):b}"


@rule(r"^\$([01]+)_2\$$")
def _z_dwojkowego(m):
    return Fraction(int(m[1], 2))


@rule(r"^\$([01]+)_2 \+ ([01]+)_2\$$")
def _binarna_suma(m):
    return f"{int(m[1], 2) + int(m[2], 2):b}"


@rule(r"^\$([\d\\,]+)\$ szesnastkowo$")
def _na_hex(m):
    return f"{int(n(m[1])):X}"


@rule(r"^\$\\mathrm\{([0-9A-F]+)\}_\{16\}\$$")
def _z_hex(m):
    return Fraction(int(m[1], 16))


@rule(r"^\$([\d\\,]+) \\bmod (\d+)\$$")
def _modulo(m):
    return Fraction(int(n(m[1])) % int(m[2]))


@rule(r"^\$(\d+)\^\{(\d+)\} \\bmod (\d+)\$$")
def _potega_modulo(m):
    return Fraction(pow(int(m[1]), int(m[2]), int(m[3])))


@rule(r"^\$([\d\\,]+)\$ --- cyfra kontrolna$")
def _cyfra(m):
    v = int(n(m[1]))
    return Fraction(1 + (v - 1) % 9)


@rule(r"^\$([\d\\,]+)\$ na czynniki$")
def _rozklad(m):
    parts = [f"{p}^{{{e}}}" if e > 1 else f"{p}" for p, e in _factor(int(n(m[1])))]
    return "$" + r" \cdot ".join(parts) + "$"


@rule(r"^ile dzielników ma \$([\d\\,]+)\$$")
def _dzielniki(m):
    d = 1
    for _, e in _factor(int(n(m[1]))):
        d *= e + 1
    return Fraction(d)


@rule(r"^czy \$([\d\\,]+)\$ jest pierwsza\?$")
def _pierwsza(m):
    v = int(n(m[1]))
    return "tak" if v > 1 and all(v % k for k in range(2, isqrt(v) + 1)) else "nie"


@rule(r"^pierwsza liczba pierwsza po \$([\d\\,]+)\$$")
def _nastepna(m):
    v = int(n(m[1])) + 1
    while any(v % k == 0 for k in range(2, isqrt(v) + 1)):
        v += 1
    return Fraction(v)


@rule(r"^czy \$([\d\\,]+)\$ jest kwadratem\?$")
def _kwadrat(m):
    v = int(n(m[1]))
    return "tak" if isqrt(v) ** 2 == v else "nie"


@rule(r"^\$1 \+ 2 \+ \\ldots \+ (\d+)\$$")
def _suma_kolejnych(m):
    k = int(m[1])
    return Fraction(k * (k + 1) // 2)


@rule(r"^\$1 \+ 3 \+ \\ldots \+ (\d+)\$$")
def _suma_nieparzystych(m):
    k = (int(m[1]) + 1) // 2
    return Fraction(k * k)


@rule(r"^\$2 \+ 4 \+ \\ldots \+ (\d+)\$$")
def _suma_parzystych(m):
    k = int(m[1]) // 2
    return Fraction(k * (k + 1))


@rule(r"^\$(\d+)\^\{-(\d+)\}\$$")
def _potega_ujemna(m):
    return Fraction(1, int(m[1]) ** int(m[2]))


@rule(r"^\$(\d+)\^\{0\}\$$")
def _potega_zero(m):
    return Fraction(1)


@rule(r"^\$([\d\\,]+)\^\{(\d+)/(\d+)\}\$$")
def _potega_ulamkowa(m):
    base, p, root = int(n(m[1])), int(m[2]), int(m[3])
    b = round(base ** (1 / root))
    for c in (b - 1, b, b + 1):
        if c ** root == base:
            return Fraction(c ** p)
    raise ValueError(f"{base} nie jest {root}-tą potęgą")


@rule(r"^\$\\log_\{(\d+)\} ([\d\\,]+)\$$")
def _log(m):
    b, v, e = int(m[1]), int(n(m[2])), 0
    while v > 1:
        if v % b:
            raise ValueError(f"{v} nie jest potęgą {b}")
        v //= b
        e += 1
    return Fraction(e)


@rule(r"^\$(\d+) \\cdot 10\^\{(\d+)\} \\times (\d+) \\cdot 10\^\{(\d+)\}\$$")
def _notacja(m):
    prod, e = int(m[1]) * int(m[3]), int(m[2]) + int(m[4])
    if prod < 10:
        mant = str(prod)
    elif prod % 10 == 0:
        mant, e = str(prod // 10), e + 1
    else:
        mant, e = f"{prod // 10}{{,}}{prod % 10}", e + 1
    return f"${mant} \\cdot 10^{{{e}}}$"


@rule(r"^\$(\d+)/(\d+)\$ na procent$")
def _na_procent(m):
    return _dec_str(Fraction(int(m[1]) * 100, int(m[2]))) + "\\%"


@rule(r"^\$(\d+)/(\d+)\$ dziesiętnie$")
def _na_dziesietny(m):
    return _dec_str(Fraction(int(m[1]), int(m[2])))


@rule(r"^\$(\d+)!\$$")
def _silnia(m):
    return Fraction(factorial(int(m[1])))


@rule(r"^\$C\((\d+), (\d+)\)\$$")
def _kombinacje(m):
    return Fraction(comb(int(m[1]), int(m[2])))


@rule(r"^\$P\((\d+), (\d+)\)\$$")
def _wariacje(m):
    a, b = int(m[1]), int(m[2])
    return Fraction(factorial(a) // factorial(a - b))


@rule(r"^(\d+)\.(\d+)\.(\d+) --- jaki dzień tygodnia$")
def _kalendarz(m):
    return ADV_WEEKDAYS[date(int(m[3]), int(m[2]), int(m[1])).weekday()]


@rule(r"^\$([\d\\,]+)\$ km w (.+) --- km/h$")
def _predkosc(m):
    """The time reads `2 h`, `45 min` or `1 h 15 min`, so it is captured whole
    and taken apart here rather than spelt as three near-identical patterns."""
    h = re.search(r"\$(\d+)\$ h", m[2])
    mi = re.search(r"\$(\d+)\$ min", m[2])
    mins = (int(h[1]) if h else 0) * 60 + (int(mi[1]) if mi else 0)
    if not mins:
        raise ValueError(f"nie umiem odczytać czasu z {m[2]!r}")
    return n(m[1]) * 60 / mins


@rule(r"^\$([\d,]+)\$ km/h \$\\rightarrow\$ m/s$")
def _kmh(m):
    return _dec_str(Fraction(int(m[1]) * 10, 36))


@rule(r"^\$([\d,]+)\$ m/s \$\\rightarrow\$ km/h$")
def _ms(m):
    return n(m[1]) * Fraction(36, 10)


@rule(r"^tam \$(\d+)\$ km/h, z powrotem \$(\d+)\$ km/h --- średnia$")
def _harmoniczna(m):
    a, b = int(m[1]), int(m[2])
    return Fraction(2 * a * b, a + b)


@rule(r"^\$([\d\\,]+)\$ przy \$(\d+)\\%\$ przez \$(\d+)\$ lata$")
def _procent_lata(m):
    v, p = int(n(m[1])), int(m[2])
    for _ in range(int(m[3])):
        v = v * (100 + p) // 100
    return Fraction(v)


@rule(r"^skala \$1:([\d\\,]+)\$, \$(\d+)\$ cm --- ile km$")
def _skala(m):
    return _dec_str(Fraction(int(m[2]) * int(n(m[1])) // 100, 1000))


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
    files = [f for d in GEN_DIRS for f in sorted(d.glob("*.tex"))
             if not f.name.startswith("_")]
    if not files:
        print("  Nie znaleziono żadnego wygenerowanego zestawu -- "
              "uruchom `make sets`")
        return 1
    for f in files:
        text = f.read_text(encoding="utf8")
        for q, ans in re.findall(r"\\zz?\{(.*?)\}\{(.*?)\}\n", text):
            try:
                want = expected(q)
            except Exception:
                unknown[re.sub(r"[\d\\,.]+", "#", q)[:44]] += 1
                continue
            checked += 1
            got = canon(ans)
            # A rule returning a STRING means the answer is that literal text
            # -- a binary expansion, a factorisation, a weekday. Those must be
            # compared against what was printed rather than against canon()'s
            # reading of it: `11101111` is a perfectly good decimal number and
            # canon() dutifully parsed it as one, so every binary answer in the
            # volume compared unequal to itself.
            if isinstance(want, set):
                ok = got in want
            elif isinstance(want, str):
                ok = ans.strip() == want
            else:
                ok = got == want
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

    where = ", ".join(d.parent.name for d in GEN_DIRS)
    print(f"  {checked} odpowiedzi przeliczonych niezależnie ({where}), "
          f"{len(bad)} błędnych, {sum(unknown.values())} nierozpoznanych")
    return 1 if bad or unknown else 0


if __name__ == "__main__":
    sys.exit(main())
