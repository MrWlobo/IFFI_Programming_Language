# Dokumentacja języka programowania IFFI

---

## Dane studentów

- Mateusz Battek - mbattek@student.agh.edu.pl
- Michał Dworniczak - mdwornic@student.agh.edu.pl

---

## Założenia programu

### Ogólne cele

Cel projektu to stworzenie języka, który jest połączeniem kilku
popularnych języków takich jak: Ada, Java i Python.

### Rodzaj translatora

- **Rodzaj:** Kompilator

### Planowany wynik działania programu

Kompilator języka IFFI do C

### Język implementacji

- **Python 3.13+**

### Realizacja parsera

- **Narzędzie:** ANTLR 4
- **Gramatyka:** opisana w pliku `Iffi.g4`

---

## Tabela tokenów języka IFFI

### Proste typy danych

| Token         | Opis                     | Przykład |
|---------------|--------------------------|----------|
| `TYPE_INT`    | typ danych całkowitych   | `int`    |
| `TYPE_FLOAT`  | typ zmiennoprzecinkowy   | `float`  | 
| `TYPE_BOOL`   | typ logiczny             | `bool`   |
| `TYPE_CHAR`   | typ znakowy              | `char`   |
| `TYPE_STRING` | typ tekstowy             | `string` |

### Złożone typy danych

| Token       | Opis                                       | Przykład |
|-------------|--------------------------------------------|----------|
| `TYPE_LIST` | lista                                      | `list`   |
| `RANGE`     | lista liczb całkowitych z podanego zakresu | `range`  |
 

### Operatory matematyczne i logiczne

| Token             | Opis                    | Przykład |
|-------------------|-------------------------|----------|
| `PLUS`            | dodawanie               | `+`      |
| `MINUS`           | odejmowanie             | `-`      |
| `MULTIPLY`        | mnożenie                | `*`      |
| `DIVIDE`          | dzielenie               | `/`      |
| `FLOOR_DIVIDE`    | dzielenie bez reszty    | `//`     |
| `MODULO`          | reszta z dzielenia      | `%`      |
| `POWER`           | potęgowanie             | `**`     |
| `INCREMENT`       | inkrementacja           | `++`     |
| `DECREMENT`       | dekrementacja           | `--`     |
| `EQUAL`           | równe                   | `==`     |
| `NOT_EQUAL`       | nierówne                | `!=`     |
| `LESS_THAN`       | mniejsze                | `<`      |
| `LESS_EQUAL`      | mniejsze/równe          | `<=`     |
| `GREATER_THAN`    | większe                 | `>`      |
| `GREATER_EQUAL`   | większe/równe           | `>=`     |
| `AND`             | operator logiczny "AND" | `AND`    |
| `OR`              | operator logiczny "OR"  | `OR`     |
| `NOT`             | operator logiczny "NOT" | `NOT`    |
| `ASSIGN`          | przypisanie             | `=`      |
| `ASSIGN_PLUS`     | przypisanie dodawania   | `+=`     |
| `ASSIGN_MINUS`    | przypisanie odejmowania | `-=`     |
| `ASSIGN_MULTIPLY` | przypisanie mnożenia    | `*=`     |
| `ASSIGN_DIVIDE`   | przypisanie dzielenia   | `/=`     |



### Znaki specjalne i separatory

| Token           | Opis                          | Przykład |
|-----------------|-------------------------------|----------|
| `LEFT_PAREN`    | nawias otwierający            | `(`      |
| `RIGHT_PAREN`   | nawias zamykający             | `)`      |
| `LEFT_BRACKET`  | nawias kwadratowy otwierający | `[`      |
| `RIGHT_BRACKET` | nawias kwadratowy zamykający  | `]`      |
| `LEFT_BRACE`    | nawias klamrowy otwierający   | `{`      |
| `RIGHT_BRACE`   | nawias klamrowy zamykający    | `}`      |
| `SEMICOLON`     | średnik                       | `;`      |
| `COMMA`         | przecinek                     | `,`      |
| `COLON`         | koniec instrukcji blokowej    | `:`      |
| `ARROW`         | strzałka                      | `->`     |
| `HASHTAG`       | jednoliniowy komentarz        | `#`      |


### Słowa kluczowe

| Token       | Opis                                  | Przykład  |
|-------------|---------------------------------------|-----------|
| `T_IF`      | instrukcja warunkowa if               | `IF`      |
| `T_ELIF`    | instrukcja elif                       | `ELIF`    |
| `T_ELSE`    | instrukcja else                       | `ELSE`    |
| `T_FI`      | instrukcja fi                         | `FI`      |
| `T_LOOP`    | instrukcja rozpoczęcia pętli          | `LOOP`    |
| `T_POOL`    | instrukcja zakończenia pętli          | `POOL`    |
| `T_FOR`     | pętla for                             | `FOR`     |
| `T_WHILE`   | pętla while                           | `WHILE`   |
| `T_DO`      | pętla do while                        | `DO`      |
| `T_IN`      | iteracja po elementach struktury      | `IN`      |
| `T_STOP`    | zakończenie działania pętli           | `STOP`    |
| `T_SKIP`    | przejście do następnej iteracji pętli | `SKIP`    |
| `T_FUNC`    | deklaracja funkcji                    | `FUNC`    |
| `T_CNUF`    | zakończenie delaracji funkcji         | `CNUF`    |
| `T_RETURN`  | zwrócenie wartości z funkcji          | `RETURN`  |


### Inne tokeny

| Token        | Opis       | Przykład                 |
|--------------|------------|--------------------------|
| `IDENTIFIER` | identyfikator | `zmienna`, `mojaFunkcja` |
| `WHITE_SPACE`| biały znak | ` `, `\n`, `\t`           |

---

---

## Instrukcja użycia

### 1. Wymagania
* Pyton 3.10+
* pip
* gcc (https://phoenixnap.com/kb/install-gcc-windows)

### 2. Przygotowanie i instalacja
Aby uruchomić projekt lokalnie należy sklonować repozytorium:
```bash
git clone https://github.com/MrWlobo/IFFI_Programming_Language.git
cd parser
pip install -r requirements.txt
```

### 3. Wygenerowanie parsera z gramatyki:
Wykonać tylko, jeśli nie ma folderu `antlr_output/` lub dokonano zmian w gramatyce.
```bash
antlr -Dlanguage=Python3 Iffi.g4 -o antlr_output -visitor
```

### 4. Uruchomienie GUI

```bash
py gui_app.py
```


---

## Przykład użycia

![Widok GUI](./pics/widok.png)

![Widok Dark GUI](./pics/widok_dark.png)

## Gramatyka

[Gramatyka](./parser/Iffi.g4)

## Przykładowy kod źródłowy w języku IFFI

```iffi
FUNC myFunc(a: int, b: int) -> int:
    int c = a + b;
    return c;
CNUF

int fa = 7;
LOOP:
    fa = fa + 8;
    IF (fa > 100):
        print(fa);
        stop;
    FI
    #komentarz
POOL

LIST[int] lista = [1, 2, 3, 8, 99, 123];
LIST[int] lista1 = [3, 2, 1];

LOOP FOR (int i IN lista):
    LOOP FOR (int j IN lista1):
        print(j+i);
    POOL
POOL

print(myFunc(fa, fa));
```