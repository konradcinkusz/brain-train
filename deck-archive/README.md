# Prezentacja Beamer — zarchiwizowana

Tu leży oryginalna prezentacja Beamer, od której zaczęło się to repozytorium.
**Nie jest budowana i nie jest utrzymywana.** Zdecydowano to w
[#16](https://github.com/konradcinkusz/brain-train/issues/16); dowody są w
[#21](https://github.com/konradcinkusz/brain-train/issues/21).

## Dlaczego tu trafiła

Prezentacja **nigdy się nie zbudowała**. Jej jedyny przebieg CI —
[run 29702584227](https://github.com/konradcinkusz/brain-train/actions/runs/29702584227),
19 lipca 2026 — zakończył się błędem, przez co wydanie `v1.0.0` nie ma
załączonego żadnego pliku.

Przyczyna: `mybraintrainer.cls` ładuje `[T1]{fontenc}` i `[utf8]{inputenc}`,
czyli stos czcionek pdfTeX-a, a workflow uruchamiał **XeLaTeX**. Pod XeLaTeX-em
wybiera to czcionki EC, które nie mają polskich znaków:

```
Missing character: There is no ś ("15B) in font ec-lmss8!
Missing character: There is no ż ("17C) in font ec-lmss12!
```

Każdy diakrytyk był po cichu gubiony. Książka używa pdfLaTeX-a, gdzie ten sam
stos jest poprawny.

## Dlaczego archiwum, a nie usunięcie

Archiwizujemy, nie kasujemy i nie komentujemy — to konwencja z
[REPO-BASELINE](https://github.com/konradcinkusz/architecture-standards/blob/main/docs/guides/REPO-BASELINE.md)
§5. Pliki znikają z korzenia repozytorium, ale zostają w historii i dają się
przywrócić jedną komendą.

`areas/*.tex` **nadal używa makr `\ExerciseSlide` i `\AnswerSlide`**
zdefiniowanych tutaj w `mybraintrainer.sty`. To celowe: gdyby ktoś kiedyś
chciał wrócić do prezentacji, treść zadań jest wciąż w formacie, który ta
prezentacja rozumie.

## Gdyby ktoś chciał ją naprawić

Dwie drogi, obie opisane w #21: zbudować ją pdfLaTeX-em (`latexmk_use_xelatex`
na `false`), albo zostawić XeLaTeX i zamienić `fontenc`/`inputenc` na `fontspec`
z czcionką mającą polskie znaki. Nikt tego nie potrzebuje — książka jest
formatem, który to repozytorium wydaje.

## Co jeszcze tu trafiło

`areas/` oraz `tools/convert_deck.py` i `tools/checkbadges.py` — cały łańcuch
poprzedniej wersji książki, w której każde zadanie miało własną ramkę, a
odpowiedź otwierała ramkę następną.

Ta struktura była zła dla tej książki i została zastąpiona zestawami
(`book/sets/`). Powód jest prosty: książka mierzy **ile zadań zrobisz i jak
szybko**, a ramka na zadanie mieściła dwa zadania na stronie i wstawiała
odpowiedź w środek serii. Teraz jest ~30 zadań na stronie, jeden pomiar na
zestaw i wszystkie odpowiedzi na końcu.

Treść zadań pisanych ręcznie (zagadki, ciągi, wyzwania, triki) została
przepisana do `book/sets/` i **to tam się ją teraz edytuje**. Kopia w `areas/`
jest historyczna.

`checkbadges.py` pilnował numerów ramek na zewnętrznym marginesie. Marginesy nie
mają już numerów, więc sprawdzenie nie mierzy niczego i zostało wyłączone z
bramek, a nie zostawione jako zielone-zawsze.
