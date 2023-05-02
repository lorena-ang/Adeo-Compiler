# -----------------------------------------------------------------------------
# grammar.py
#
# Adeo grammar file for use with PLY library
# -----------------------------------------------------------------------------

import sys
from variable_table import VariableTable
from quadruples import Quadruples
from semantic_cube import SemanticCube

#
# LEXER
#

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
    'EQOP',
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
t_RELOP = r'([<>]=?)'
t_EQOP = r'([!=]=)'
t_AND = r'\&\&'
t_OR = r'\|\|'
t_SEMICOLON = r'\;'
t_COLON = r'\:'
t_COMMA = r'\,'
t_DOT = r'.'
t_PLUS = r'\+'
t_MINUS = r'\-'
t_TIMES = r'\*'
t_DIVIDE = r'\/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LBRACK = r'\['
t_RBRACK = r'\]'
t_ASSIGNOP = r'\='
t_INT_CONST = r'[+-]?[0-9]+'
t_FLOAT_CONST = r'[+-]?[0-9]+\.[0-9]+'
t_STRING_CONST = r'\"[^\"]*\"'

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

#
# PARSER
#

scope = "global"
semantic_cube = SemanticCube()
variable_table = VariableTable()
quadruples = Quadruples()

# Parsing rules

def p_program(t):
    '''
    program : PROGRAM ID SEMICOLON p_1 p_2 p_3 MAIN LPAREN RPAREN block
    '''
    variable_table.print()
    quadruples.print()
    t[0] = "END"

def p_p_1(t):
    '''
    p_1 : class p_1
        |
    '''

def p_p_2(t):
    '''
    p_2 : variables p_2
        |
    '''

def p_p_3(t):
    '''
    p_3 : function p_3
        |
    '''

def p_block(t):
    '''
    block : LBRACE p_2 block_1 RBRACE
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
              | f_call SEMICOLON
              | return
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
    elements = t[3]
    for elem in elements:
        quadruples.add(("PRINT", elem, None, None))

def p_write_1(t):
    '''
    write_1 : expression COMMA write_1
            | STRING_CONST COMMA write_1
            | expression
            | STRING_CONST
    '''
    if len(t) == 4:
        t[0] = [t[1], *t[3]]
    else:
        t[0] = [t[1]]

def p_read(t):
    '''
    read : READ LPAREN var RPAREN SEMICOLON
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
    f_call : ID LPAREN f_call_1 RPAREN
    '''

def p_f_call_1(t):
    '''
    f_call_1 : expression f_call_2
             |
    '''

def p_f_call_2(t):
    '''
    f_call_2 : COMMA expression f_call_2
             |
    '''

def p_return(t):
    '''
    return : RETURN expression SEMICOLON
    '''

def p_type(t):
    '''
    type : INT
         | FLOAT
         | STRING
         | BOOL
    '''
    t[0] = t[1]

def p_function(t):
    '''
    function : function_t FUNCTION ID function_p block
    '''

def p_function_t(t):
    '''
    function_t : type
               | VOID
    '''
    t[0] = t[1]

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
    variables : VAR type COLON ID array variables_1 SEMICOLON
              | VAR ID COLON ID array variables_1 SEMICOLON
    '''
    type = t[2]
    names = [t[4], *t[6]]
    for name in names:
        variable_table.add(name, type, scope, 0)
            
def p_variables_1(t):
    '''
    variables_1 : COMMA ID array variables_1
                |
    '''
    if len(t) == 5:
        t[0] = [t[2], *t[4]]
    else:
        t[0] = []

def p_array(t):
    '''
    array : LBRACK INT_CONST RBRACK
          | LBRACK INT_CONST RBRACK LBRACK INT_CONST RBRACK
          |
    '''
    t[0] = []

def p_var(t):
    '''
    var : ID array
        | ID DOT ID
    '''
    if len(t) == 3:
        t[0] = t[1]

def p_class(t):
    '''
    class : CLASS ID LBRACE type COLON ID class_1 RBRACE SEMICOLON
    '''

def p_class_1(t):
    '''
    class_1 : COMMA type COLON ID class_1
            |
    '''

def p_const(t):
    '''
    const : int_const
          | float_const
          | string_const
          | bool_const
    '''
    t[0] = t[1]

def p_int_const(t):
    '''
    int_const : INT_CONST
    '''
    t[0] = ("int", t[1])

def p_float_const(t):
    '''
    float_const : FLOAT_CONST
    '''
    t[0] = ("float", t[1])

def p_string_const(t):
    '''
    string_const : STRING_CONST
    '''
    t[0] = ("string", t[1])

def p_bool_const(t):
    '''
    bool_const : BOOL_CONSTANT_TRUE
               | BOOL_CONSTANT_FALSE
    '''
    t[0] = ("bool", t[1])

def p_expression(t):
    '''
    expression : sub_expr_e e_1
    '''

def p_e_1(t):
    '''
    e_1 : AND sub_expr_e e_1
        | OR sub_expr_e e_1
        |
    '''

def p_sub_expr_e(t):
    '''
    sub_expr_e : sub_expr_r e_2
    '''

def p_e_2(t):
    '''
    e_2 : EQOP sub_expr_r e_2
        |
    '''

def p_sub_expr_r(t):
    '''
    sub_expr_r : expr
               | expr RELOP expr
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
           | const
           | f_call
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

# memoria
# que nombre del scope esté en la tabla de variables (diccionario con llave de scope y contenido sea tabla de variables) (que el scope no esté en la variable)
