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

Zeszyt ćwiczeń na czas: arytmetyka, kolejność działań, procenty, ciągi,
zagadki logiczne i triki rachunkowe. **Nie liczy się pojedynczy wynik — liczy
się ile zadań zrobisz i jak szybko.**

**434 zadania · 18 zestawów · 16 stron A4.**

## Quick start

```bash
git clone https://github.com/konradcinkusz/brain-train.git
cd brain-train
make book
```

Potrzebujesz `pdflatex`, `latexmk` i `python3`. Gotowy PDF powstaje jako
`book/main-pl-a4.pdf`.

## Jak działa format

Zadania są zebrane w **zestawy** — po 24--30 na stronie, jedno pod drugim.
Zestaw robisz w całości, na stoper, i notujesz czas oraz wynik pod spodem.
**Wszystkie odpowiedzi są na końcu książki**, nigdy obok zadania.

```
ZESTAW 1   Dodawanie dwucyfrowe              ★☆☆   ⏱ cel: 2:30
─────────────────────────────────────────────────────────────────
  1. 18 + 36  ____     11. 75 + 89  ____     21. 55 + 32  ____
  2. 22 + 82  ____     12. 30 + 13  ____     22. 62 + 15  ____
  3. 59 + 31  ____     13. 83 + 23  ____     23. 30 + 23  ____
  ...                  ...                   ...
 10. 89 + 35  ____     20. 22 + 50  ____     30. 15 + 18  ____
─────────────────────────────────────────────────────────────────
Czas: ________   Poprawne: ____ / 30   Data: ________
```

Rubryka na datę jest tam celowo: jeden pomiar nie mówi nic. Wracasz do tego
samego zestawu za tydzień i porównujesz — ten sam zestaw, krótszy czas, mniej
pomyłek.

## Poziomy trudności

Gwiazdki opisują **zestaw**, nie pojedyncze zadanie:

| Gwiazdki | Zestaw |
|----------|--------|
| ★ | rozgrzewka |
| ★★ | normalne tempo |
| ★★★ | trudniejsze — tu czas rośnie |

## Struktura repozytorium

```
.
├── book/
│   ├── main-pl-a4.tex                # Plik główny — cienki, format jest w preambule
│   ├── preamble.tex                  # Zestaw, \z, magazyn odpowiedzi
│   ├── structure.tex                 # JEDNA lista zestawów
│   ├── frontmatter/                  # Strona tytułowa, „Jak korzystać”
│   └── sets/
│       ├── 20-zagadki.tex            # Pisane ręcznie: zagadki, ciągi,
│       ├── 21-ciagi.tex              #   wyzwania, triki — tego się nie generuje
│       ├── 22-mieszane.tex
│       ├── 23-triki.tex
│       └── generated/                # GENEROWANE (make sets) — 14 zestawów rachunków
├── tools/
│   ├── gen_sets.py                   # Generator zestawów + bramka drift
│   └── checklog.py                   # Bramka logu (nie kod wyjścia!)
├── deck-archive/                     # Poprzednie wersje — nie budowane
├── .github/workflows/
│   ├── build.yml                     # Build na każdy push i PR
│   └── ci.yml                        # Build + wydanie PDF na tag v*/V*
├── Makefile
├── CLAUDE.md                          # Decyzje i pułapki — czytaj przed zmianami
├── CONTRIBUTING.md
├── LICENSE
└── README.md
```

## Budowanie

| Cel | Co robi |
|---|---|
| `make book` | Buduje książkę i uruchamia wszystkie bramki |
| `make sets` | Regeneruje zestawy rachunkowe |
| `make drift` | Sprawdza, czy wygenerowane zestawy są aktualne |
| `make check` | Same bramki, bez budowania |
| `make clean` | Usuwa artefakty |

Trzy bramki, każda sprawdza coś, czego pozostałe nie widzą:

- **`tools/checklog.py`** — błędy, nierozwiązane referencje, przepełnione pudełka
  i brak zbieżności. To jest bramka, **nie kod wyjścia `latexmk`**: przy
  `nonstopmode` nieudany przebieg i tak zapisuje PDF, a przy `-file-line-error`
  linia błędu zaczyna się od ścieżki, więc `grep '^!'` też jej nie widzi.
- **`tools/gen_sets.py --check`** — zestawy rachunkowe są generowane; zmiana
  generatora bez regeneracji zostawia w książce starą wersję, a oba pliki są
  poprawne, więc reszta bramek świeci na zielono. Ta sama bramka pilnuje listy
  `\input`-ów: zestaw dodany do generatora i zapomniany w liście to zestaw,
  którego nikt nigdy nie zobaczy.

Generator liczy odpowiedzi tym samym kodem, który układa zadania, więc
wydrukowana odpowiedź nie może nie zgadzać się ze swoim zadaniem.

<p align="right">(<a href="#readme-top">wróć na górę</a>)</p>

### Dlaczego rachunki są generowane

Bo książkę ocenia się liczbą zadań, a kilkaset ręcznie wpisanych sum to miejsce,
w którym chowają się pomyłki. Każde zadanie i jego odpowiedź powstają z tych
samych trzech linijek kodu. Generator jest deterministyczny (stały seed), więc
książka jest identyczna przy każdym buildzie — inaczej nie dałoby się porównać
dzisiejszego czasu z zeszłotygodniowym.

Zagadek, ciągów i trików **się nie generuje** — pułapka słowna to żart, a żart
ma autora. Te siedzą w `book/sets/` i pisze się je ręcznie.

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
