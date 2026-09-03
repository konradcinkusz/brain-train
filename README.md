<a name="readme-top"></a>

# Trening Mózgu

[![Ask me anything](https://flat.badgen.net/static/Ask%20me/anything?icon=github&color=black&scale=1.01)](https://github.com/konradcinkusz "Ask me anything")
[![Licencja](https://flat.badgen.net/github/license/konradcinkusz/brain-train?icon=github&color=black&scale=1.01)](https://github.com/konradcinkusz/brain-train/blob/main/LICENSE "Licencja")
[![Utrzymywane](https://flat.badgen.net/static/Maintained/yes?icon=github&color=black&scale=1.01)](https://github.com/konradcinkusz/brain-train/commits/main "Utrzymywane")
[![Gałęzie](https://flat.badgen.net/github/branches/konradcinkusz/brain-train?icon=github&color=black&scale=1.01)](https://github.com/konradcinkusz/brain-train/branches "Gałęzie")
[![Commity](https://flat.badgen.net/github/commits/konradcinkusz/brain-train?icon=github&color=black&scale=1.01)](https://github.com/konradcinkusz/brain-train/commits/main "Commity")
[![Zgłoszenia](https://flat.badgen.net/github/issues/konradcinkusz/brain-train?icon=github&color=black&scale=1.01)](https://github.com/konradcinkusz/brain-train/issues "Zgłoszenia")
[![Pull requesty](https://flat.badgen.net/github/prs/konradcinkusz/brain-train?icon=github&color=black&scale=1.01)](https://github.com/konradcinkusz/brain-train/pulls "Pull requesty")
[![Wydanie](https://flat.badgen.net/github/release/konradcinkusz/brain-train?icon=github&color=black&scale=1.01)](https://github.com/konradcinkusz/brain-train/releases/latest "Najnowsze wydanie")
[![Build book](https://github.com/konradcinkusz/brain-train/actions/workflows/build.yml/badge.svg)](https://github.com/konradcinkusz/brain-train/actions/workflows/build.yml "Build book")

Zeszyt ćwiczeń na czas: arytmetyka, kolejność działań, procenty, ułamki,
potęgi, ciągi, zagadki logiczne i triki rachunkowe. **Nie liczy się pojedynczy
wynik — liczy się ile zadań zrobisz i jak szybko.**

**Dwa tomy.** Podstawowy: 4424 zadania, 113 zestawów, 110 stron, plan na 17
tygodni. Zaawansowany: 4032 zadania, 102 zestawy, 111 stron, plan na 16
tygodni. Razem **8456 zadań i 231 dni treningu**, dzień po dniu.

### [⬇ Pobierz PDF](https://github.com/konradcinkusz/brain-train/releases/latest/download/trening-mozgu-a4.pdf)

Gotowa książka z najnowszego wydania — bez LaTeX-a, bez budowania. A4, do druku
dwustronnego.

## Quick start

```bash
git clone https://github.com/konradcinkusz/brain-train.git
cd brain-train
make book
```

Potrzebujesz `pdflatex`, `latexmk` i `python3`. Gotowy PDF powstaje jako
`book/main-pl-a4.pdf`.

## Jak działa format

Zadania są zebrane w **zestawy** — jedno pod drugim, po 40 w każdym zestawie
rachunkowym. Zestaw robisz w całości, na stoper, i notujesz czas oraz wynik pod
spodem. **Wszystkie odpowiedzi są na końcu książki**, nigdy obok zadania.

```
ZESTAW 1   Dodawanie dwucyfrowe              ★☆☆   ⏱ cel: 3:20
─────────────────────────────────────────────────────────────────
  1. 18 + 36  ____     15. 75 + 89  ____     28. 55 + 32  ____
  2. 22 + 82  ____     16. 30 + 13  ____     29. 62 + 15  ____
  3. 59 + 31  ____     17. 83 + 23  ____     30. 30 + 23  ____
  ...                  ...                   ...
 14. 89 + 35  ____     27. 22 + 50  ____     40. 15 + 18  ____
─────────────────────────────────────────────────────────────────
1.  Czas: ________   Poprawne: ____ / 40   Data: ________
2.  Czas: ________   Poprawne: ____ / 40   Data: ________
```

**Dwa wiersze, nie jeden.** Książka od początku każe wrócić do zestawu po
tygodniu i porównać — i dawała na to jedną linijkę. Plan wyznacza tę powtórkę
na konkretny dzień dla większości zestawów, więc drugi pomiar musi mieć gdzie
usiąść, obok pierwszego. Zestawy kontrolne mają pięć wierszy.

Każdy zestaw rachunkowy ma tyle samo zadań, bo dwa czasy da się porównać tylko
wtedy, gdy mierzą tę samą pracę. Zestaw nigdy nie jest rozbity między strony —
rubryka z czasem stoi pod zadaniami, które opisuje, i pilnuje tego bramka
w buildzie.

Rubryka na datę jest tam celowo: jeden pomiar nie mówi nic. Wracasz do tego
samego zestawu za tydzień i porównujesz — ten sam zestaw, krótszy czas, mniej
pomyłek.

Odpowiedzi z tyłu mają w żywej paginie zakres zestawów na stronie
(`Odpowiedzi 26–37`), bo osiem stron tablicy bez tego przegląda się palcem.

## Dwa tomy, i czym się różnią

| | **Trening Mózgu** | **Trening Mózgu — Zaawansowany** |
|---|---|---|
| dla kogo | od zera | po pierwszym tomie |
| co ćwiczy | rachunki: cztery działania, procenty, ułamki dziesiętne, kolejność | operacje, których w pierwszym nie ma wcale |
| bloki | Fundament · Tempo · Wyzwanie · Mistrzostwo | Systemy i reszty · Struktura liczby · Ułamki i potęgi · Zastosowania |
| zestawy | 113 | 102 |
| zadania | 4424 | 4032 |
| plan | 119 dni / 17 tygodni | 112 dni / 16 tygodni |

**Drugi tom to nie pierwszy z większymi liczbami.** Pierwszy kończy się na
dodawaniu pięciocyfrowym, mnożeniu trzycyfrowego przez dwucyfrowe i procencie
składanym — dopisanie jeszcze jednej cyfry daje działanie *dłuższe*, a nie
trudniejsze. Drugi tom robi rzeczy, których w pierwszym nie ma:

- **systemy pozycyjne** — dwójkowy i szesnastkowy, w obie strony
- **arytmetyka modularna** — reszty, potęgi modulo, cyfra kontrolna
- **struktura liczby** — czynniki pierwsze, liczba dzielników, Euklides
- **ułamki mnożone i dzielone**, wykładnik ujemny i ułamkowy, logarytmy,
  notacja naukowa
- **zastosowania, w których intuicja zawodzi** — średnia prędkość tam
  i z powrotem, procent przez lata, kombinatoryka, dzień tygodnia z daty

Reguły gry są te same: czterdzieści zadań w zestawie, w pamięci, na stoper,
odpowiedzi na końcu książki. Oba tomy dzielą preambułę, bramki i CI — nie są
osobnymi projektami, tylko dwiema listami zestawów nad jedną maszynerią.

## Plan na 17 tygodni

119 dni, jeden zestaw dziennie, kwadrans. Kto zatrzyma się po trzynastu
tygodniach, i tak skończył kurs — czwarty blok jest nadprogramowy. Książki można używać bez planu — po
kolei — ale plan zdejmuje z Ciebie codzienną decyzję, co robić, i układa
kolejność tak, żeby nie była przypadkowa:

- **Rosnące obciążenie** — cztery tygodnie Bloku I, pięć Bloku II, cztery
  Bloku III i cztery Bloku IV.
- **Przeplot** — dwa dni pod rząd nigdy nie ćwiczą tej samej rodziny zadań.
  Sześć zestawów dodawania w sześć dni idzie *szybciej*, gdy się je robi,
  i zostaje w głowie gorzej.
- **Odstęp** — każdy dzień po pierwszym tygodniu powtarza zestaw sprzed
  siedmiu dni, przeciwko czasowi już zapisanemu pod spodem. To jest ten pomiar,
  dla którego ta książka istnieje.
- **Co siódmy dzień pomiar kontrolny** — ten sam zestaw co tydzień, z pięcioma
  wierszami na wynik, więc cztery pomiary widać obok siebie, a nie w czterech
  miejscach książki. Do tego **siatka na wykres** — pięć liczb w kolumnie to
  tabela, pięć punktów na siatce to trend.

```
Tydzień 2   Blok I — Fundament
──────────────────────────────────────────────────────────────────────────
 Dzień  Zestaw dnia                    Cel   Powt.  Data     Czas   Poprawne
     8  4 · Dzielenie w tabliczce     3:20      1   ______  ______  ____/40
     9  11 · Jednostki                3:20      3   ______  ______  ____/40
    10  8 · Tabliczka mnożenia II     2:40      7   ______  ______  ____/40
   ...
    14  86 · Pomiar kontrolny I       3:40      —   ______  ______  ____/40
```

Plan jest **generowany** z listy zestawów, nie pisany ręcznie: 91 wierszy
wpisanych z palca to 91 okazji, żeby wskazać zestaw, który się przesunął.
A żeby numer w planie nie mógł się rozjechać z numerem w książce, każdy zestaw
jest wstawiany z oczekiwanym numerem i **przerywa build**, jeśli wypadnie pod
innym.

Trzy zasady wyżej są wnioskami z badań nad ćwiczeniem, a nie pomiarem tej
książki — nikt jeszcze nie przerobił tego planu, i książka mówi to wprost.

## Trzy bloki, rosnąca trudność

Każdy blok to osobny rozdział. Kolejność w książce jest drabiną: zaczynasz od
rzeczy, które umiesz, i kończysz na takich, które trzeba rozłożyć na kroki.

| Blok | Gwiazdki | Co ćwiczysz | Zestawów |
|---|---|---|---|
| **I — Fundament** | ★ | dwie cyfry, tabliczka, dopełnienia, jednostki, równania jednokrokowe | 24 |
| **II — Tempo** | ★★ | trzy cyfry, procenty, ułamki, reszty, potęgi, kolejność działań | 34 |
| **III — Wyzwanie** | ★★★ | cztery cyfry, mnożenie dwucyfrowe, nawiasy z potęgami, procent od drugiej strony | 23 |
| **IV — Mistrzostwo** | ★★★ | równania dwukrokowe, ułamki o różnych mianownikach, procent składany, działania poniżej zera, jednostki kwadratowe | 24 |
| **Łamigłówki** | ★★ | zagadki, ciągi, triki — pisane ręcznie | 4 |
| **Pomiary kontrolne** | ★–★★★ | po jednym na blok, pięć wierszy na pomiar | 4 |

Gwiazdki opisują **zestaw**, nie pojedyncze zadanie. Cel czasowy też: to
sekundy na zadanie razy długość zestawu, więc rośnie razem z pracą, a nie
dlatego, że ktoś go zgadł.

## Struktura repozytorium

```
.
├── book/
│   ├── main-pl-a4.tex                # Tom I — cienki, format jest w preambule
│   ├── main-pl-a4-adv.tex            # Tom II — różni się pięcioma liniami
│   ├── preamble.tex                  # Zestaw, \z, magazyn odpowiedzi
│   ├── structure.tex                 # JEDNA lista zestawów tomu I
│   ├── structure-adv.tex             #   i jedna tomu II
│   ├── frontmatter/                  # Tytuł, „Jak korzystać”, plan
│   ├── plan/generated/               # GENEROWANE — tabele planu i jego liczby
│   ├── plan-adv/generated/           #   to samo dla tomu II
│   ├── sets-adv/                     # Tom II: zestawy ręczne i generowane
│   └── sets/
│       ├── 20-zagadki.tex            # Pisane ręcznie: zagadki, ciągi,
│       ├── 21-ciagi.tex              #   wyzwania, triki — tego się nie generuje
│       ├── 22-mieszane.tex
│       ├── 23-triki.tex
│       └── generated/                # GENEROWANE (make sets) — 109 zestawów
│           └── _blok-*.tex           #   listy \input, jedna na rozdział
├── tools/
│   ├── gen_sets.py                   # Generator zestawów + bramka drift
│   ├── gen_sets_adv.py               # Tom II: własne buildery i lista
│   ├── gen_plan.py                   # Generator planów obu tomów
│   ├── checkanswers.py               # Przelicza odpowiedzi drugą ścieżką
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

## Druk

Książka jest złożona pod **druk dwustronny** i to zostało zmierzone na gotowym
PDF-ie, nie założone:

- **Margines na oprawę stoi po wewnętrznej stronie** i odbija się jak trzeba —
  1,8 cm od grzbietu, 1,5 cm od krawędzi zewnętrznej, na każdej stronie
  parzystej i nieparzystej. Zamienione stronami zszyłyby się w tekst i nic
  w buildzie by tego nie zgłosiło.
- **Rozdziały zaczynają się na nieparzystej.** Kosztuje to kilka pustych
  stron — są puste celowo i nie niosą ani żywej paginy, ani numeru.
- **Żaden zestaw nie jest rozbity między strony**, pilnuje tego bramka
  w buildzie, a odpowiedzi są wszystkie z tyłu, więc zestaw nigdy nie dzieli
  rozkładówki ze swoimi odpowiedziami.

Drukuj na A4, dwustronnie, **odbicie wzdłuż dłuższej krawędzi**. Zszywka albo
spirala po lewej.

## Budowanie

| Cel | Co robi |
|---|---|
| `make books` | Buduje **oba tomy** i uruchamia wszystkie bramki |
| `make book` | Sam tom podstawowy |
| `make book-adv` | Sam tom zaawansowany |
| `make sets` | Regeneruje zestawy i plany obu tomów |
| `make plan` | Regeneruje same plany |
| `make drift` | Sprawdza, czy wygenerowane zestawy są aktualne |
| `make answers` | Przelicza każdą odpowiedź z wydrukowanego pytania |
| `make check` | Same bramki, bez budowania |
| `make clean` | Usuwa artefakty |

Bramki, każda sprawdza coś, czego pozostałe nie widzą:

- **`tools/checklog.py`** — błędy, nierozwiązane referencje, przepełnione pudełka
  i brak zbieżności. To jest bramka, **nie kod wyjścia `latexmk`**: przy
  `nonstopmode` nieudany przebieg i tak zapisuje PDF, a przy `-file-line-error`
  linia błędu zaczyna się od ścieżki, więc `grep '^!'` też jej nie widzi.
- **`tools/gen_sets.py --check`** — zestawy rachunkowe są generowane; zmiana
  generatora bez regeneracji zostawia w książce starą wersję, a oba pliki są
  poprawne, więc reszta bramek świeci na zielono. Ta sama bramka pilnuje listy
  `\input`-ów: zestaw dodany do generatora i zapomniany w liście to zestaw,
  którego nikt nigdy nie zobaczy.

- **`tools/checkanswers.py`** — czyta `.tex`, który wchodzi do builda, parsuje
  pytanie tak, jak widzi je czytelnik, i liczy odpowiedź **drugą ścieżką**.
  Generator gwarantuje, że odpowiedź zgadza się z pytaniem, bo liczy oba z tych
  samych liczb — ale builder pomylony konsekwentnie (minus zamiast plusa,
  procent od złej liczby) wydrukuje zgodną parę. To jedyna bramka, która patrzy
  na stronę, a nie na kod, który ją zrobił. **Kształt pytania, którego nie zna,
  jest błędem, nie pominięciem** — inaczej przestałaby mierzyć w dniu, w którym
  ktoś doda buildera.

- **`tools/gen_plan.py --check`** — plan wskazuje zestawy po numerach, więc
  zmiana listy zestawów bez regeneracji planu wysyła czytelnika pod zły numer,
  a plik nadal jest poprawnym LaTeX-em.

Dwie bramki siedzą w preambule, nie w `tools/`, bo obie potrzebują liczb, które
istnieją dopiero w trakcie składania. Pierwsza: listy `\input` niosą numer,
pod którym zestaw ma wypaść, a zestaw, który wypadnie pod innym (albo bez
żadnego), **przerywa build** — inaczej przestawienie rozdziału przesunęłoby
cały plan o jeden zestaw, po cichu. Druga: każdy zestaw ma etykietę
w nagłówku i w stopce, a build **przerywa się błędem**, jeśli obie wypadną na
różnych stronach. Zestaw rozbity między strony to rubryka z czasem po drugiej
stronie kartki niż zadania, które ocenia — a ta rubryka jest w tej książce
najważniejsza.

Generator liczy odpowiedzi tym samym kodem, który układa zadania, więc
wydrukowana odpowiedź nie może nie zgadzać się ze swoim zadaniem — a
`make answers` sprawdza jeszcze, czy sam kod nie liczy konsekwentnie źle.

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

Dwie drogi, obie kończą się tym samym: zbudowaną książką załączoną do wydania.

**Tag.** Wypchnij `v*` lub `V*`:

```bash
git tag v2.0.0
git push origin v2.0.0
```

**Albo bez lokalnego klona:** *Actions → Release book PDF → Run workflow*, wersja
w polu `version`. Workflow tworzy tag sam, swoim tokenem
([#35](https://github.com/konradcinkusz/brain-train/pull/35)).

Wydanie powstaje tylko wtedy, gdy build przejdzie wszystkie bramki — job wydania
deklaruje `needs: build`, więc inaczej w ogóle się nie uruchamia. To celowe:
wydanie `v1.0.0` nie ma załączonego PDF-a, bo jego build się nie powiódł, a nikt
tego nie zauważył ([#21](https://github.com/konradcinkusz/brain-train/issues/21)).

**Wydanie sprawdza się po załącznikach, nie po zielonym workflow.** `v1.0.0`
jest tego przykładem: istnieje, nie jest szkicem i nie niesie niczego.

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
