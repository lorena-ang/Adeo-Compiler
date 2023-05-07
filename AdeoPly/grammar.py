# -----------------------------------------------------------------------------
# grammar.py
#
# Adeo grammar file for use with PLY library
# -----------------------------------------------------------------------------

import sys
from variable_table import Variable
from memory_manager import MemoryManager
from function_directory import FunctionDirectory
from stack import Context, Stack
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
    'true' : 'TRUE',
    'false' : 'FALSE',
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

data_memory_manager = MemoryManager(0)
constant_memory_manager = MemoryManager(4000)
temporal_memory_manager = MemoryManager(8000)
function_directory = FunctionDirectory()
quadruples = Quadruples()

context_stack = Stack()
context_stack.push(Context("global", data_memory_manager))

jump_stack: list[int] = []

# Parsing rules

def p_program(t):
    '''
    program : PROGRAM ID SEMICOLON p_1 p_2 p_3 MAIN LPAREN RPAREN block
    '''
    data_memory_manager.print("Global")
    constant_memory_manager.print("Constant")
    temporal_memory_manager.print("Temporal")
    quadruples.print()
    # context_stack.print()
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
    statement : assignment SEMICOLON
              | conditional
              | write
              | read
              | l_while
              | l_for
              | f_call SEMICOLON
              | return
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
        if elements is not None:
            if type(elem) == tuple:
                quadruples.add_quad(("PRINT", elem[1], None, None))
            elif type(elem) == Variable:
                address = elem.address
                quadruples.add_quad(("PRINT", address, None, None))
        else:
            raise Exception("The data to be printed is invalid")

def p_write_1(t):
    '''
    write_1 : expression COMMA write_1
            | expression
    '''
    if len(t) == 4:
        t[0] = [t[1], *t[3]]
    else:
        t[0] = [t[1]]

def p_read(t):
    '''
    read : READ LPAREN var RPAREN SEMICOLON
    '''
    if t[3] is not None:
            variable = t[3]
            address = variable.address
            quadruples.add_quad(("READ", address, None, None))
    else:
        raise Exception(f"There is no variable named '{t[3]}'.")

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
    
def p_type(t):
    '''
    type : INT
         | FLOAT
         | STRING
         | BOOL
    '''
    t[0] = t[1]

def p_variables(t):
    '''
    variables : VAR type COLON ID array variables_1 SEMICOLON
              | VAR ID COLON ID array variables_1 SEMICOLON
    '''
    type = t[2]
    variables = [t[4], *t[6]]
    for var in variables:
        context_stack.add_variable_to_stack(var, type)

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

def p_var(t):
    '''
    var : ID
        | ID DOT ID
        | ID array
    '''
    if len(t) == 3 and t[2] is None:
        variable = context_stack.get_variable_from_context(t[1])
        if variable is not None:
            t[0] = variable
    else:
        pass

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
    value = int(t[1])
    address = constant_memory_manager.find_address(value)
    if address is None:
        address = constant_memory_manager.add_value_to_memory(value)
    t[0] = ("int", address)

def p_float_const(t):
    '''
    float_const : FLOAT_CONST
    '''
    value = float(t[1])
    address = constant_memory_manager.find_address(value)
    if address is None:
        address = constant_memory_manager.add_value_to_memory(value)
    t[0] = ("float", address)

def p_string_const(t):
    '''
    string_const : STRING_CONST
    '''
    value = str(t[1])
    address = constant_memory_manager.find_address(value)
    if address is None:
        address = constant_memory_manager.add_value_to_memory(value)
    t[0] = ("string", address)

def p_bool_const(t):
    '''
    bool_const : TRUE
               | FALSE
    '''
    value = str(t[1])
    address = constant_memory_manager.find_address(value)
    if address is None:
        address = constant_memory_manager.add_value_to_memory(value)
    t[0] = ("bool", address)
    
def p_assignment(t):
    '''
    assignment : var ASSIGNOP assignment
               | var ASSIGNOP expression
    '''
    left_type, left_address = t[1].process_variable()
    left_name = t[1].name
    if type(t[3]) is tuple:
        right_type, right_address = t[3]
    else:
        right_type, right_address = t[3].process_variable()
    operation_type = SemanticCube().get_result_type(left_type, t[2], right_type)
    if left_name is not None and context_stack.check_variable_exists(left_name):
            quadruples.add_quad(("=", right_address, None, left_address))
            t[0] = (operation_type, left_address)
    else:
        raise Exception(f"Only variables may be assigned to.")

def p_expr_unique(t):
    '''
    expression : sub_expr_e
    sub_expr_e : sub_expr_r
    sub_expr_r : expr
    expr : term
    term : factor
    factor : var
           | const
           | f_call
           | LPAREN expr RPAREN
    '''
    if len(t) == 2:
        t[0] = t[1]
    else:
        t[0] = t[2]

def p_expr_operations(t):
    '''
    expression : expression AND sub_expr_e
               | expression OR sub_expr_e
    sub_expr_e : sub_expr_e EQOP sub_expr_r
    sub_expr_r : sub_expr_r RELOP expr
    expr : expr PLUS term
         | expr MINUS term
    term : term TIMES factor
         | term DIVIDE factor
    '''
    if type(t[1]) is tuple:
        left_type, left_address = t[1]
    else:
        left_type, left_address = t[1].process_variable()
    if type(t[3]) is tuple:
        right_type, right_address = t[3]
    else:
        right_type, right_address = t[3].process_variable()
    operation_type = SemanticCube().get_result_type(left_type, t[2], right_type)
    address = temporal_memory_manager.reserve_space(operation_type)
    quadruples.add_quad((t[2], left_address, right_address, address))
    t[0] = (operation_type, address)

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
                    print("\nThe data from the .txt file is valid for Adeo language.")
                else:
                    print("\nThe data from the .txt file is invalid for Adeo language.")
        except (EOFError, FileNotFoundError) as e:
            print(e)
    else:
        print("ERROR: Filename not added correctly.")