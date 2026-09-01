# Wkład w Trening Mózgu

Nowe zadania mile widziane. Ten plik opisuje, jak je napisać, żeby pasowały do
formatu i przeszły bramki.

---

## Gdzie mieszkają zadania

**Edytuj `areas/`, nigdy `book/chapters/`.**

`book/chapters/*.tex` jest **generowane** przez `tools/convert_deck.py` i
nadpisywane przy każdym `make convert`. Zmiana zrobiona tam znika po pierwszej
regeneracji, a `make drift` i tak zgłosi rozjazd.

```
areas/3-zagadki-logiczne.tex   ← tu piszesz
        │  make convert
        ▼
book/chapters/3-zagadki-logiczne.tex   ← generowane, nie dotykaj
```

## Jak wygląda zadanie

Para makr: zadanie i odpowiedź do niego.

```latex
% -- 19 --
\ExerciseSlide[\CategoryBadge[LogicColor!20]{Sylogizm}]
  {1}{2 min}{%
    Wszystkie Bloopy są Razzies.\par
    Wszystkie Razzies są Lazzies.\par
    Czy wszystkie Bloopy są Lazzies?
  }
\AnswerSlide[\CategoryBadge[LogicColor!20]{Sylogizm}]{Tak!}{Bloopy $\to$ Razzies $\to$ Lazzies.}
```

| Argument | Znaczenie |
|---|---|
| `[...]` | Odznaka kategorii — opcjonalna, ale w praktyce zawsze jest |
| `{1}` | Trudność: `1`, `2` lub `3` gwiazdki |
| `{2 min}` | Limit czasu, tak jak ma się wyświetlić |
| `{...}` | Treść zadania |
| `\AnswerSlide{...}{...}` | Wynik, a potem **co najwyżej jedna linijka** podpowiedzi |

Konwerter przenosi odpowiedź o jedną ramkę do przodu — w książce odpowiedź do
zadania *N* otwiera ramkę *N+1*. Nic z tym nie robisz, to dzieje się samo.

## Zasady, których bramki nie sprawdzą

**Odpowiedź pokazuje wynik i najwyżej jedną linijkę podpowiedzi.** Bez rozpisywania
kroków, bez tłumaczenia teorii. To reguła tego repozytorium od commita `01c9d37`.

**Żadna instrukcja nie może zależeć od tego, gdzie łamie się strona.** Pisz
*zanim przeczytasz dalej*, nigdy *zanim odwrócisz stronę*. Miejsce łamania
strony jest własnością formatu, nie tekstu — zdanie o przewracaniu kartki jest
prawdziwe w jednym buildzie i fałszywe w drugim. *Zakryj dłonią stronę poniżej*
jest w porządku: mówi o dłoni, nie o kartce.

**Gwiazdki mają zgadzać się z limitem czasu:**

| | | |
|---|---|---|
| ★ | łatwe | do 1 min |
| ★★ | średnie | 1–3 min |
| ★★★ | trudne | 3–5 min |

**Cyfra zostaje cyfrą.** Nie zapisuj liczby słowem tam, gdzie jest liczbą —
`$2$`, nie *dwa*.

**Diakrytyki kopiuj tak, jak je zastałeś.** Pliki mieszają UTF-8 (`Kolejność`)
z escape'ami TeX-a (`Mno\. zenie`). Oba dają ten sam znak; ujednolicanie jednego
w drugi to cicha zmiana w kilkudziesięciu zadaniach, o którą nikt nie prosił.

**Komentarz `% -- NN --`** to globalny numer zadania. Dodając zadanie na końcu
obszaru, nadaj mu kolejny wolny numer; wstawiając w środku, przenumeruj resztę
pliku.

## Kolory obszarów

Każdy obszar ma swój akcent — użyj tego, który pasuje do pliku:

| Obszar | Kolor |
|---|---|
| 1 Arytmetyka | `ArithColor!20` |
| 2 Kolejność Działań | `OpsColor!20` |
| 3 Zagadki Logiczne | `LogicColor!20` |
| 4 Ciągi i Wzorce | `SeqColor!20` |
| 5 Mieszane Wyzwania | `MixColor!20` |

## Zanim wyślesz pull requesta

```bash
make convert   # przenieś zmiany z areas/ do book/chapters/
make book      # zbuduj i uruchom wszystkie bramki
```

`make book` musi zakończyć się bez błędów. Trzy rzeczy, które zgłosi:

- **`errors`, `unresolved refs`, `overfull hbox/vbox`** — muszą być zerowe.
  Przepełnione pudełko oznacza, że coś wystaje poza kolumnę.
- **`wrong margin`** — numery ramek muszą być na zewnętrznym marginesie.
- **`STALE`** — zapomniałeś `make convert`.

Zaktualizuj też liczbę zadań w `README.md`, jeśli się zmieniła.

**Nie ufaj kodowi wyjścia `latexmk`.** Przy `nonstopmode` nieudany przebieg i
tak zapisuje PDF. Bramką jest `tools/checklog.py`, i to on decyduje.

## Nowy obszar

Nowy rozdział to trzy zmiany:

1. `areas/N-nazwa.tex` z zadaniami,
2. wpis w `AREA_META` w `tools/convert_deck.py` (tytuł rozdziału i jedno zdanie
   wprowadzenia),
3. `\include{chapters/N-nazwa}` w `book/structure.tex`.

Kolor obszaru dodaj w `book/preamble.tex` obok pozostałych.

## Kontekst

`CLAUDE.md` opisuje, dlaczego układ wygląda tak, jak wygląda, i jakie pułapki
zostały już rozbrojone. Przeczytaj go, zanim ruszysz `book/preamble.tex`.
