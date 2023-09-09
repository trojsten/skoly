# Databáza škôl

Trojstenová databáza slovenských ZŠ + SŠ založená na verejných dátach z [RISPortal](https://crinfo.iedu.sk/RISPortal/register/).

Okrem verejných dát udržiavame školám vlastné názvy očistené od nepodstatných údajov zo štátnej databázy.

## Cieľ

Naším cieľom je vyrobiť a udržiavať databázu škôl pre potreby Trojstenu a jeho súťaží. Bohužiaľ, oficiálne dostupné
databázy neobsahujú kvalitné dáta - napríklad gymnázium ŠpMNDaG má názov "Elokované pracovisko ako súčasť Školy pre
mimoriadne nadané deti a GYMNÁZIUM", čo je možno ich oficiálny názov, ale pre naše potreby je to nepoužiteľné.

Výsledkom je zoznam škôl s názvom, skráteným názvom[^1], adresou a druhom školy.

## Pravidlá úpravy názvov

Názvy škôl upravujeme ručne, približné pravidlá toho, čo z názvov odstráňujeme:

- elokované pracoviská
- vyučovací jazyk
- cudzojazyčné preklady názvov
- "ako súčasť..."

Príklad:

- "Gymnázium Zoltána Kodálya s vyučovacím jazykom maďarským - Kodály Zoltán Gimnázium" → "Gymnázium Zoltána Kodálya"
- "Súkromná základná škola s materskou školou francúzsko-slovenská ako organizačná zložka  Súkromnej spojenej školy
  francúzsko-slovenskej" → "Súkromná základná škola s materskou školou"
- "Elokované pracovisko ako súčasť Základnej školy" → "Základná škola"

Zároveň sa snažíme upratať medzery a iné náhodné preklepy v oficiálnych dátach.

## Typy škôl

Typy škôl v oficiánych dátach sa nedajú jednoducho napárovať na typy, ktoré by sme chceli my, preto sme zaviedli
jednoduchý systém:

Typ školy sa skladá z dvoch častí:
- skupina škôl (`zs`, `ss`, `gym`)
- dĺžka štúdia v rokoch

Napríklad `gym:4`, `gym:8`, `zs:9`...

Tieto typy sa odvodzujú od študijných odborov škôl v oficiálnych databázach. Niektoré odbory bohužiaľ v týchto dátach
nemajú dĺžku štúdia, tie sú reprezentované iba skupinami škôl (pr. `ss`). Preto sa môže stať, že škola má typy `ss:4`,
`ss:3` a `ss`.

### `types`, `programmes` a `years`

V projekte sa používajú rôzne reprezentácie, ktoré reprezentujú rôzne koncepty, ale majú podobné názvy:

- `types` - reprezentuje typ školy, ako definuje stĺpec `TypSaSZKod`.
- `programme` - reprezentuje študijný odbor
- `year` - reprezentuje typ školy podľa nášho, vyššie uvedeného systému

## Aktualizácia dát

```shell
pipenv install
pipenv run python cli.py update-types
pipenv run python cli.py update-schools
# teraz možno aktualizovať data/schools.csv
# our_name, our_short pre nové / premenované školy

pipenv run python cli.py update-programmes
pipenv run python cli.py finalize
```

[^1]: zatiaľ používame oficiálne dáta, eventuálne budeme generovať vlastné
