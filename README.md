# BrainTrain 2025

![CI](https://github.com/konradcinkusz/BrainTrain/actions/workflows/ci.yml/badge.svg)
![PDF](https://img.shields.io/github/v/release/konradcinkusz/BrainTrain?label=PDF)

Zbiór krótkich zadań wzmacniających obie półkule mózgu — arytmetyka na czas, kolejność działań, zagadki logiczne, ciągi liczbowe i wyzwania mieszane. Format inspirowany książkami z serii *Trening Mózgu*: jedno zadanie, stoper, porównaj z podanym limitem czasu. Bez kalkulatora!

## Quick start

```bash
git clone https://github.com/konradcinkusz/BrainTrain.git
cd BrainTrain
latexmk -xelatex main.tex
```

## Struktura repozytorium

```
.
├── main.tex                           # Główny plik LaTeX
├── mybraintrainer.cls                 # Klasa Beamer (kolory, stopka, fontawesome)
├── mybraintrainer.sty                 # Makra: \ExerciseSlide, \AnswerSlide
├── areas/
│   ├── 1-arytmetyka-podstawy.tex     # Dodawanie, odejmowanie, mnożenie, dzielenie
│   ├── 2-kolejnosc-dzialan.tex       # Nawiasy, priorytety, potęgi
│   ├── 3-zagadki-logiczne.tex        # Sylogizmy, pułapki słowne, dedukcja
│   ├── 4-ciagi-i-wzorce.tex          # Ciągi liczbowe i literowe
│   └── 5-mieszane-wyzwania.tex       # Prędkość, procenty, finanse, praca
├── .github/workflows/ci.yml           # Build & Release PDF on version tag
├── LICENSE
└── README.md
```

## Książka (w budowie)

Zbiór jest przenoszony do formatu **książki A4** w układzie Stroudowskim: jedno
zadanie na ramkę, numer ramki na zewnętrznym marginesie, odpowiedź otwiera
ramkę następną — zakrywasz stronę dłonią, liczysz na czas, czytasz dalej.

```bash
make book     # zbuduj książkę i sprawdź log
make help     # pozostałe cele
```

Szkielet (`book/`) zawiera na razie jeden rozdział z trzema zadaniami; pozostałe
35 zadań przenosi [#17](https://github.com/konradcinkusz/brain-train/issues/17).
Całość opisuje [#14](https://github.com/konradcinkusz/brain-train/issues/14).

> `make book` nie ufa kodowi wyjścia `latexmk`: przy `nonstopmode` nieudany
> przebieg i tak zapisuje PDF, a przy `-file-line-error` linia błędu zaczyna się
> od ścieżki, więc `grep '^!'` też jej nie widzi. Bramką jest
> `tools/checklog.py`.

## Poziomy trudności

| Gwiazdki | Poziom | Czas docelowy |
|----------|--------|---------------|
| ★ | Łatwy | do 1 min |
| ★★ | Średni | 1–3 min |
| ★★★ | Trudny | 3–5 min |

## Wydanie PDF

Wypchnij tag `v*`, aby wyzwolić GitHub Actions i opublikować PDF w GitHub Releases:

```bash
git tag v1.0.0
git push origin v1.0.0
```

## Wkład

Fork, otwórz issue lub pull request — nowe zadania mile widziane!

## Licencja

MIT No Attribution — szczegóły w [LICENSE](LICENSE).
