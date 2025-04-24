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

block : ( statement | T_STOP ';' | T_SKIP ';' )+ ;

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
    : expr (('==' | '!=' | '<' | '>' | '<=' | '>=') expr)?
    | '(' logic_expr ')'
    | NOT logic_expr
    | logic_expr AND logic_expr
    | logic_expr OR logic_expr
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

TYPE_INT: 'int';
TYPE_FLOAT: 'float';
//TYPE_DOUBLE: 'double';
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
T_IF: 'if';
T_FI: 'fi';
T_ELIF: 'elif';
T_ELSE: 'else';

// Loops
T_LOOP: 'loop';
T_POOL: 'pool';
T_FOR: 'for';
T_IN: 'in';
T_WHILE: 'while';
T_DO: 'do';
T_STOP: 'stop';
T_SKIP: 'skip';

// Functions
T_FUNC: 'func';
T_CNUF: 'cnuf';

// Boolean operators
NOT: 'not';
AND: 'and';
OR: 'or';


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
