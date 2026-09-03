#!/usr/bin/env python3
"""Generate the ADVANCED volume's drill sets.

WHAT MAKES IT ADVANCED, AND WHAT DELIBERATELY DOES NOT. Not bigger numbers.
The basic volume already ends on five-digit addition, three-by-two
multiplication and compound percentages; another digit on the end of those is
a longer sum, not a harder one, and ninety sets of it would be the same book
printed twice.

This volume asks for operations the basic one does not contain at all --
positional systems, modular arithmetic, the structure of a number, fractions
multiplied rather than added, exponents that are negative or fractional,
logarithms, and the handful of applied calculations where the intuitive answer
is reliably wrong. The rules of the game are unchanged: forty exercises, in the
head, against a stopwatch, every answer in one appendix at the back.

    tools/gen_sets_adv.py            # write book/sets-adv/generated/
    tools/gen_sets_adv.py --check    # fail if the tree is stale

The machinery, the page format and every builder the basic volume already has
are imported from gen_sets.py rather than copied. What is here is this
volume's own builders and its own list of sets.
"""
from __future__ import annotations

import argparse
import sys
from datetime import date
from fractions import Fraction
from math import comb, factorial, gcd, isqrt
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gen_sets import (  # noqa: E402
    BASIC, HAND_CHAPTER, Hand, N, Set, Volume, build, dec, dect, distinct,
    dzielenie, fmt, frac_txt, mieszane, mnozenie, sgn,
)

# ------------------------------------------------------------------
#  Blok I -- Systemy i reszty
# ------------------------------------------------------------------

def _bin(n: int) -> str:
    return f"{n:b}"


def dwojkowy(r):
    """Both directions. Eight bits is the ceiling on purpose: past that the
    exercise is transcription rather than conversion, which is the same reason
    the basic volume caps its roman numerals at eight letters."""
    n = r.randint(5, 255)
    if r.random() < 0.5:
        return f"${fmt(n)}$ dwójkowo", _bin(n)
    return f"${_bin(n)}_2$", fmt(n)


def szesnastkowy(r):
    n = r.randint(16, 255)
    if r.random() < 0.5:
        return f"${fmt(n)}$ szesnastkowo", f"{n:X}"
    return f"$\\mathrm{{{n:X}}}_{{16}}$", fmt(n)


def binarne_sumy(r):
    """Added in binary and answered in binary. Converting to decimal and back
    gets the right answer and a worse time, which is the point -- carrying at
    two is a different motion from carrying at ten."""
    a, b = r.randint(3, 60), r.randint(3, 60)
    return f"${_bin(a)}_2 + {_bin(b)}_2$", _bin(a + b)


def modulo(r):
    m = r.choice([3, 4, 6, 7, 8, 9, 11, 12, 13])
    a = r.randint(50, 999)
    return rf"${fmt(a)} \bmod {m}$", fmt(a % m)


def potega_modulo(r):
    """Small exponents and small moduli, because the method is repeated
    squaring in the head and not a calculator. `3^5 mod 7` is two squarings
    and a multiply."""
    b = r.randint(2, 9)
    e = r.randint(2, 6)
    m = r.choice([5, 7, 9, 11, 13])
    return rf"${b}^{{{e}}} \bmod {m}$", fmt(pow(b, e, m))


def cyfra_kontrolna(r):
    """The digital root -- add the digits, and the digits of that, until one
    is left. It is the number modulo nine, which is what makes casting out
    nines a check on a whole multiplication."""
    n = r.randint(1000, 999999)
    return f"${fmt(n)}$ --- cyfra kontrolna", fmt(1 + (n - 1) % 9)


def podzielnosc_trudna(r):
    """Seven, eleven, thirteen, seventeen -- the divisors whose rules the
    basic volume leaves out because they are not a digit sum. Half the draws
    are built divisible, for the reason that volume records: left to chance a
    divisor of seventeen answers `nie` sixteen times out of seventeen, and a
    reader who noticed would score well without applying anything."""
    d = r.choice([7, 11, 13, 17])
    n = d * r.randint(20, 700) if r.random() < 0.5 else r.randint(200, 9999)
    return (f"czy ${fmt(n)}$ dzieli się przez ${d}$?",
            "tak" if n % d == 0 else "nie")


# ------------------------------------------------------------------
#  Blok II -- Struktura liczby
# ------------------------------------------------------------------

def _factor(n: int) -> list[tuple[int, int]]:
    out, d = [], 2
    while d * d <= n:
        e = 0
        while n % d == 0:
            n //= d
            e += 1
        if e:
            out.append((d, e))
        d += 1
    if n > 1:
        out.append((n, 1))
    return out


def rozklad(r):
    """Prime factorisation, written the way it is written on paper: exponents
    where there are any, a centred dot between the factors."""
    n = r.randint(24, 400)
    while len(_factor(n)) < 2:
        n = r.randint(24, 400)
    parts = [f"{p}^{{{e}}}" if e > 1 else f"{p}" for p, e in _factor(n)]
    return f"${fmt(n)}$ na czynniki", "$" + r" \cdot ".join(parts) + "$"


