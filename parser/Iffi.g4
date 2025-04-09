grammar Iffi;

start_ : statement* EOF;

statement
    : assignment
    | if_statement
    ;

assignment : ID '=' expr ';' ;

if_statement
    : IF '(' expr ')' ':' block (ELIF '(' expr ')' ':' block)* (ELSE ':' block)? FI
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

//Keywords
IF: 'if';
FI: 'fi';
ELIF: 'elif';
ELSE: 'else';


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
