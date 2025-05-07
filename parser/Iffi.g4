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
    ;

declaration
    : basic_data_type ID (ASSIGN expr)? SEMICOLON
    | advanced_data_type ID (ASSIGN data_structure)? SEMICOLON
    ;

assignment
    : ID ASSIGN expr SEMICOLON
    | ID ASSIGN_PLUS expr SEMICOLON
    | ID ASSIGN_MINUS expr SEMICOLON
    | ID ASSIGN_MULTIPLY expr SEMICOLON
    | ID ASSIGN_DIVIDE expr SEMICOLON
    | ID ASSIGN data_structure SEMICOLON
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
    : T_FUNC ID LEFT_PAREN (argument (COMMA argument)*)? RIGHT_PAREN ARROW (basic_data_type | advanced_data_type| VOID) COLON block T_CNUF
    ;

argument
    : ID COLON (basic_data_type | advanced_data_type)
    ;

function_call
    : ID LEFT_PAREN ((ID | atom | data_structure) (COMMA (ID | atom | data_structure))*)? RIGHT_PAREN SEMICOLON
    ;

increment_decrement
    : ID (INCREMENT | DECREMENT) SEMICOLON
    | (INCREMENT | DECREMENT) ID SEMICOLON
    ;
    
try_catch_statement
    : T_TRY COLON T_CATCH LEFT_PAREN exception_type ID RIGHT_PAREN COLON block (T_CATCH LEFT_PAREN exception_type ID RIGHT_PAREN COLON block)* T_FINALLY COLON block T_YRT
    ;

stop_statement : T_STOP SEMICOLON ;

skip_statement : T_SKIP SEMICOLON ;

return_statement : T_RETURN logic_expr SEMICOLON ;

block : ( statement | stop_statement | skip_statement | return_statement )+ ;

expr
    : atom
    | function_call
    | expr (INCREMENT | DECREMENT)
    | expr POWER expr
    | expr (MULTIPLY | DIVIDE | FLOOR_DIVIDE | MODULO) expr
    | expr (PLUS | MINUS) expr
    | LEFT_PAREN expr RIGHT_PAREN
    | prefix_increment_decrement
    | postfix_increment_decrement
    | atom T_IN data_structure
    | atom T_IN ID
    | data_structure
    ;

logic_expr
    : LEFT_PAREN logic_expr RIGHT_PAREN
    | NOT logic_expr
    | logic_expr AND logic_expr
    | logic_expr OR logic_expr
    | expr ((EQUAL | NOT_EQUAL | LESS_THAN | GREATER_THAN | LESS_EQUAL | GREATER_EQUAL) expr)?
    ;

prefix_increment_decrement
    : (INCREMENT | DECREMENT) ID
    ;

postfix_increment_decrement
    : ID (INCREMENT | DECREMENT)
    ;

data_structure
    : LEFT_BRACKET (atom (COMMA atom)*)? RIGHT_BRACKET
    | LEFT_BRACE (atom COLON atom (COMMA atom COLON atom)*)? RIGHT_BRACE
    | LEFT_PAREN (atom (COMMA atom)*)? RIGHT_PAREN
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

// Try-catch
T_TRY: 'try' | 'TRY';
T_YRT: 'yrt' | 'YRT';
T_CATCH: 'catch' | 'CATCH';
T_FINALLY: 'finally' | 'FINALLY';

// Functions
T_FUNC: 'func' | 'FUNC';
T_CNUF: 'cnuf' | 'CNUF';
T_RETURN: 'return' | 'RETURN';

// Boolean operators
NOT: 'not' | 'NOT';
AND: 'and' | 'AND';
OR: 'or' | 'OR';

// Exception
exception_type
    : ID
    ;


atom
    : INT
    | FLOAT
    | ID
    | BOOL
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
//DOUBLE: [-]?([0-9]*[.])?[0-9]+ ;
ID: [a-zA-Z_][a-zA-Z_0-9]* ;
BOOL: 'true' | 'false' ;
WS: [ \t\n\r]+ -> skip ;
LINE_COMMENT : '#' .*? '\r'? '\n' -> skip ;
