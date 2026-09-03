# Wkład w Trening Mózgu

Nowe zadania mile widziane. Ten plik opisuje, jak je napisać, żeby pasowały do
formatu i przeszły bramki.

---

## Najpierw: co ta książka mierzy

Nie to, czy pojedyncze zadanie jest ciekawe. **Ile zadań czytelnik zrobi i jak
szybko.** Wszystko poniżej z tego wynika: zadania są krótkie, jedno pod drugim,
a odpowiedzi są na końcu książki, żeby nie przerywały serii.

Zadanie, które wymaga akapitu wstępu, nie pasuje do tej książki.

## Dwa tomy

`tools/gen_sets.py` to tom podstawowy, `tools/gen_sets_adv.py` — zaawansowany.
Drugi importuje z pierwszego całą maszynerię i wszystkie buildery; ma własne
tylko te, których pierwszy nie potrzebuje. **Nie kopiuj między nimi niczego** —
jeśli obu potrzebny jest ten sam builder, jego miejsce jest w `gen_sets.py`.

Seedy: `1001`–`1225` należą do tomu I, `2001`–`2100` do tomu II, a `audit()`
odmawia seeda, którego używa drugi tom.

## Dwa źródła

| Gdzie | Co | Kto pisze |
|---|---|---|
| `tools/gen_sets.py`, `tools/gen_sets_adv.py` | zestawy rachunkowe | generator |
| `book/sets/*.tex`, `book/sets-adv/*.tex` | zagadki, ciągi, wyzwania, triki | człowiek |

**Rachunków nie wpisuje się ręcznie.** Kilkaset sum przepisanych z palca to
miejsce, w którym chowają się pomyłki; generator liczy odpowiedź tym samym
kodem, którym układa zadanie, więc nie mogą się rozjechać.

**Zagadek się nie generuje.** Pułapka słowna to żart, a żart ma autora.

`book/sets/generated/` jest **generowane i nadpisywane** — nie edytuj tam nic.

## Nowe zadanie rachunkowe

Dopisz je do generatora. **Builder losuje JEDNO zadanie** i liczy jego
odpowiedź z tych samych liczb, które wypisał:

```python
def dodawanie(r, lo, hi):
    a, b = r.randint(lo, hi), r.randint(lo, hi)
    return f"${fmt(a)} + {fmt(b)}$", fmt(a + b)
```

Potem dopisz zestaw do listy `SETS`:

```python
Set("82-nowy", "Tytuł zestawu", 2, 2, 8, 3, 1157, "dodawanie",
    lambda r: distinct(N, lambda: dodawanie(r, 101, 999))),
```

Pola: `nazwa pliku`, `tytuł`, `blok` (1–3, czyli rozdział), `gwiazdki`,
**`sekundy na zadanie`**, `liczba kolumn`, `seed`, `rodzina`, `builder`,
i opcjonalnie `wide=True`, gdy zadanie nie mieści się w `\z` i potrzebuje `\zz`.

**Celu czasowego się nie wpisuje — wpisuje się sekundy na jedno zadanie.**
Cel to `sekundy × N`, więc zmiana `N` przesuwa wszystkie cele naraz, zamiast
zostawiać osiemdziesiąt liczb, z których każda przestała być prawdziwa.

**Rodzina nie jest ozdobą.** `tools/gen_plan.py` układa z niej plan tak, żeby
dwa zestawy tej samej rodziny nie wypadły dzień po dniu — trening z
przeplotem trzyma się dłużej niż blokowy. **Rodzina to jest to, co czytelnik
ćwiczy**: dwa zestawy dzielą ją tylko wtedy, gdy zrobienie jednego zamiast
drugiego to ta sama praca. Dlatego „procent od drugiej strony" ma własną
rodzinę, a nie siedzi w `procenty` — plan wybiera zestawy tak, żeby każda
rodzina weszła, zanim któraś dostanie drugi zestaw, więc źle nadana rodzina
niczego nie psuje, tylko po cichu wyrzuca umiejętność z planu.

`distinct(N, ...)` losuje aż uzbiera `N` **różnych** zadań — przy czterdziestu
losowaniach powtórki są prawie pewne, a powtórka w zestawie wygląda jak błąd
druku. Jeśli zakres buildera jest węższy niż `N`, `distinct` przerwie build
z komunikatem, zamiast kręcić się w kółko.

**Długość zestawu to `N`, jedna stała na górze pliku.** Nie wpisuj liczby
zadań w pojedynczy zestaw — dwa czasy da się porównać tylko wtedy, gdy zestawy
mierzą tę samą pracę.

**Seed musi być nowy i stały.** Zmiana seeda po cichu podmienia czterdzieści
zadań, więc czytelnik porównuje wtedy dwa różne zestawy. Zmiana nazwy pliku
i kolejności na liście jest darmowa; zmiana seeda nie.

**Dzielenie buduj od ilorazu**, nie losuj dzielnej i dzielnika osobno, bo
wyjdzie reszta:

```python
b, q = r.randint(blo, bhi), r.randint(qlo, qhi)
return rf"${fmt(b * q)} \div {fmt(b)}$", fmt(q)
```

**Bez `\sqrt` i `\frac`.** Oba są wyższe niż `\strut`, który ustala rytm
wierszy, więc zestaw z nich zbudowany oddycha inaczej niż wszystkie pozostałe.
Jeśli działanie trzeba nazwać — nazwij je słowem (`pierwiastek z $169$`).

**I naucz checkera nowego kształtu pytania.** `tools/checkanswers.py`
przelicza każdą wydrukowaną odpowiedź z wydrukowanego pytania, drugą ścieżką
niż generator — i **kształt, którego nie rozpoznaje, jest błędem, nie
pominięciem**. Checker, który po cichu przepuszcza to, czego nie zna,
przestaje mierzyć w dniu, w którym ktoś doda buildera, i dalej świeci na
zielono. Dopisz regułę:

