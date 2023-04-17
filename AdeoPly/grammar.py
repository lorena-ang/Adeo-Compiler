# -----------------------------------------------------------------------------
# grammar.py
#
# Adeo grammar file for use with PLY library
# -----------------------------------------------------------------------------

import sys

keywords = {
    'program' :'PROGRAM',
    'var' : 'VAR',
    'int' : 'INT',
    'float' : 'FLOAT',
    'string' : 'STRING',
    'bool' : 'BOOL',
    'void' : 'VOID',
    'if' : 'IF',
    'else' : 'ELSE',
    'elseif' : 'ELSEIF',
    'true' : 'BOOL_CONSTANT_TRUE',
    'false' : 'BOOL_CONSTANT_FALSE',
    'Class' : 'CLASS',
    'while' : 'WHILE',
    'for' : 'FOR',
    'to' : 'TO',
    'do' : 'DO',
    'function' : 'FUNCTION',
    'return': 'RETURN',
    'read' : 'READ',
    'print' : 'PRINT',
    'main' : 'MAIN'
}

tokens = list(keywords.values()) + [ 
    'ID',
    'RELOP',
    'AND',
    'OR',
    'SEMICOLON',
    'COLON',
    'COMMA',
    'DOT',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'LBRACK',
    'RBRACK',
    'INT_CONST',
    'FLOAT_CONST',
    'STRING_CONST',
    'ASSIGNOP',
]

# Tokens
t_RELOP = r'([<>]=?|[!=]=)'
t_AND = r'&&'
t_OR = r'\|\|'
t_SEMICOLON = r'\;'
t_COLON = r'\:'
t_COMMA = r'\,'
t_DOT = r'.'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LBRACK = r'\['
t_RBRACK = r'\]'
t_ASSIGNOP = r'='
t_INT_CONST = r'[+-]?[0-9]+'
t_FLOAT_CONST = r'[+-]?[0-9]+\.[0-9]+'
t_STRING_CONST = r'\"([^\\\n]|(\\.))*?\"'

# Functions

# ID
def t_ID(t):
    r'[a-zA-Z]+[a-zA-Z0-9_]*'
    t.type = keywords.get(t.value, 'ID')
    return t

# Ignore characters
t_ignore = " \t"
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Illegal character error
def t_error(t):
    print(f"Illegal character '{t.value[0]!r}' in line {t.lineno}")
    t.lexer.skip(1)

# Build the lexer
import ply.lex as lex
lexer = lex.lex()

# Parsing rules

def p_program(t):
    '''
    program : PROGRAM ID SEMICOLON p_1 p_2 p_3 MAIN LPAREN RPAREN block
    '''
    t[0] = "END"

def p_p_1(t):
    '''
    p_1 : class p_1
        |
    '''

def p_p_2(t):
    '''
    p_2 : variables
        |
    '''

def p_p_3(t):
    '''
    p_3 : function p_3
        |
    '''

def p_block(t):
    '''
    block : LBRACE block_v block_1 RBRACE
    '''

def p_block_v(t):
    '''
    block_v : variables
            |
    '''

def p_block_1(t):
    '''
    block_1 : statement block_1
            |
    '''

def p_statement(t):
    '''
    statement : assignment
              | conditional
              | write
              | read
              | l_while
              | l_for
              | f_call
    '''

def p_assignment(t):
    '''
    assignment : var ASSIGNOP expression SEMICOLON
    '''

def p_conditional(t):
    '''
    conditional : IF LPAREN expression RPAREN block conditional_1
    '''

def p_conditional_1(t):
    '''
    conditional_1 : ELSEIF LPAREN expression RPAREN block conditional_1
                  | ELSE block
                  |
    '''

def p_write(t):
    '''
    write : PRINT LPAREN write_1 RPAREN SEMICOLON
    '''

def p_write_1(t):
    '''
    write_1 : expression w_1
            | STRING_CONST w_1
    '''

def p_w_1(t):
    '''
    w_1 : COMMA write_1
        |
    '''

def p_read(t):
    '''
    read : READ LPAREN ID RPAREN SEMICOLON
    '''

def p_l_while(t):
    '''
    l_while : WHILE LPAREN expression RPAREN block
    '''

def p_l_for(t):
    '''
    l_for : FOR ID ASSIGNOP expression TO expr DO block
    '''

def p_f_call(t):
    '''
    f_call : ID LPAREN f_call_1 RPAREN SEMICOLON
    '''

def p_f_call_1(t):
    '''
    f_call_1 : expression f_call_2
             |
    '''

def p_f_call_2(t):
    '''
    f_call_2 : COMMA expression f_call_1
             |
    '''

def p_type(t):
    '''
    type : INT
         | FLOAT
         | STRING
         | BOOL
    '''

def p_function(t):
    '''
    function : function_t FUNCTION ID function_p block
    '''

def p_function_t(t):
    '''
    function_t : type
               | VOID
    '''

def p_function_p(t):
    '''
    function_p : LPAREN RPAREN
               | LPAREN params RPAREN
    '''

def p_params(t):
    '''
    params : type ID params_1
    '''

def p_params_1(t):
    '''
    params_1 : COMMA type ID params_1
             |
    '''

def p_variables(t):
    '''
    variables : variables_1
    '''

def p_variables_1(t):
    '''
    variables_1 : VAR type COLON ID array variables_2 SEMICOLON variables_1
                |
    '''

def p_variables_2(t):
    '''
    variables_2 : COMMA ID array variables_2
                |
    '''

def p_array(t):
    '''
    array : LBRACK INT_CONST RBRACK
          | LBRACK INT_CONST RBRACK LBRACK INT_CONST RBRACK
          |
    '''

def p_var(t):
    '''
    var : ID array
        | ID DOT ID
    '''

def p_class(t):
    '''
    class : CLASS ID LBRACE type COLON ID class_1 RBRACE SEMICOLON
    '''

def p_class_1(t):
    '''
    class_1 : COMMA type COLON ID class_1
            |
    '''

def p_expression(t):
    '''
    expression : sub_expr e_1
    '''

def p_e_1(t):
    '''
    e_1 : AND sub_expr e_1
        | OR sub_expr e_1
        |
    '''

def p_sub_expr(t):
    '''
    sub_expr : expr sub_expr_1
    '''

def p_sub_expr_1(t):
    '''
    sub_expr_1 : RELOP expr
               |
    '''

def p_expr(t):
    '''
    expr : term expr_1
    '''

def p_expr_1(t):
    '''
    expr_1 : PLUS term expr_1
           | MINUS term expr_1
           |
    '''

def p_term(t):
    '''
    term : factor term_1
    '''

def p_term_1(t):
    '''
    term_1 : TIMES factor term_1
           | DIVIDE factor term_1
           |
    '''

def p_factor(t):
    '''
    factor : LPAREN expr RPAREN
           | var
           | INT_CONST
           | FLOAT_CONST
    '''

# Syntax error
def p_error(t):
    print(f'Syntax error at {t} for {t.value!r} in line {t.lineno}')

# Build the parser
import ply.yacc as yacc
parser = yacc.yacc()

# To test: python3 grammar.py test.txt
if __name__ == '__main__':
    if len(sys.argv) == 2:
        name = sys.argv[1]
        # Read and run text file
        try:
            with open(name, 'r') as file:
                file_content = file.read()
                if parser.parse(file_content) == "END":
                    print("The data from the .txt file is valid for Adeo language.")
                else:
                    print("The data from the .txt file is invalid for Adeo language.")
        except (EOFError, FileNotFoundError) as e:
            print(e)
    else:
        print("ERROR: Filename not added correctly.")