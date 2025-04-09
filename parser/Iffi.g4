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
