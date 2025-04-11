grammar Iffi;

start_ : statement* EOF;

statement
    : declaration
    | assignment
    | if_statement
    | for_loop
    | while_loop
    | do_while_loop
    | function
    | function_call
    ;

declaration
    : basic_data_type ID ('=' expr)? ';'
    | advanced_data_type ID ('=' data_structure)? ';'
    ;

assignment
    : ID '=' expr ';'
    | ID '=' data_structure ';'
    ;

if_statement
    : IF '(' expr ')' ':' block (ELIF '(' expr ')' ':' block)* (ELSE ':' block)? FI
    ;

for_loop
    : LOOP FOR '(' basic_data_type ID IN data_structure ')' ':' block POOL
    | LOOP FOR '(' basic_data_type ID IN ID ')' ':' block POOL
    ;

while_loop
    : LOOP WHILE '(' expr ')' ':' block POOL
    ;

do_while_loop
    : LOOP DO ':' block WHILE '(' expr ')' POOL
    ;

function
    : FUNC ID '(' (argument (',' argument)*)? ')' '->' (basic_data_type | advanced_data_type| VOID) block CNUF
    ;

argument
    : ID ':' (basic_data_type | advanced_data_type)
    ;

function_call
    : ID '(' ((ID | atom | data_structure) (',' (ID | atom | data_structure))*)? ')' ';'
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
    | atom IN data_structure
    | atom IN ID
    ;

data_structure
    : '[' (atom (',' atom)*)? ']'
    | '{' (atom ':' atom (',' atom ':' atom)*)? '}'
    | '(' (atom (',' atom)*)? ')'
    ;

// Keywords

// Basic data types
basic_data_type
    : TYPE_INT
    | TYPE_FLOAT
    | TYPE_DOUBLE
    | TYPE_BOOL
    | TYPE_CHAR
    | TYPE_STRING
    ;

TYPE_INT: 'int';
TYPE_FLOAT: 'float';
TYPE_DOUBLE: 'double';
TYPE_BOOL: 'bool';
TYPE_CHAR: 'char';
TYPE_STRING: 'string';

// Advanced data types
advanced_data_type
    : TYPE_ARRAY
    | TYPE_LIST
    | TYPE_MAP
    | TYPE_TUPLE
    ;

TYPE_ARRAY: 'array';
TYPE_LIST: 'list';
TYPE_MAP: 'map';
TYPE_TUPLE: 'tuple';

// Void
VOID: 'void';

// If statements
IF: 'if';
FI: 'fi';
ELIF: 'elif';
ELSE: 'else';

// Loops
LOOP: 'loop';
POOL: 'pool';
FOR: 'for';
IN: 'in';
WHILE: 'while';
DO: 'do';

// Functions
FUNC: 'func';
CNUF: 'cnuf';

atom
    : INT
    | FLOAT
    | ID
    | BOOL
    ;

INT: [+-]?[0-9]+ ;
FLOAT: [+-]?([0-9]*[.])?[0-9]+ ;
DOUBLE: [+-]?([0-9]*[.])?[0-9]+ ;
ID: [a-zA-Z_][a-zA-Z_0-9]* ;
BOOL: 'true' | 'false' ;
WS: [ \t\n\r]+ -> skip ;