```python
@rule(r"^suma cyfr \$([\d\\,]+)\$$")
def _suma_cyfr(m):
    return Fraction(sum(int(c) for c in m[1].replace("\\,", "")))
```

Potem `make sets && make book`. **`make sets` regeneruje też plan** — plan
wskazuje zestawy po numerach, więc dołożenie zestawu przesuwa wszystko po nim.
Gdybyś o tym zapomniał, build i tak się przerwie: listy `\input` niosą numer,
pod którym zestaw ma wypaść.

## Nowe zadanie pisane ręcznie

Do odpowiedniego pliku w `book/sets/`:

```latex
\zz{Ile miesi\k{e}cy w roku ma 28 dni?}{Wszystkie \hfill {\itshape\footnotesize Ka\. zdy ma co najmniej 28 dni.}}
```

- `\z{treść}{odpowiedź}` — krótkie, mieści się w kolumnie
- `\zz{treść}{odpowiedź}` — szerokie, zajmuje całą szerokość

Numeracja jest automatyczna, w obrębie zestawu. Odpowiedź trafia do dodatku na
końcu sama — nie ma osobnej listy do zaktualizowania.

## Nowy zestaw pisany ręcznie

```latex
\begin{zestaw}{Tytuł}{2}{5:00}{2}
  \z{...}{...}
  \btnc              % koniec pierwszej kolumny
  \z{...}{...}
\end{zestaw}
```

Argumenty: tytuł, gwiazdki, cel czasowy, liczba kolumn — plus opcjonalny
pierwszy argument w nawiasie kwadratowym: liczba wierszy na pomiar, domyślnie
**dwa** (`\begin{zestaw}[5]{...}` mają tylko zestawy kontrolne). Dwa, bo plan
wyznacza powtórkę prawie każdego zestawu, a oba czasy muszą stać obok siebie.

Potem dopisz go do listy `HAND` w `tools/gen_sets.py` i uruchom `make sets`.
**Nie dopisuj `\input` wprost do `structure.tex`** — zestaw wstawiony z
pominięciem generowanej listy nie dostanie numeru, którego oczekuje plan, i
build się przerwie. To jest celowe: plan i książka muszą się zgadzać co do
numeracji, a jedna lista jest jedynym sposobem, żeby nie mogły się rozjechać.

**`\btnc` mówi, gdzie kończy się kolumna** — przy `n` kolumnach potrzeba
`n-1` takich znaczników, rozłożonych równo. Zestaw jest jednym nierozrywalnym
pudełkiem (dlatego nie ma tu `multicols`), więc podziału nie zrobi za Ciebie
składacz.

**Zestaw musi się zmieścić na stronie.** Nagłówek i stopka mają etykiety, a
build przerywa się błędem `Zestaw N is split`, jeśli wypadną na różnych
stronach. Za długi zestaw skróć albo daj mu więcej kolumn.

## Zasady, których bramki nie sprawdzą

**Podpowiedź co najwyżej jednolinijkowa, i tylko wtedy, gdy coś wnosi.** Przy
rachunkach odpowiedź to sam wynik. Przy trikach podpowiedź **jest** treścią —
wynik sprawdzisz w dziesięć sekund, chodzi o skrót.

**Gwiazdki i cel czasowy opisują zestaw, nie zadanie.** Nie ma czegoś takiego
jak trudne zadanie w łatwym zestawie — jeśli jedno zadanie odstaje, jest w złym
zestawie.

**Cyfra zostaje cyfrą.** `$2$`, nie *dwa*.

**Diakrytyki kopiuj tak, jak je zastałeś.** Pliki mieszają UTF-8 (`Kolejność`)
z escape'ami TeX-a (`Mno\. zenie`). Oba dają ten sam znak.

**Żadna instrukcja nie zależy od łamania strony.** Odpowiedzi są na końcu
książki, więc nie ma czego przewracać — i to jest jeden z powodów, dla których
ten układ zastąpił poprzedni.

## Zanim wyślesz pull requesta

```bash
make sets      # jeśli ruszałeś generator
make book      # build + bramki
```

`make book` musi wyjść bez błędów:

- **`errors`, `unresolved refs`, `overfull hbox/vbox`** — zerowe. Przepełnione
  pudełko znaczy, że coś wystaje poza kolumnę; najczęściej zadanie za szerokie
  na `\z` i powinno być `\zz`.
- **`Zestaw N expected number M`** — kolejność w książce rozjechała się
  z generatorem. `make sets` naprawia; jeśli nie, przestawiłeś rozdział
  w `structure.tex`.
- **`STALE`** — zapomniałeś `make sets` (albo zostawiłeś w
  `book/sets/generated/` plik, którego generator już nie tworzy).
- **`nierozpoznanych`** — dodałeś buildera i nie nauczyłeś jego kształtu
  `tools/checkanswers.py`. Zobacz wyżej.
- **`Zestaw N is split`** — zestaw nie mieści się na stronie.

**Nie ufaj kodowi wyjścia `latexmk`.** Przy `nonstopmode` nieudany przebieg i
tak zapisuje PDF. Bramką jest `tools/checklog.py`.

Zaktualizuj liczby w `README.md`, jeśli się zmieniły — `make sets` wypisuje
liczbę zestawów i zadań w każdym bloku, a `make book` liczbę stron.

## Kontekst

`CLAUDE.md` opisuje, dlaczego układ wygląda tak, jak wygląda, i jakie pułapki
zostały już rozbrojone. Przeczytaj go, zanim ruszysz `book/preamble.tex`.
