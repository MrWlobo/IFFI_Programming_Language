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
    | increment_decrement
    ;

declaration
    : basic_data_type ID ('=' expr)? ';'
    | advanced_data_type ID ('=' data_structure)? ';'
    ;

assignment
    : ID '=' expr ';'
    | ID '+=' expr ';'
    | ID '-=' expr ';'
    | ID '*=' expr ';'
    | ID '/=' expr ';'
    | ID '=' data_structure ';'
    ;

if_statement
    : T_IF '(' logic_expr ')' ':' block (T_ELIF '(' logic_expr ')' ':' block)* (T_ELSE ':' block)? T_FI
    ;

for_loop
    : T_LOOP T_FOR '(' basic_data_type ID T_IN data_structure ')' ':' block T_POOL
    | T_LOOP T_FOR '(' basic_data_type ID T_IN ID ')' ':' block T_POOL
    ;

while_loop
    : T_LOOP T_WHILE '(' logic_expr ')' ':' block T_POOL
    ;

do_while_loop
    : T_LOOP T_DO ':' block T_WHILE '(' logic_expr ')' T_POOL
    ;

function
    : T_FUNC ID '(' (argument (',' argument)*)? ')' '->' (basic_data_type | advanced_data_type| VOID) block T_CNUF
    ;

argument
    : ID ':' (basic_data_type | advanced_data_type)
    ;

function_call
    : ID '(' ((ID | atom | data_structure) (',' (ID | atom | data_structure))*)? ')' ';'
    ;

increment_decrement
    : ID ('++' | '--') ';'
    | ('++' | '--') ID ';'
    ;

stop_statement : T_STOP ';' ;

skip_statement : T_SKIP ';' ;

return_statement : T_RETURN logic_expr ';' ;

block : ( statement | stop_statement | skip_statement | return_statement )+ ;

expr
    : atom
    | function_call
    | expr ('++' | '--')
    | expr '**' expr
    | expr ('*' | '/' | '//' | '%') expr
    | expr ('+' | '-') expr
    | '(' expr ')'
    | prefix_increment_decrement
    | postfix_increment_decrement
    | atom T_IN data_structure
    | atom T_IN ID
    | data_structure
    ;

logic_expr
    : '(' logic_expr ')'
    | NOT logic_expr
    | logic_expr AND logic_expr
    | logic_expr OR logic_expr
    | expr (('==' | '!=' | '<' | '>' | '<=' | '>=') expr)?
    ;

prefix_increment_decrement
    : ('++' | '--') ID
    ;

postfix_increment_decrement
    : ID ('++' | '--')
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
//    | TYPE_DOUBLE
    | TYPE_BOOL
    | TYPE_CHAR
    | TYPE_STRING
    ;

TYPE_INT: 'int' | 'INT';
TYPE_FLOAT: 'float' | 'FLOAT';
//TYPE_DOUBLE: 'double';
TYPE_BOOL: 'bool' | 'BOOL';
TYPE_CHAR: 'char' | 'CHAR';
TYPE_STRING: 'string' | 'STRING';

// Advanced data types
advanced_data_type
    : TYPE_ARRAY
    | TYPE_LIST
    | TYPE_MAP
    | TYPE_TUPLE
    ;

TYPE_ARRAY: 'array' | 'ARRAY';
TYPE_LIST: 'list' | 'LIST';
TYPE_MAP: 'map' | 'MAP';
TYPE_TUPLE: 'tuple' | 'TUPLE';

// Void
VOID: 'void' | 'VOID';

// If statements
T_IF: 'if' | 'IF';
T_FI: 'fi' | 'FI';
T_ELIF: 'elif' | 'ELIF';
T_ELSE: 'else' | 'ELSE';

// Loops
T_LOOP: 'loop' | 'LOOP';
T_POOL: 'pool' | 'POOL';
T_FOR: 'for' | 'FOR';
T_IN: 'in' | 'IN';
T_WHILE: 'while' | 'WHILE';
T_DO: 'do' | 'DO';
T_STOP: 'stop' | 'STOP';
T_SKIP: 'skip' | 'SKIP';

// Functions
T_FUNC: 'func' | 'FUNC';
T_CNUF: 'cnuf' | 'CNUF';
T_RETURN: 'return' | 'RETURN';

// Boolean operators
NOT: 'not' | 'NOT';
AND: 'and' | 'AND';
OR: 'or' | 'OR';


atom
    : INT
    | FLOAT
    | ID
    | BOOL
    ;

INT: [-]?[0-9]+ ;
FLOAT: [-]?([0-9]*[.])?[0-9]+ ;
//DOUBLE: [-]?([0-9]*[.])?[0-9]+ ;
ID: [a-zA-Z_][a-zA-Z_0-9]* ;
BOOL: 'true' | 'false' ;
WS: [ \t\n\r]+ -> skip ;
LINE_COMMENT : '#' .*? '\r'? '\n' -> skip ;
