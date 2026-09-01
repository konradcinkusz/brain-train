# Wkład w Trening Mózgu

Nowe zadania mile widziane. Ten plik opisuje, jak je napisać, żeby pasowały do
formatu i przeszły bramki.

---

## Najpierw: co ta książka mierzy

Nie to, czy pojedyncze zadanie jest ciekawe. **Ile zadań czytelnik zrobi i jak
szybko.** Wszystko poniżej z tego wynika: zadania są krótkie, jedno pod drugim,
po 24--30 na stronie, a odpowiedzi są na końcu książki, żeby nie przerywały
serii.

Zadanie, które wymaga akapitu wstępu, nie pasuje do tej książki.

## Dwa źródła

| Gdzie | Co | Kto pisze |
|---|---|---|
| `tools/gen_sets.py` | zestawy rachunkowe | generator |
| `book/sets/*.tex` | zagadki, ciągi, wyzwania, triki | człowiek |

**Rachunków nie wpisuje się ręcznie.** Kilkaset sum przepisanych z palca to
miejsce, w którym chowają się pomyłki; generator liczy odpowiedź tym samym
kodem, którym układa zadanie, więc nie mogą się rozjechać.

**Zagadek się nie generuje.** Pułapka słowna to żart, a żart ma autora.

`book/sets/generated/` jest **generowane i nadpisywane** — nie edytuj tam nic.

## Nowe zadanie rachunkowe

Dopisz je do generatora. Zadanie i odpowiedź powstają razem:

```python
def dodawanie(r, n, lo, hi):
    for _ in range(n):
        a, b = r.randint(lo, hi), r.randint(lo, hi)
        yield f"${fmt(a)} + {fmt(b)}$", fmt(a + b)
```

Potem dopisz zestaw do listy `SETS`:

```python
("15-nowy", "Tytuł zestawu", 2, "4:00", 3, 1015,
 lambda r: list(dodawanie(r, 30, 101, 999))),
```

Kolumny: `(nazwa pliku, tytuł, gwiazdki, cel czasowy, liczba kolumn, seed, builder)`.

**Seed musi być nowy i stały.** Książka ma być identyczna przy każdym buildzie
— inaczej czytelnik nie porówna dzisiejszego czasu z zeszłotygodniowym.

**Dzielenie buduj od ilorazu**, nie losuj dzielnej i dzielnika osobno, bo
wyjdzie reszta:

```python
b, q = r.randint(blo, bhi), r.randint(qlo, qhi)
yield rf"${fmt(b * q)} \div {fmt(b)}$", fmt(q)
```

Potem `make sets && make book`.

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
\end{zestaw}
```

Argumenty: tytuł, gwiazdki, cel czasowy, liczba kolumn. Potem dopisz
`\input{sets/nazwa}` w `book/structure.tex`.

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
- **`STALE`** — zapomniałeś `make sets`.

**Nie ufaj kodowi wyjścia `latexmk`.** Przy `nonstopmode` nieudany przebieg i
tak zapisuje PDF. Bramką jest `tools/checklog.py`.

Zaktualizuj liczbę zadań w `README.md`, jeśli się zmieniła — `make book`
wypisuje ją na końcu.

## Kontekst

`CLAUDE.md` opisuje, dlaczego układ wygląda tak, jak wygląda, i jakie pułapki
zostały już rozbrojone. Przeczytaj go, zanim ruszysz `book/preamble.tex`.
