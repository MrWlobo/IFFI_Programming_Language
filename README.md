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

| Token         | Opis         | Przykład |
|---------------|--------------|----------|
| `TYPE_ARRAY`  | tablica      | `array`  |
| `TYPE_LIST`   | lista        | `list`   | 
| `TYPE_MAP`    | mapa         | `map`    |
| `TYPE_TUPLE`  | krotka       | `tuple`  |

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
| `AND`             | operator logiczny "i"   | `AND`    |
| `OR`              | operator logiczny "lub" | `OR`     |
| `NOT`             | operator logiczny "nie" | `NOT`    |
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

| Token       | Opis                              | Przykład  |
|-------------|-----------------------------------|-----------|
| `T_IF`      | instrukcja warunkowa if           | `IF`      |
| `T_ELIF`    | instrukcja elif                   | `ELIF`    |
| `T_ELSE`    | instrukcja else                   | `ELSE`    |
| `T_FI`      | instrukcja fi                     | `FI`      |
| `T_LOOP`    | instrukcja rozpoczęcia pętli      | `LOOP`    |
| `T_POOL`    | instrukcja zakończenia pętli      | `POOL`    |
| `T_FOR`     | pętla for                         | `FOR`     |
| `T_WHILE`   | pętla while                       | `WHILE`   |
| `T_DO`      | pętla do while                    | `DO`      |
| `T_FUNC`    | deklaracja funkcji                | `FUNC`    |
| `T_CNUF`    | zakończenie delaracji funkcji     | `CNUF`    |
| `T_TRY`     | blok potencjalnych błędów         | `TRY`     |
| `T_YRT`     | zakończenie obsługi błędów        | `YRT`     |
| `T_CATCH`   | obsługa wyjątków                  | `CATCH`   |
| `T_FINALLY` | blok wykonywany po obsłudze błędów | `FINALLY` |


### Inne tokeny

| Token        | Opis       | Przykład                 |
|--------------|------------|--------------------------|
| `IDENTIFIER` | identyfikator | `zmienna`, `mojaFunkcja` |
| `WHITE_SPACE`| biały znak | ` `, `\n`, `\t`           |

---

## Gramatyka
```antlr
grammar Iffi;

start_ : statement* EOF;

statement
    : declaration
    | assignment
    | if_statement
    | while_loop
    | do_while_loop
    ;

declaration
    : basic_data_type ID ('=' expr)? ';'
    ;

assignment : ID '=' expr ';' ;

if_statement
    : IF '(' expr ')' ':' block (ELIF '(' expr ')' ':' block)* (ELSE ':' block)? FI
    ;

while_loop
    : LOOP WHILE '(' expr ')' ':' block POOL
    ;

do_while_loop
    : LOOP DO ':' block WHILE '(' expr ')' POOL
    ;

block : statement+ ;

expr
    : atom
    | expr ('+' | '-') expr
    | expr '**' expr
    | expr ('*' | '/') expr
    | expr ('+' | '-') expr
    | expr '%' expr
    | expr '==' expr
    | expr '<' expr
    | expr '<=' expr
    | expr '>' expr
    | expr '>=' expr
    | '(' expr ')'
    ;

// Keywords

// Basic data types
basic_data_type
    : 'int'
    | 'float'
    | 'double'
    | 'bool'
    | 'char'
    | 'string'
    ;

// Advanced data types
advanced_data_types
    : 'array'
    | 'list'
    | 'map'
    | 'tuple'
    ;

// If statements
IF: 'if';
FI: 'fi';
ELIF: 'elif';
ELSE: 'else';

// Loops
LOOP: 'loop';
POOL: 'pool';
FOR: 'for';
WHILE: 'while';
DO: 'do';


atom
    : INT
    | FLOAT
    | ID
    | BOOL
    ;

INT   : [+-]?[0-9]+ ;
FLOAT : [+-]?([0-9]*[.])?[0-9]+ ;
ID    : [a-zA-Z_][a-zA-Z_0-9]* ;
BOOL  : 'true' | 'false' ;
WS    : [ \t\n\r]+ -> skip ;
```


---

## Narzędzia i biblioteki

| Narzędzie                | Zastosowanie                    |
|--------------------------|---------------------------------|
| `ANTLR 4`                | Generator parsera i leksera     |
| `Python 3.13+`           | Interpreter                     |
| `antlr4-python3-runtime` | Wykonanie parsera w Pythonie    |

---

## Przykładowy kod źródłowy w języku IFFI

```iffi
if (20 < 21):
    var = 2 ** 9;
    xd = 99 % 4;
elif (9 == 9):
    g = 2 + 3;
else:
    if (6 == 8):
        ee = 9.13;
        ee2 = 8;
    else:
        y = true;
    fi
fi

loop while (6 > 0):
    int v = 9;
    string j3 =7.2;
pool

loop do:
    char b = 7823;
    while (2 ** 7)
pool