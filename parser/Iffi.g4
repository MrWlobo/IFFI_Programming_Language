grammar Iffi;

start_ : statement* EOF;

statement
    : declaration
    | assignment
    | if_statement
    | loop
    | for_loop
    | while_loop
    | do_while_loop
    | function
    | function_call
    | increment_decrement
    | print_call
    | stop_statement
    | skip_statement
    | return_statement
    ;

declaration
    : basic_data_type ID (ASSIGN expr)? SEMICOLON
    | basic_data_type ID (ASSIGN logic_expr)? SEMICOLON
    | advanced_data_type LEFT_BRACKET basic_data_type RIGHT_BRACKET ID (ASSIGN data_structure)? SEMICOLON
    ;

assignment
    : ID (LEFT_BRACKET expr RIGHT_BRACKET)? ASSIGN expr SEMICOLON
    | ID ASSIGN_PLUS expr SEMICOLON
    | ID ASSIGN_MINUS expr SEMICOLON
    | ID ASSIGN_MULTIPLY expr SEMICOLON
    | ID ASSIGN_DIVIDE expr SEMICOLON
    ;

if_statement
    : T_IF LEFT_PAREN logic_expr RIGHT_PAREN COLON block (T_ELIF LEFT_PAREN logic_expr RIGHT_PAREN COLON block)* (T_ELSE COLON block)? T_FI
    ;

loop
    : T_LOOP COLON block T_POOL
    ;

for_loop
    : T_LOOP T_FOR LEFT_PAREN basic_data_type ID T_IN data_structure RIGHT_PAREN COLON block T_POOL
    | T_LOOP T_FOR LEFT_PAREN basic_data_type ID T_IN ID RIGHT_PAREN COLON block T_POOL
    ;

while_loop
    : T_LOOP T_WHILE LEFT_PAREN logic_expr RIGHT_PAREN COLON block T_POOL
    ;

do_while_loop
    : T_LOOP T_DO COLON block T_WHILE LEFT_PAREN logic_expr RIGHT_PAREN T_POOL
    ;

function
    : T_FUNC ID LEFT_PAREN (argument (COMMA argument)*)? RIGHT_PAREN ARROW (basic_data_type | advanced_data_type LEFT_BRACKET basic_data_type RIGHT_BRACKET| VOID) COLON block T_CNUF
    ;

argument
    : ID COLON (basic_data_type | advanced_data_type LEFT_BRACKET basic_data_type RIGHT_BRACKET)
    ;

function_call
    : function_call_expr SEMICOLON
    ;

increment_decrement
    : prefix_increment_decrement SEMICOLON
    | postfix_increment_decrement SEMICOLON
    ;

print_call
    : PRINT LEFT_PAREN expr RIGHT_PAREN SEMICOLON ;

stop_statement : T_STOP SEMICOLON ;

skip_statement : T_SKIP SEMICOLON ;

return_statement : T_RETURN (expr | logic_expr) SEMICOLON ;

block : ( statement )* ;

expr
    : ID LEFT_BRACKET expr RIGHT_BRACKET
    | function_call_expr
    | prefix_increment_decrement
    | postfix_increment_decrement
    | atom
    | LEFT_PAREN expr RIGHT_PAREN
    | expr POWER expr
    | expr (MULTIPLY | DIVIDE | FLOOR_DIVIDE | MODULO) expr
    | expr (PLUS | MINUS) expr
    | data_structure
    | ID LEFT_BRACKET expr RIGHT_BRACKET
    ;

logic_expr
    : LEFT_PAREN logic_expr RIGHT_PAREN
    | NOT logic_expr
    | expr ((EQUAL | NOT_EQUAL | LESS_THAN | GREATER_THAN | LESS_EQUAL | GREATER_EQUAL) expr)
    | logic_expr AND logic_expr
    | logic_expr OR logic_expr
    | expr
    ;

function_call_expr : ID LEFT_PAREN (expr (COMMA expr)*)? RIGHT_PAREN ;

prefix_increment_decrement
    : (INCREMENT | DECREMENT) ID
    ;

postfix_increment_decrement
    : ID (INCREMENT | DECREMENT)
    ;

data_structure
    : LEFT_BRACKET (expr (COMMA expr)*)? RIGHT_BRACKET
    | RANGE LEFT_PAREN expr COMMA expr RIGHT_PAREN
    ;

// Basic data types
basic_data_type
    : TYPE_INT
    | TYPE_FLOAT
    | TYPE_BOOL
    | TYPE_CHAR
    | TYPE_STRING
    ;

TYPE_INT: 'int' | 'INT';
TYPE_FLOAT: 'float' | 'FLOAT';
TYPE_BOOL: 'bool' | 'BOOL';
TYPE_CHAR: 'char' | 'CHAR';
TYPE_STRING: 'string' | 'STRING';

// Advanced data types
advanced_data_type
    : TYPE_LIST
    ;

TYPE_LIST: 'list' | 'LIST';
RANGE: 'range' | 'RANGE';

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

// Print call
PRINT: 'print';

atom
    : BOOL
    | ID
    | INT
    | FLOAT
    | CHAR
    | STRING
    ;

LEFT_PAREN: '(';
RIGHT_PAREN: ')';
LEFT_BRACKET: '[';
RIGHT_BRACKET: ']';
LEFT_BRACE: '{';
RIGHT_BRACE: '}';
SEMICOLON: ';';
COMMA: ',';
COLON: ':';
ARROW: '->';
HASHTAG: '#';
PLUS: '+';
MINUS: '-';
MULTIPLY: '*';
DIVIDE: '/';
FLOOR_DIVIDE: '//';
MODULO: '%';
POWER: '**';
INCREMENT: '++';
DECREMENT: '--';
EQUAL: '==';
NOT_EQUAL: '!=';
LESS_THAN: '<';
LESS_EQUAL: '<=';
GREATER_THAN: '>';
GREATER_EQUAL: '>=';
ASSIGN: '=';
ASSIGN_PLUS: '+=';
ASSIGN_MINUS: '-=';
ASSIGN_MULTIPLY: '*=';
ASSIGN_DIVIDE: '/=';

INT: [-]?[0-9]+ ;
FLOAT: [-]?([0-9]*[.])?[0-9]+ ;
BOOL: 'true' | 'false' ;
ID: [a-zA-Z_][a-zA-Z_0-9]* ;
CHAR: '\'' ( '\\' . | ~['\\\r\n] ) '\'' ;
STRING: '"' ( '\\' . | ~["\\\r\n] )* '"' ;
WS: [ \t\n\r]+ -> skip ;
LINE_COMMENT : '#' ~[\r\n]* ('\r'? '\n' | EOF) -> skip ;
