# BrainTrain 2025

[![Build book](https://github.com/konradcinkusz/brain-train/actions/workflows/build.yml/badge.svg)](https://github.com/konradcinkusz/brain-train/actions/workflows/build.yml "Build book")
[![Licencja](https://flat.badgen.net/github/license/konradcinkusz/brain-train?icon=github&color=black&scale=1.01)](https://github.com/konradcinkusz/brain-train/blob/main/LICENSE "Licencja")
[![Zgłoszenia](https://flat.badgen.net/github/issues/konradcinkusz/brain-train?icon=github&color=black&scale=1.01)](https://github.com/konradcinkusz/brain-train/issues "Zgłoszenia")

Zbiór krótkich zadań wzmacniających obie półkule mózgu — arytmetyka na czas, kolejność działań, zagadki logiczne, ciągi liczbowe i wyzwania mieszane. Format inspirowany książkami z serii *Trening Mózgu*: jedno zadanie, stoper, porównaj z podanym limitem czasu. Bez kalkulatora!

## Quick start

```bash
git clone https://github.com/konradcinkusz/brain-train.git
cd brain-train
make book
```

## Struktura repozytorium

```
.
├── areas/                             # ŹRÓDŁO zadań (38 w pięciu obszarach)
│   ├── 1-arytmetyka-podstawy.tex     # Dodawanie, odejmowanie, mnożenie, dzielenie
│   ├── 2-kolejnosc-dzialan.tex       # Nawiasy, priorytety, potęgi
│   ├── 3-zagadki-logiczne.tex        # Sylogizmy, pułapki słowne, dedukcja
│   ├── 4-ciagi-i-wzorce.tex          # Ciągi liczbowe i literowe
│   └── 5-mieszane-wyzwania.tex       # Prędkość, procenty, finanse, praca
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
├── main.tex                           # Prezentacja Beamer (patrz #16, #21)
├── mybraintrainer.cls / .sty          # Klasa i makra prezentacji
├── .github/workflows/
│   ├── build.yml                     # Build książki na każdy push i PR
│   └── ci.yml                        # Build + wydanie PDF na tag v*/V*
├── Makefile
├── LICENSE
└── README.md
```

## Książka (w budowie)

Zbiór jest przenoszony do formatu **książki A4** w układzie Stroudowskim: jedno
zadanie na ramkę, numer ramki na zewnętrznym marginesie, odpowiedź otwiera
ramkę następną — zakrywasz stronę dłonią, liczysz na czas, czytasz dalej.

```bash
make book     # zbuduj książkę i sprawdź log
make convert  # przenieś areas/ do book/chapters/
make help     # pozostałe cele
```

Wszystkie **38 zadań** z pięciu obszarów są już w książce (`book/`, 18 stron).
Rozdziały w `book/chapters/` są **generowane** z `areas/` przez
`tools/convert_deck.py` — edytuj `areas/` i uruchom `make convert`; `make book`
sprawdza, czy nie rozjechały się z sobą. Całość opisuje
[#14](https://github.com/konradcinkusz/brain-train/issues/14).

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

Wypchnij tag `v*` lub `V*`, aby zbudować książkę i dołączyć PDF
(`trening-mozgu-a4.pdf`) do wydania:

```bash
git tag v2.0.0
git push origin v2.0.0
```

Wydanie powstaje tylko wtedy, gdy build przejdzie wszystkie bramki — inaczej
job wydania w ogóle się nie uruchamia. To celowe: wydanie `v1.0.0` nie ma
załączonego PDF-a, bo jego build się nie powiódł, a nikt tego nie zauważył
([#21](https://github.com/konradcinkusz/brain-train/issues/21)).

## Wkład

Fork, otwórz issue lub pull request — nowe zadania mile widziane!

## Licencja

MIT No Attribution — szczegóły w [LICENSE](LICENSE).