def liczba_dzielnikow(r):
    """How many divisors, which is the product of one more than each exponent
    -- and is the reason the factorisation set comes first."""
    n = r.randint(12, 400)
    d = 1
    for _, e in _factor(n):
        d *= e + 1
    return f"ile dzielników ma ${fmt(n)}$", fmt(d)


def euklides(r):
    """Pairs too large to see the common factor in, so the algorithm is the
    only route. The basic volume's NWD sets stop where these start."""
    g = r.choice([3, 6, 7, 9, 11, 12, 13, 14, 17, 19, 21])
    a, b = g * r.randint(11, 90), g * r.randint(11, 90)
    while gcd(a // g, b // g) != 1:
        a, b = g * r.randint(11, 90), g * r.randint(11, 90)
    return f"NWD$({fmt(a)}, {fmt(b)})$", fmt(g)


def _prime(n: int) -> bool:
    return n > 1 and all(n % k for k in range(2, isqrt(n) + 1))


PRIMES = [p for p in range(53, 400) if _prime(p)]


def czy_pierwsza(r):
    """Half of the composites are a product of two primes above ten, which is
    the case that catches people: 91 looks prime and is 7 times 13."""
    if r.random() < 0.5:
        n = r.choice(PRIMES)
    else:
        n = r.choice([7, 11, 13, 17, 19, 23]) * r.choice([7, 11, 13, 17, 19])
    return f"czy ${fmt(n)}$ jest pierwsza?", "tak" if _prime(n) else "nie"


def nastepna_pierwsza(r):
    n = r.randint(20, 400)
    p = n + 1
    while not _prime(p):
        p += 1
    return f"pierwsza liczba pierwsza po ${fmt(n)}$", fmt(p)


def czy_kwadrat(r):
    """The last digit rules out six of the ten, and the magnitude brackets the
    root -- so this is two seconds of reasoning and not a search."""
    if r.random() < 0.5:
        n = r.randint(12, 99) ** 2
    else:
        n = r.randint(150, 9800)
        while isqrt(n) ** 2 == n:
            n = r.randint(150, 9800)
    return (f"czy ${fmt(n)}$ jest kwadratem?",
            "tak" if isqrt(n) ** 2 == n else "nie")


def suma_ciagu(r):
    """Closed forms rather than addition: the first n numbers, the first n odd
    numbers, the first n even numbers. A reader who adds them up gets the same
    answer and misses the whole exercise."""
    n = r.randint(6, 60)
    kind = r.randint(0, 2)
    if kind == 0:
        return (rf"$1 + 2 + \ldots + {n}$", fmt(n * (n + 1) // 2))
    if kind == 1:
        return (rf"$1 + 3 + \ldots + {2 * n - 1}$", fmt(n * n))
    return (rf"$2 + 4 + \ldots + {2 * n}$", fmt(n * (n + 1)))


# ------------------------------------------------------------------
#  Blok III -- Ułamki i potęgi
# ------------------------------------------------------------------
ADENS = (2, 3, 4, 5, 6, 8, 9, 10, 12)


def dec_str(f: Fraction) -> str:
    """A terminating fraction as a Polish decimal, computed digit by digit
    rather than through a float. A float would round, and a rounded answer in a
    scored drill is a wrong answer -- so a fraction that does NOT terminate
    raises here instead, which makes it a builder bug rather than a page the
    reader cannot reproduce."""
    whole, rest = divmod(f.numerator, f.denominator)
    if rest == 0:
        return fmt(whole)
    digits = ""
    for _ in range(12):
        rest *= 10
        d, rest = divmod(rest, f.denominator)
        digits += str(d)
        if rest == 0:
            return f"{whole},{digits}"
    raise ValueError(f"{f} nie ma skończonego rozwinięcia dziesiętnego")


def ulamki_mnozenie(r):
    d1, d2 = r.choice(ADENS), r.choice(ADENS)
    n1, n2 = r.randint(1, d1 - 1), r.randint(1, d2 - 1)
    return (f"${n1}/{d1} \\times {n2}/{d2}$",
            frac_txt(Fraction(n1, d1) * Fraction(n2, d2)))


def ulamki_dzielenie(r):
    """Dividing by a fraction is multiplying by its reciprocal, and the answer
    being LARGER than what you started with is the thing that has to stop
    being surprising."""
    d1, d2 = r.choice(ADENS), r.choice(ADENS)
    n1, n2 = r.randint(1, d1 - 1), r.randint(1, d2 - 1)
    return (rf"${n1}/{d1} \div {n2}/{d2}$",
            frac_txt(Fraction(n1, d1) / Fraction(n2, d2)))


def potegi_ujemne(r):
    """A negative exponent is a reciprocal, not a negative number -- which is
    the single most common thing to get wrong about them."""
    b = r.randint(2, 10)
    if r.random() < 0.85:
        e = r.randint(1, 4)
        return f"${b}^{{-{e}}}$", frac_txt(Fraction(1, b ** e))
    return f"${b}^{{0}}$", "1"


def potega_ulamkowa(r):
    """A fractional exponent is a root and a power, and the reader chooses
    which to do first -- taking the root first keeps the numbers small."""
    base, root = r.choice([(4, 2), (8, 3), (9, 2), (16, 2), (16, 4),
                           (25, 2), (27, 3), (32, 5), (36, 2), (49, 2),
                           (64, 2), (64, 3), (64, 6), (81, 2), (100, 2),
                           (121, 2), (125, 3), (128, 7), (144, 2), (169, 2)])
    p = r.randint(1, 3)
    b = round(base ** (1 / root))
    while b ** root != base:
        b += 1 if b ** root < base else -1
    return f"${fmt(base)}^{{{p}/{root}}}$", fmt(b ** p)


def logarytmy(r):
    """Always with its base written. Two readerships read a bare logarithm as
    two different functions, and a drill scored on the answer cannot afford
    the ambiguity."""
    b = r.randint(2, 10)
    e = r.randint(2, 16)
    while b ** e > 100000:
        e -= 1
    return rf"$\log_{{{b}}} {fmt(b ** e)}$", fmt(e)


def notacja_naukowa(r):
    """Normalised, always -- `20 \\cdot 10^{6}` is the same number and is not
    an answer in scientific notation, so the exercise includes noticing that
    the mantissa left its range."""
    m1, m2 = r.randint(2, 9), r.randint(2, 9)
    e1, e2 = r.randint(2, 8), r.randint(2, 8)
    prod, e = m1 * m2, e1 + e2
    if prod < 10:
        mant = fmt(prod)
    elif prod % 10 == 0:
        mant, e = fmt(prod // 10), e + 1
    else:
        mant, e = f"{prod // 10}{{,}}{prod % 10}", e + 1
    return (rf"${m1} \cdot 10^{{{e1}}} \times {m2} \cdot 10^{{{e2}}}$",
            f"${mant} \\cdot 10^{{{e}}}$")


def ulamek_na_procent(r):
    """Denominators whose percentage terminates, so the answer is exact and
    the drill is the conversion rather than a rounding convention."""
    d = r.choice([2, 4, 5, 8, 10, 16, 20, 25, 40, 50])
    n = r.randint(1, d - 1)
    return f"${n}/{d}$ na procent", dec_str(Fraction(n * 100, d)) + "\\%"


def ulamek_na_dziesietny(r):
    d = r.choice([2, 4, 5, 8, 10, 20, 25, 40, 50])
    n = r.randint(1, d - 1)
    return f"${n}/{d}$ dziesiętnie", dec_str(Fraction(n, d))


def dziesietne_male(r):
    """A small decimal against a large whole number, where the point moves
    further than anybody expects."""
    # The multiplier is a multiple of the decimal's own denominator, so the
    # product is whole. Drawn freely it truncated -- `0,003 x 25` came out as
    # `0,0` -- which is a wrong answer rather than a rounded one.
    t = r.randint(2, 9)
    places = r.choice([2, 3])
    z = 10 ** places
    k = z * r.randint(2, 20)
    lead = "0{,}0" + ("0" if places == 3 else "")
    return rf"${lead}{t} \times {fmt(k)}$", fmt(t * k // z)


# ------------------------------------------------------------------
#  Blok IV -- Zastosowania
# ------------------------------------------------------------------

def kombinatoryka(r):
    """Three shapes under one heading: a factorial, a choice and an ordered
    choice. Factorials alone are eight distinct exercises between 3! and 10!,
    which is not a set -- and the three belong together anyway, because
    telling them apart is most of what the block is for."""
    kind = r.randint(0, 2)
    if kind == 0:
        n = r.randint(3, 10)
        return f"${n}!$", fmt(factorial(n))
    n = r.randint(4, 14)
    k = r.randint(2, min(5, n - 1))
    if kind == 1:
        return f"$C({n}, {k})$", fmt(comb(n, k))
    return f"$P({n}, {k})$", fmt(factorial(n) // factorial(n - k))


WEEKDAYS = ["poniedziałek", "wtorek", "środa", "czwartek", "piątek",
            "sobota", "niedziela"]


def dzien_tygodnia(r):
    """The day of the week from a date. Computed with the calendar rather than
    with a remembered rule, because the rule is what the reader is being asked
    to acquire and the book may not get it wrong while asking."""
    d = date(r.randint(2000, 2049), r.randint(1, 12), r.randint(1, 28))
    return (f"{d.day}.{d.month:02d}.{d.year} --- jaki dzień tygodnia",
            WEEKDAYS[d.weekday()])


def predkosc(r):
    """Distance over time, where the time is not a whole number of hours --
    which is the only part of this that is ever difficult."""
    v = r.choice([40, 45, 50, 60, 70, 75, 80, 90, 100, 120])
    mins = r.choice([30, 45, 75, 90, 105, 120, 135, 150])
    while (v * mins) % 60:      # both redrawn: fixing v and hunting for a
        v = r.choice([40, 45, 50, 60, 70, 75, 80, 90, 100, 120])
        mins = r.choice([30, 45, 75, 90, 105, 120, 135, 150])
    h, m = mins // 60, mins % 60
    czas = f"${h}$ h ${m}$ min" if h and m else (f"${h}$ h" if h else f"${m}$ min")
    return (f"${fmt(v * mins // 60)}$ km w {czas} --- km/h", fmt(v))


def kmh_ms(r):
    """Divide by 3.6, which is the conversion everybody looks up. The speeds
    are multiples of eighteen so the answer stays whole."""
    # Multiples of NINE, not eighteen: eighteen gives only a dozen speeds and
    # distinct() cannot fill a set of forty from them. Nine leaves the m/s side
    # on a half, which is exact and is what the conversion actually looks like.
    v = 9 * r.randint(2, 24)
    ms = Fraction(v * 10, 36)
    if r.random() < 0.5:
        return rf"${v}$ km/h $\rightarrow$ m/s", dec_str(ms)
    return rf"${dec_str(ms)}$ m/s $\rightarrow$ km/h", fmt(v)


HSPEEDS = (20, 24, 30, 36, 40, 45, 48, 50, 60, 72, 75, 80, 90, 96,
           100, 120, 144, 150, 180, 200, 240)


def srednia_harmoniczna(r):
    """There and back at two speeds. The average is NOT the mean of the two --
    more of the journey is spent at the slower one -- and this is the trap the
    whole block is built around."""
    while True:
        a, b = r.choice(HSPEEDS), r.choice(HSPEEDS)
        if a != b and (2 * a * b) % (a + b) == 0:
            return (f"tam ${a}$ km/h, z powrotem ${b}$ km/h --- średnia",
                    fmt(2 * a * b // (a + b)))


def procent_lata(r):
    """Compound growth over a small number of years, where the naive answer
    multiplies the rate by the years."""
    base = r.choice([1000, 2000, 4000, 5000, 8000, 10000])
    p = r.choice([10, 20, 25, 50])
    yrs = r.randint(2, 3)
    v = base
    for _ in range(yrs):
        v = v * (100 + p) // 100
    return (rf"${fmt(base)}$ przy ${p}\%$ przez ${yrs}$ lata", fmt(v))


def skala(r):
    """A map scale, which is a ratio doing a unit conversion at the same time
    -- and the centimetre-to-kilometre step is where it goes wrong."""
    s = r.choice([10000, 25000, 50000, 100000, 200000])
    cm = r.randint(2, 12)
    metres = cm * s // 100
    return (f"skala $1:{fmt(s)}$, ${cm}$ cm --- ile km",
            dec_str(Fraction(metres, 1000)))


# ------------------------------------------------------------------
#  The sets. Four blocks, and the ladder inside this volume is not the basic
#  one continued -- it is four different subjects, ordered so that each rests
#  on the one before: you need remainders before you need factorisation, and
#  factorisation before fractional exponents mean anything.
#
#  SEEDS 2001 UPWARDS ARE THIS VOLUME'S. The basic book holds 1001--1025 and
#  1101--1225, and the gap is deliberate: audit() refuses a seed the other
#  volume already uses, because two books printing the same forty exercises is
#  a wasted page nobody would ever notice.
# ------------------------------------------------------------------
ADV_SETS = [

    # --- Blok I --- Systemy i reszty ------------------------------
    Set("01-dwojkowy", "System dwójkowy", 1, 2, 10, 3, 2001, "dwojkowy",
        lambda r: distinct(N, lambda: dwojkowy(r))),
    Set("02-modulo", "Reszta modulo", 1, 2, 8, 3, 2002, "modulo",
        lambda r: distinct(N, lambda: modulo(r))),
    Set("03-szesnastkowy", "System szesnastkowy", 1, 2, 10, 3, 2003, "szesnastkowy",
        lambda r: distinct(N, lambda: szesnastkowy(r))),
    Set("04-cyfra", "Cyfra kontrolna", 1, 2, 7, 2, 2004, "cyfra",
        lambda r: distinct(N, lambda: cyfra_kontrolna(r))),
    Set("05-podzielnosc", "Podzielność przez 7, 11, 13", 1, 2, 9, 2, 2005, "podzielnosc",
        lambda r: distinct(N, lambda: podzielnosc_trudna(r)), True),
    Set("06-binarne", "Dodawanie dwójkowe", 1, 2, 11, 2, 2006, "binarne",
        lambda r: distinct(N, lambda: binarne_sumy(r))),
    Set("07-potega-modulo", "Potęga modulo", 1, 2, 12, 3, 2007, "potega-modulo",
        lambda r: distinct(N, lambda: potega_modulo(r))),
    Set("08-dwojkowy-b", "System dwójkowy II", 1, 2, 10, 3, 2008, "dwojkowy",
        lambda r: distinct(N, lambda: dwojkowy(r))),
    Set("09-modulo-b", "Reszta modulo II", 1, 2, 8, 3, 2009, "modulo",
        lambda r: distinct(N, lambda: modulo(r))),
    Set("10-szesnastkowy-b", "System szesnastkowy II", 1, 2, 10, 3, 2010, "szesnastkowy",
        lambda r: distinct(N, lambda: szesnastkowy(r))),
    Set("11-cyfra-b", "Cyfra kontrolna II", 1, 2, 7, 2, 2011, "cyfra",
        lambda r: distinct(N, lambda: cyfra_kontrolna(r))),
    Set("12-podzielnosc-b", "Podzielność przez 7, 11, 13 II", 1, 2, 9, 2, 2012, "podzielnosc",
        lambda r: distinct(N, lambda: podzielnosc_trudna(r)), True),
    Set("13-binarne-b", "Dodawanie dwójkowe II", 1, 2, 11, 2, 2013, "binarne",
        lambda r: distinct(N, lambda: binarne_sumy(r))),
    Set("14-potega-modulo-b", "Potęga modulo II", 1, 2, 12, 3, 2014, "potega-modulo",
        lambda r: distinct(N, lambda: potega_modulo(r))),
    Set("15-dwojkowy-c", "System dwójkowy III", 1, 2, 10, 3, 2015, "dwojkowy",
        lambda r: distinct(N, lambda: dwojkowy(r))),
    Set("16-modulo-c", "Reszta modulo III", 1, 2, 8, 3, 2016, "modulo",
        lambda r: distinct(N, lambda: modulo(r))),
    Set("17-szesnastkowy-c", "System szesnastkowy III", 1, 2, 10, 3, 2017, "szesnastkowy",
        lambda r: distinct(N, lambda: szesnastkowy(r))),
    Set("18-cyfra-c", "Cyfra kontrolna III", 1, 2, 7, 2, 2018, "cyfra",
        lambda r: distinct(N, lambda: cyfra_kontrolna(r))),
    Set("19-mix1", "Mieszane — systemy", 1, 2, 10, 3, 2019, "mieszane",
        lambda r: mieszane(r, [
            lambda: dwojkowy(r),
            lambda: szesnastkowy(r),
            lambda: modulo(r),
            lambda: cyfra_kontrolna(r),
        ])),
    Set("20-podzielnosc-c", "Podzielność przez 7, 11, 13 III", 1, 2, 9, 2, 2020, "podzielnosc",
        lambda r: distinct(N, lambda: podzielnosc_trudna(r)), True),
    Set("21-binarne-c", "Dodawanie dwójkowe III", 1, 2, 11, 2, 2021, "binarne",
        lambda r: distinct(N, lambda: binarne_sumy(r))),
    Set("22-potega-modulo-c", "Potęga modulo III", 1, 2, 12, 3, 2022, "potega-modulo",
        lambda r: distinct(N, lambda: potega_modulo(r))),
    Set("23-dwojkowy-d", "System dwójkowy IV", 1, 2, 10, 3, 2023, "dwojkowy",
        lambda r: distinct(N, lambda: dwojkowy(r))),
    Set("24-modulo-d", "Reszta modulo IV", 1, 2, 8, 3, 2024, "modulo",
        lambda r: distinct(N, lambda: modulo(r))),

    # --- Blok II --- Struktura liczby ------------------------------
    Set("25-rozklad", "Rozkład na czynniki", 2, 2, 12, 3, 2025, "rozklad",
        lambda r: distinct(N, lambda: rozklad(r))),
    Set("26-pierwsza", "Czy pierwsza", 2, 2, 10, 2, 2026, "pierwsza",
        lambda r: distinct(N, lambda: czy_pierwsza(r))),
    Set("27-euklides", "Algorytm Euklidesa", 2, 2, 13, 3, 2027, "euklides",
        lambda r: distinct(N, lambda: euklides(r))),
    Set("28-kwadrat", "Czy kwadrat", 2, 2, 9, 2, 2028, "kwadrat",
        lambda r: distinct(N, lambda: czy_kwadrat(r))),
    Set("29-suma-ciagu", "Sumy ciągów", 2, 2, 9, 3, 2029, "suma-ciagu",
        lambda r: distinct(N, lambda: suma_ciagu(r))),
    Set("30-dzielniki", "Ile dzielników", 2, 2, 11, 2, 2030, "dzielniki",
        lambda r: distinct(N, lambda: liczba_dzielnikow(r))),
    Set("31-nastepna", "Następna pierwsza", 2, 2, 11, 2, 2031, "nastepna",
        lambda r: distinct(N, lambda: nastepna_pierwsza(r)), True),
    Set("32-rozklad-b", "Rozkład na czynniki II", 2, 2, 12, 3, 2032, "rozklad",
        lambda r: distinct(N, lambda: rozklad(r))),
    Set("33-pierwsza-b", "Czy pierwsza II", 2, 2, 10, 2, 2033, "pierwsza",
        lambda r: distinct(N, lambda: czy_pierwsza(r))),
    Set("34-euklides-b", "Algorytm Euklidesa II", 2, 2, 13, 3, 2034, "euklides",
        lambda r: distinct(N, lambda: euklides(r))),
    Set("35-kwadrat-b", "Czy kwadrat II", 2, 2, 9, 2, 2035, "kwadrat",
        lambda r: distinct(N, lambda: czy_kwadrat(r))),
    Set("36-suma-ciagu-b", "Sumy ciągów II", 2, 2, 9, 3, 2036, "suma-ciagu",
        lambda r: distinct(N, lambda: suma_ciagu(r))),
    Set("37-dzielniki-b", "Ile dzielników II", 2, 2, 11, 2, 2037, "dzielniki",
        lambda r: distinct(N, lambda: liczba_dzielnikow(r))),
    Set("38-nastepna-b", "Następna pierwsza II", 2, 2, 11, 2, 2038, "nastepna",
        lambda r: distinct(N, lambda: nastepna_pierwsza(r)), True),
    Set("39-rozklad-c", "Rozkład na czynniki III", 2, 2, 12, 3, 2039, "rozklad",
        lambda r: distinct(N, lambda: rozklad(r))),
    Set("40-pierwsza-c", "Czy pierwsza III", 2, 2, 10, 2, 2040, "pierwsza",
        lambda r: distinct(N, lambda: czy_pierwsza(r))),
    Set("41-euklides-c", "Algorytm Euklidesa III", 2, 2, 13, 3, 2041, "euklides",
        lambda r: distinct(N, lambda: euklides(r))),
    Set("42-kwadrat-c", "Czy kwadrat III", 2, 2, 9, 2, 2042, "kwadrat",
        lambda r: distinct(N, lambda: czy_kwadrat(r))),
    Set("43-mix2", "Mieszane — struktura", 2, 2, 11, 3, 2043, "mieszane",
        lambda r: mieszane(r, [
            lambda: rozklad(r),
            lambda: liczba_dzielnikow(r),
            lambda: euklides(r),
            lambda: suma_ciagu(r),
        ])),
    Set("44-suma-ciagu-c", "Sumy ciągów III", 2, 2, 9, 3, 2044, "suma-ciagu",
        lambda r: distinct(N, lambda: suma_ciagu(r))),
    Set("45-dzielniki-c", "Ile dzielników III", 2, 2, 11, 2, 2045, "dzielniki",
        lambda r: distinct(N, lambda: liczba_dzielnikow(r))),
    Set("46-nastepna-c", "Następna pierwsza III", 2, 2, 11, 2, 2046, "nastepna",
        lambda r: distinct(N, lambda: nastepna_pierwsza(r)), True),
    Set("47-rozklad-d", "Rozkład na czynniki IV", 2, 2, 12, 3, 2047, "rozklad",
        lambda r: distinct(N, lambda: rozklad(r))),
    Set("48-pierwsza-d", "Czy pierwsza IV", 2, 2, 10, 2, 2048, "pierwsza",
        lambda r: distinct(N, lambda: czy_pierwsza(r))),

    # --- Blok III --- Ułamki i potęgi -------------------------------
    Set("49-ulamki-mnoz", "Mnożenie ułamków", 3, 3, 10, 3, 2049, "ulamki-x",
        lambda r: distinct(N, lambda: ulamki_mnozenie(r))),
    Set("50-logarytmy", "Logarytmy", 3, 3, 9, 3, 2050, "logarytmy",
        lambda r: distinct(N, lambda: logarytmy(r))),
    Set("51-potegi-ujemne", "Potęgi ujemne i zero", 3, 3, 8, 3, 2051, "potegi-ujemne",
        lambda r: distinct(N, lambda: potegi_ujemne(r))),
    Set("52-na-dziesietny", "Ułamek na dziesiętny", 3, 3, 10, 3, 2052, "na-dziesietny",
        lambda r: distinct(N, lambda: ulamek_na_dziesietny(r))),
    Set("53-ulamki-dziel", "Dzielenie ułamków", 3, 3, 11, 3, 2053, "ulamki-:",
        lambda r: distinct(N, lambda: ulamki_dzielenie(r))),
    Set("54-notacja", "Notacja naukowa", 3, 3, 11, 2, 2054, "notacja",
        lambda r: distinct(N, lambda: notacja_naukowa(r))),
    Set("55-potega-ulamek", "Wykładnik ułamkowy", 3, 3, 11, 3, 2055, "potega-ulamek",
        lambda r: distinct(N, lambda: potega_ulamkowa(r))),
    Set("56-na-procent", "Ułamek na procent", 3, 3, 10, 3, 2056, "na-procent",
        lambda r: distinct(N, lambda: ulamek_na_procent(r))),
    Set("57-male", "Małe dziesiętne", 3, 3, 9, 3, 2057, "male",
        lambda r: distinct(N, lambda: dziesietne_male(r))),
    Set("58-ulamki-mnoz-b", "Mnożenie ułamków II", 3, 3, 10, 3, 2058, "ulamki-x",
        lambda r: distinct(N, lambda: ulamki_mnozenie(r))),
    Set("59-logarytmy-b", "Logarytmy II", 3, 3, 9, 3, 2059, "logarytmy",
        lambda r: distinct(N, lambda: logarytmy(r))),
    Set("60-potegi-ujemne-b", "Potęgi ujemne i zero II", 3, 3, 8, 3, 2060, "potegi-ujemne",
        lambda r: distinct(N, lambda: potegi_ujemne(r))),
    Set("61-na-dziesietny-b", "Ułamek na dziesiętny II", 3, 3, 10, 3, 2061, "na-dziesietny",
        lambda r: distinct(N, lambda: ulamek_na_dziesietny(r))),
    Set("62-ulamki-dziel-b", "Dzielenie ułamków II", 3, 3, 11, 3, 2062, "ulamki-:",
        lambda r: distinct(N, lambda: ulamki_dzielenie(r))),
    Set("63-notacja-b", "Notacja naukowa II", 3, 3, 11, 2, 2063, "notacja",
        lambda r: distinct(N, lambda: notacja_naukowa(r))),
    Set("64-potega-ulamek-b", "Wykładnik ułamkowy II", 3, 3, 11, 3, 2064, "potega-ulamek",
        lambda r: distinct(N, lambda: potega_ulamkowa(r))),
    Set("65-na-procent-b", "Ułamek na procent II", 3, 3, 10, 3, 2065, "na-procent",
        lambda r: distinct(N, lambda: ulamek_na_procent(r))),
    Set("66-male-b", "Małe dziesiętne II", 3, 3, 9, 3, 2066, "male",
        lambda r: distinct(N, lambda: dziesietne_male(r))),
    Set("67-mix3", "Mieszane — ułamki i potęgi", 3, 3, 11, 3, 2067, "mieszane",
        lambda r: mieszane(r, [
            lambda: ulamki_mnozenie(r),
            lambda: potegi_ujemne(r),
            lambda: logarytmy(r),
            lambda: ulamek_na_dziesietny(r),
        ])),
    Set("68-ulamki-mnoz-c", "Mnożenie ułamków III", 3, 3, 10, 3, 2068, "ulamki-x",
        lambda r: distinct(N, lambda: ulamki_mnozenie(r))),
    Set("69-logarytmy-c", "Logarytmy III", 3, 3, 9, 3, 2069, "logarytmy",
        lambda r: distinct(N, lambda: logarytmy(r))),
    Set("70-potegi-ujemne-c", "Potęgi ujemne i zero III", 3, 3, 8, 3, 2070, "potegi-ujemne",
        lambda r: distinct(N, lambda: potegi_ujemne(r))),
    Set("71-ulamki-dziel-c", "Dzielenie ułamków III", 3, 3, 11, 3, 2071, "ulamki-:",
        lambda r: distinct(N, lambda: ulamki_dzielenie(r))),
    Set("72-potega-ulamek-c", "Wykładnik ułamkowy III", 3, 3, 11, 3, 2072, "potega-ulamek",
        lambda r: distinct(N, lambda: potega_ulamkowa(r))),

    # --- Blok IV --- Zastosowania ----------------------------------
    Set("73-kombinatoryka", "Kombinatoryka", 4, 3, 12, 3, 2073, "kombinatoryka",
        lambda r: distinct(N, lambda: kombinatoryka(r))),
    Set("74-kmh-ms", "km/h i m/s", 4, 3, 9, 2, 2074, "kmh-ms",
        lambda r: distinct(N, lambda: kmh_ms(r))),
    Set("75-predkosc", "Prędkość średnia", 4, 3, 13, 2, 2075, "predkosc",
        lambda r: distinct(N, lambda: predkosc(r)), True),
    Set("76-skala", "Skala mapy", 4, 3, 12, 2, 2076, "skala",
        lambda r: distinct(N, lambda: skala(r)), True),
    Set("77-harmoniczna", "Tam i z powrotem", 4, 3, 14, 2, 2077, "harmoniczna",
        lambda r: distinct(N, lambda: srednia_harmoniczna(r)), True),
    Set("78-kalendarz", "Dzień tygodnia", 4, 3, 16, 2, 2078, "kalendarz",
        lambda r: distinct(N, lambda: dzien_tygodnia(r)), True),
    Set("79-procent-lata", "Procent przez lata", 4, 3, 14, 2, 2079, "procent-lata",
        lambda r: distinct(N, lambda: procent_lata(r)), True),
    Set("80-kombinatoryka-b", "Kombinatoryka II", 4, 3, 12, 3, 2080, "kombinatoryka",
        lambda r: distinct(N, lambda: kombinatoryka(r))),
    Set("81-kmh-ms-b", "km/h i m/s II", 4, 3, 9, 2, 2081, "kmh-ms",
        lambda r: distinct(N, lambda: kmh_ms(r))),
    Set("82-predkosc-b", "Prędkość średnia II", 4, 3, 13, 2, 2082, "predkosc",
        lambda r: distinct(N, lambda: predkosc(r)), True),
    Set("83-skala-b", "Skala mapy II", 4, 3, 12, 2, 2083, "skala",
        lambda r: distinct(N, lambda: skala(r)), True),
    Set("84-harmoniczna-b", "Tam i z powrotem II", 4, 3, 14, 2, 2084, "harmoniczna",
        lambda r: distinct(N, lambda: srednia_harmoniczna(r)), True),
    Set("85-kalendarz-b", "Dzień tygodnia II", 4, 3, 16, 2, 2085, "kalendarz",
        lambda r: distinct(N, lambda: dzien_tygodnia(r)), True),
    Set("86-procent-lata-b", "Procent przez lata II", 4, 3, 14, 2, 2086, "procent-lata",
        lambda r: distinct(N, lambda: procent_lata(r)), True),
    Set("87-kombinatoryka-c", "Kombinatoryka III", 4, 3, 12, 3, 2087, "kombinatoryka",
        lambda r: distinct(N, lambda: kombinatoryka(r))),
    Set("88-kmh-ms-c", "km/h i m/s III", 4, 3, 9, 2, 2088, "kmh-ms",
        lambda r: distinct(N, lambda: kmh_ms(r))),
    Set("89-predkosc-c", "Prędkość średnia III", 4, 3, 13, 2, 2089, "predkosc",
        lambda r: distinct(N, lambda: predkosc(r)), True),
    Set("90-skala-c", "Skala mapy III", 4, 3, 12, 2, 2090, "skala",
        lambda r: distinct(N, lambda: skala(r)), True),
    Set("91-mix4", "Mieszane — zastosowania", 4, 3, 13, 2, 2091, "mieszane",
        lambda r: mieszane(r, [
            lambda: kombinatoryka(r),
            lambda: kmh_ms(r),
            lambda: potega_modulo(r),
            lambda: ulamki_dzielenie(r),
        ])),
    Set("92-harmoniczna-c", "Tam i z powrotem III", 4, 3, 14, 2, 2092, "harmoniczna",
        lambda r: distinct(N, lambda: srednia_harmoniczna(r)), True),
    Set("93-kalendarz-c", "Dzień tygodnia III", 4, 3, 16, 2, 2093, "kalendarz",
        lambda r: distinct(N, lambda: dzien_tygodnia(r)), True),
    Set("94-procent-lata-c", "Procent przez lata III", 4, 3, 14, 2, 2094, "procent-lata",
        lambda r: distinct(N, lambda: procent_lata(r)), True),
    Set("95-kombinatoryka-d", "Kombinatoryka IV", 4, 3, 12, 3, 2095, "kombinatoryka",
        lambda r: distinct(N, lambda: kombinatoryka(r))),
    Set("96-kmh-ms-d", "km/h i m/s IV", 4, 3, 9, 2, 2096, "kmh-ms",
        lambda r: distinct(N, lambda: kmh_ms(r))),

    # --- Pomiary kontrolne -----------------------------------------
    #  One per block, five scoring rows each, done weekly for the four weeks
    #  its block runs. Same argument as the basic volume's: a benchmark is
    #  informative over the material the reader is drilling this month.
    Set("99-kontrolny-1", "Pomiar kontrolny I", 9, 2, 10, 3, 2097, "kontrolny",
        lambda r: mieszane(r, [
            lambda: dwojkowy(r),
            lambda: modulo(r),
            lambda: szesnastkowy(r),
            lambda: cyfra_kontrolna(r),
            lambda: potega_modulo(r),
        ]), rows=5),
    Set("100-kontrolny-2", "Pomiar kontrolny II", 9, 2, 11, 3, 2098, "kontrolny",
        lambda r: mieszane(r, [
            lambda: rozklad(r),
            lambda: euklides(r),
            lambda: liczba_dzielnikow(r),
            lambda: suma_ciagu(r),
        ]), rows=5),
    Set("101-kontrolny-3", "Pomiar kontrolny III", 9, 3, 11, 3, 2099, "kontrolny",
        lambda r: mieszane(r, [
            lambda: ulamki_mnozenie(r),
            lambda: ulamki_dzielenie(r),
            lambda: potegi_ujemne(r),
            lambda: logarytmy(r),
            lambda: ulamek_na_dziesietny(r),
        ]), rows=5),
    Set("102-kontrolny-4", "Pomiar kontrolny IV", 9, 3, 13, 2, 2100, "kontrolny",
        lambda r: mieszane(r, [
            lambda: kombinatoryka(r),
            lambda: kmh_ms(r),
            lambda: potega_ulamkowa(r),
            lambda: notacja_naukowa(r),
        ]), rows=5),
]


ADV_HAND = [
    Hand("97-zagadki", "Zagadki — trudniejsze", 3, "20:00", "zagadki", 16),
    Hand("98-triki", "Triki zaawansowane", 3, "12:00", "triki-reczne", 16),
]

ADV_TITLES = {1: "Systemy i reszty", 2: "Struktura liczby",
              3: "Ułamki i potęgi", 4: "Zastosowania",
              8: HAND_CHAPTER, 9: "Pomiary kontrolne"}

ADV = Volume("adv", "sets-adv", "Trening Mózgu — Zaawansowany",
             ADV_SETS, ADV_HAND, ADV_TITLES)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--check", action="store_true")
    a = p.parse_args()
    return build(ADV, a.check, BASIC)


if __name__ == "__main__":
    sys.exit(main())
