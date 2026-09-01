<a name="readme-top"></a>

# Trening Mózgu

[![Ask me anything](https://flat.badgen.net/static/Ask%20me/anything?icon=github&color=black&scale=1.01)](https://github.com/konradcinkusz "Ask me anything")
[![Licencja](https://flat.badgen.net/github/license/konradcinkusz/brain-train?icon=github&color=black&scale=1.01)](https://github.com/konradcinkusz/brain-train/blob/main/LICENSE "Licencja")
[![Utrzymywane](https://flat.badgen.net/static/Maintained/yes?icon=github&color=black&scale=1.01)](https://github.com/konradcinkusz/brain-train/commits/main "Utrzymywane")
[![Gałęzie](https://flat.badgen.net/github/branches/konradcinkusz/brain-train?icon=github&color=black&scale=1.01)](https://github.com/konradcinkusz/brain-train/branches "Gałęzie")
[![Commity](https://flat.badgen.net/github/commits/konradcinkusz/brain-train?icon=github&color=black&scale=1.01)](https://github.com/konradcinkusz/brain-train/commits/main "Commity")
[![Zgłoszenia](https://flat.badgen.net/github/issues/konradcinkusz/brain-train?icon=github&color=black&scale=1.01)](https://github.com/konradcinkusz/brain-train/issues "Zgłoszenia")
[![Pull requesty](https://flat.badgen.net/github/prs/konradcinkusz/brain-train?icon=github&color=black&scale=1.01)](https://github.com/konradcinkusz/brain-train/pulls "Pull requesty")
[![Build book](https://github.com/konradcinkusz/brain-train/actions/workflows/build.yml/badge.svg)](https://github.com/konradcinkusz/brain-train/actions/workflows/build.yml "Build book")

Zbiór krótkich zadań na czas — arytmetyka, kolejność działań, zagadki logiczne,
ciągi liczbowe, wyzwania mieszane i szybkie triki rachunkowe. Format inspirowany serią *Trening Mózgu*
i programowanym układem Strouda: jedno zadanie na **ramkę**, stoper, porównanie
z limitem. Bez kalkulatora.

**52 zadania · 6 obszarów · 26 stron A4.**

## Quick start

```bash
git clone https://github.com/konradcinkusz/brain-train.git
cd brain-train
make book
```

Potrzebujesz `pdflatex`, `latexmk` i `python3`. Gotowy PDF powstaje jako
`book/main-pl-a4.pdf`.

## Jak działa format

Każde zadanie zajmuje jedną **ramkę** — kawałek strony między dwiema cienkimi
kreskami, z numerem na zewnętrznym marginesie. Odpowiedź nie stoi pod zadaniem:
otwiera ramkę **następną**.

```
──────────────────────────────────────────────────────  ①
★☆☆                              [Dodawanie]  [⏱ 30 s]
                    47 + 38 = ?
──────────────────────────────────────────────────────  ②
           ┌────────────────────────────┐
           │             85             │
           └────────────────────────────┘
★☆☆                             [Odejmowanie]  [⏱ 30 s]
                   156 − 79 = ?
```

Zakrywasz dłonią stronę poniżej kreski, uruchamiasz stoper, liczysz w pamięci,
a dopiero potem czytasz dalej. To jedyna reguła tego formatu — i powód, dla
którego książka nie jest prezentacją przelaną na papier: slajd może schować
odpowiedź, bo czytelnik jej nie widzi, dopóki nie przewinie. Strona nie może.

<p align="right">(<a href="#readme-top">wróć na górę</a>)</p>

## Poziomy trudności

| Gwiazdki | Poziom | Czas docelowy |
|----------|--------|---------------|
| ★ | Łatwy | do 1 min |
| ★★ | Średni | 1–3 min |
| ★★★ | Trudny | 3–5 min |

## Struktura repozytorium

```
.
├── areas/                             # ŹRÓDŁO zadań (52 w sześciu obszarach)
│   ├── 1-arytmetyka-podstawy.tex     # Dodawanie, odejmowanie, mnożenie, dzielenie
│   ├── 2-kolejnosc-dzialan.tex       # Nawiasy, priorytety, potęgi
│   ├── 3-zagadki-logiczne.tex        # Sylogizmy, pułapki słowne, dedukcja
│   ├── 4-ciagi-i-wzorce.tex          # Ciągi liczbowe i literowe
│   ├── 5-mieszane-wyzwania.tex       # Prędkość, procenty, finanse, praca
│   └── 6-szybkie-triki.tex           # Skróty rachunkowe: ×11, kwadraty, procenty
├── book/                              # KSIĄŻKA A4 (układ Stroudowski)
│   ├── main-pl-a4.tex                # Plik główny — cienki, format jest w preambule
│   ├── preamble.tex                  # Ramki, odpowiedzi, numery na marginesie
│   ├── structure.tex                 # JEDNA lista rozdziałów
│   ├── frontmatter/                  # Strona tytułowa, „Jak korzystać”
│   └── chapters/                     # GENEROWANE z areas/ (make convert)
├── tools/
│   ├── convert_deck.py               # areas/ → book/chapters/
│   ├── checklog.py                   # Bramka logu (nie kod wyjścia!)
│   └── checkbadges.py                # Numery ramek na właściwym marginesie
├── deck-archive/                      # Prezentacja Beamer — zarchiwizowana, nie budowana
├── .github/workflows/
│   ├── build.yml                     # Build książki na każdy push i PR
│   └── ci.yml                        # Build + wydanie PDF na tag v*/V*
├── Makefile
├── CLAUDE.md                          # Decyzje układu i pułapki — czytaj przed zmianami
├── LICENSE
└── README.md
```

## Budowanie

| Cel | Co robi |
|---|---|
| `make book` | Buduje książkę i uruchamia wszystkie bramki |
| `make convert` | `areas/` → `book/chapters/` |
| `make drift` | Sprawdza, czy rozdziały zgadzają się z `areas/` |
| `make check` | Same bramki, bez budowania |
| `make clean` | Usuwa artefakty |

Trzy bramki, każda sprawdza coś, czego pozostałe nie widzą:

- **`tools/checklog.py`** — błędy, nierozwiązane referencje, przepełnione pudełka
  i brak zbieżności. To jest bramka, **nie kod wyjścia `latexmk`**: przy
  `nonstopmode` nieudany przebieg i tak zapisuje PDF, a przy `-file-line-error`
  linia błędu zaczyna się od ścieżki, więc `grep '^!'` też jej nie widzi.
- **`tools/checkbadges.py`** — czyta gotowy PDF i sprawdza, że numer każdej ramki
  jest na *zewnętrznym* marginesie. Ten defekt nie daje błędu, ostrzeżenia ani
  przepełnionego pudełka — żaden log go nie zobaczy.
- **`tools/convert_deck.py --check`** — rozdziały są generowane z `areas/`;
  zadanie zmienione w źródle i nieprzekonwertowane zostawia w książce starą wersję,
  a obie wersje plików są poprawne, więc reszta bramek świeci na zielono.

Obie bramki czytające PDF sprawdzono, wprowadzając defekt, którego pilnują —
sprawdzenie, które nigdy nie zawiodło, może nie mierzyć niczego.

<p align="right">(<a href="#readme-top">wróć na górę</a>)</p>

### Dlaczego zadania mieszkają w `areas/`, a nie w `book/chapters/`

W `areas/` zadanie stoi obok **swojej własnej** odpowiedzi — tak się o zadaniu
myśli. W książce odpowiedź otwiera ramkę *następną*, więc leży przy zadaniu
**kolejnym**. Pisanie wprost w formacie książki znaczyłoby przesuwanie każdej
odpowiedzi o jedno miejsce ręcznie; `tools/convert_deck.py` robi to za Ciebie i
`make drift` pilnuje, żeby obie strony się nie rozjechały.

## Wydanie PDF

Wypchnij tag `v*` lub `V*`, aby zbudować książkę i dołączyć
`trening-mozgu-a4.pdf` do wydania:

```bash
git tag v2.0.0
git push origin v2.0.0
```

Wydanie powstaje tylko wtedy, gdy build przejdzie wszystkie bramki — job wydania
deklaruje `needs: build`, więc inaczej w ogóle się nie uruchamia. To celowe:
wydanie `v1.0.0` nie ma załączonego PDF-a, bo jego build się nie powiódł, a nikt
tego nie zauważył ([#21](https://github.com/konradcinkusz/brain-train/issues/21)).

## Wkład

Nowe zadania mile widziane. Zacznij od
[CONTRIBUTING.md](CONTRIBUTING.md) — opisuje format ramki, konwencje i to, co
trzeba zaktualizować, dodając zadanie.

## Licencja

MIT No Attribution — szczegóły w [LICENSE](LICENSE).

Maszyneria układu (`book/preamble.tex`, `tools/`) jest portem z
[`konradcinkusz/math-for-ai-engineers`](https://github.com/konradcinkusz/math-for-ai-engineers),
którego **kod jest na MIT**.

## Obserwuj

[![GitHub followers](https://img.shields.io/github/followers/konradcinkusz?style=social)](https://github.com/konradcinkusz "GitHub followers")
[![GitHub stars](https://img.shields.io/github/stars/konradcinkusz/brain-train?style=social)](https://github.com/konradcinkusz/brain-train/stargazers "GitHub stars")

## Historia gwiazdek

<a href="https://star-history.com/#konradcinkusz/brain-train&Timeline">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=konradcinkusz/brain-train&type=Timeline&theme=dark" />
  <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=konradcinkusz/brain-train&type=Timeline" />
  <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=konradcinkusz/brain-train&type=Timeline" />
</picture>
</a>

<p align="right">(<a href="#readme-top">wróć na górę</a>)</p>
