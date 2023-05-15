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
from quadruples import Quad, Quadruples
from semantic_cube import SemanticCube

#
# LEXER
#

keywords = {
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

jumps: list[int] = []
end_count: list[int] = []
end_jumps: list[int] = []

function_stack: list[str] = []

# Parsing rules

def p_program(t):
    '''
    program : class_decl variables_decl function_decl MAIN LPAREN RPAREN block
    '''
    data_memory_manager.print("Global")
    constant_memory_manager.print("Constant")
    # temporal_memory_manager.print("Temporal")
    quadruples.print()
    # context_stack.print()
    t[0] = "END"

def p_program_decl(t):
    '''
    class_decl : class class_decl
               |
    variables_decl : variables variables_decl
                   |
    function_decl : function function_decl
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

def p_block(t):
    '''
    block : LBRACE b_push_context variables_decl block_1 RBRACE b_pop_context
    l_block : LBRACE l_push_context block_1 RBRACE l_pop_context
    c_block : LBRACE block_1 RBRACE
    '''

def p_block_1(t):
    '''
    block_1 : statement block_1
            |
    '''
    
def p_b_push_context(t):
    '''
    b_push_context :
    '''
    context_stack.push(Context("local", temporal_memory_manager))
    
def p_b_pop_context(t):
    '''
    b_pop_context : 
    '''
    context_stack.pop()
    
def p_l_push_context(t):
    '''
    l_push_context :
    '''
    context_stack.push(Context("loop", temporal_memory_manager))
    end_count.append(0)

def p_l_pop_context(t):
    '''
    l_pop_context :
    '''
    context_stack.pop()
    for _ in range(end_count.pop()):
        quadruples[end_jumps.pop()] = Quad("GOTO", None, None, quadruples.instr_ptr)

def p_conditional(t):
    '''
    conditional : IF LPAREN expression conditional_np1 RPAREN l_push_context c_block conditional_1 l_pop_context
    '''
    last_jump = jumps.pop()
    quad = quadruples[last_jump]
    quadruples[last_jump] = Quad(quad.operator, quad.left_address, None, quadruples.instr_ptr)
    
def p_conditional_1(t):
    '''
    conditional_1 : ELSEIF LPAREN conditional_np2 expression conditional_np1 RPAREN c_block conditional_1
                  | ELSE conditional_np3 c_block
                  |
    '''
    
def p_conditional_np1(t):
    '''
    conditional_np1 :
    '''
    if isinstance(t[-1], tuple):
        type, address = t[-1]
    else:
        type, address = t[-1].process_variable()
    if type == "bool":
        jumps.append(quadruples.instr_ptr)
        quadruples.add_quad(Quad("GOTOF", address, None, None))
    else:
        raise TypeError("Type mismatch error: Expression should be a boolean.")
    
def p_conditional_np2(t):
    '''
    conditional_np2 :
    '''
    end_jumps.append(quadruples.instr_ptr)
    end_count[-1] += 1
    quadruples.add_quad(Quad("GOTO", None, None, None))
    last_jump = jumps.pop()
    quad = quadruples[last_jump]
    quadruples[last_jump] = Quad(quad.operator, quad.left_address, None, quadruples.instr_ptr)

def p_conditional_np3(t):
    '''
    conditional_np3 :
    '''
    quadruples.add_quad(Quad("GOTO", None, None, None))
    last_jump = jumps.pop()
    jumps.append(quadruples.instr_ptr - 1)
    quad = quadruples[last_jump]
    quadruples[last_jump] = Quad(quad.operator, quad.left_address, None, quadruples.instr_ptr)

def p_write(t):
    '''
    write : PRINT LPAREN write_1 RPAREN SEMICOLON
    '''
    elements = t[3]
    for elem in elements:
        if elements is not None:
            if type(elem) == tuple:
                quadruples.add_quad(Quad("PRINT", elem[1], None, None))
            elif type(elem) == Variable:
                address = elem.address
                quadruples.add_quad(Quad("PRINT", address, None, None))
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
        quadruples.add_quad(Quad("READ", address, None, None))
    else:
        raise Exception(f"There is no variable named '{t[3]}'.")

def p_l_while(t):
    '''
    l_while : WHILE LPAREN l_while_np1 expression conditional_np1 RPAREN l_block
    '''
    last_jump = jumps.pop()
    second_last_jump = jumps.pop()
    quadruples.add_quad(Quad("GOTO", None, None, second_last_jump))
    quad = quadruples[last_jump]
    quadruples[last_jump] = Quad(quad.operator, quad.left_address, None, quadruples.instr_ptr)
    
def p_l_while_np1(t):
    '''
    l_while_np1 :
    '''
    jumps.append(quadruples.instr_ptr)

def p_l_for(t):
    '''
    l_for : FOR l_for_np1 ASSIGNOP expr l_for_np2 TO expr l_for_np3 DO l_block
    '''
    # Jumps
    last_jump = jumps.pop()
    first_jump = jumps.pop()
    # Look for 1 const or save it
    value = 1
    one_address = constant_memory_manager.find_address(value)
    if one_address is None:
        one_address = constant_memory_manager.add_value_to_memory(value)
    # Add one
    left_type, left_address = t[2].process_variable()
    operation_type = SemanticCube().get_result_type(left_type, "+", "int")
    address = data_memory_manager.reserve_space(operation_type)
    quadruples.add_quad(Quad("+", left_address, one_address, address))
    quadruples.add_quad(Quad("=", address, one_address, left_address))
    # Update quadruples
    quadruples.add_quad(Quad("GOTO", None, None, first_jump))
    quad = quadruples[last_jump]
    quadruples[last_jump] = Quad(quad.operator, quad.left_address, None, quadruples.instr_ptr)

def p_l_for_np1(t):
    '''
    l_for_np1 : ID
    '''
    variable = context_stack.get_variable_from_context(t[1])
    if variable is not None:
        if variable.type == "int":
            t[0] = variable
        else:
            raise TypeError("Type mismatch error: Variable in for loop should be an integer.")
    else:
        raise Exception("The variable in for loop does not exist.")
    
def p_l_for_np2(t):
    '''
    l_for_np2 :
    '''
    left_type, left_address = t[-3].process_variable()
    left_name = t[-3].name
    if type(t[-1]) is tuple:
        right_type, right_address = t[-1]
    else:
        right_type, right_address = t[-1].process_variable()
    operation_type = SemanticCube().get_result_type(left_type, "=", right_type)
    if left_name is not None and context_stack.check_variable_exists(left_name):
        quadruples.add_quad(Quad("=", right_address, None, left_address))
        t[0] = (operation_type, left_address)
    else:
        raise Exception(f"Only variables may be assigned to.")
    jumps.append(quadruples.instr_ptr)

def p_l_for_np3(t):
    '''
    l_for_np3 :
    '''
    if type(t[-4]) is tuple:
        left_type, left_address = t[-4]
    else:
        left_type, left_address = t[-4].process_variable()
    if type(t[-1]) is tuple:
        right_type, right_address = t[-1]
    else:
        right_type, right_address = t[-1].process_variable()
    operation_type = SemanticCube().get_result_type(left_type, "<", right_type)
    address = temporal_memory_manager.reserve_space(operation_type)
    quadruples.add_quad(Quad("<", left_address, right_address, address))
    jumps.append(quadruples.instr_ptr)
    quadruples.add_quad(Quad("GOTOF", address, None, None))

def p_f_call(t):
    '''
    f_call : ID LPAREN args RPAREN
    '''
    f_name = t[1]
    f_args = t[3]
    
    if function_directory.check_function_exists(f_name):
        function = function_directory.get_function_from_directory(f_name)
        f_params = function.parameters
        if len(f_params) != len(f_args):
            raise Exception(f"The amount of function parameters and call arguments does not match for function '{f_name}'.")
        else:
            quadruples.add_quad(Quad("ERA", None, None, function.address))
            for param, arg in zip(f_params, f_args):
                p = param
                if type(arg) == Variable:
                    a_type = arg.type
                    a_address = arg.address
                else:
                    a_type, a_address = arg
                if (p.type == a_type):
                    quadruples.add_quad(Quad("PARAM", a_address, None, p.address))
                else:
                    raise TypeError(f"One or more call arguments in function '{f_name}' do not match the parameter types")
            quadruples.add_quad(Quad("GOSUB", None, None, function.address))
            if function.return_type != "void":
                r_address = temporal_memory_manager.reserve_space(function.return_type)
                quadruples.add_quad(Quad("=", function.return_address, None, r_address))
            else:
                r_address = function.return_address
            t[0] = (function.return_type, r_address)
    else:
        raise Exception(f"The function named '{f_name}' was not declared.")

def p_args(t):
    '''
    args : expression COMMA args
         | expression
         |
    '''
    if len(t) == 4:
        t[0] = [t[1], *t[3]]
    elif len(t) == 1:
        t[0] = []
    else:
        t[0] = [t[1]]

def p_return(t):
    '''
    return : RETURN expression SEMICOLON
    '''
    if type(t[2]) is tuple:
        expr_type, expr_address = t[2]
    else:
        expr_type, expr_address = t[2].process_variable()
    f_name = function_stack[-1]
    
    if function_directory.check_function_exists(f_name):
        function = function_directory.get_function_from_directory(f_name)
        if function.return_type == "void":
            raise Exception("A return statement cannot be used inside a function of type void.")
        elif function.return_address is not None and expr_type == function.return_type:
            quadruples.add_quad(Quad("=", expr_address, None, function.return_address))
            quadruples.add_quad(Quad("ENDSUB", None, None, None))
            function.return_bool = True
        else:
            raise Exception(f"The item returned for the function named '{f_name}' does not match its expected return type.")
    else:
        raise Exception("Return statements must be inside a function.")

def p_function(t):
    '''
    function : function_t function_p function_np1 function_np2 block
             | function_v function_p function_np1 function_np2 block
    '''
    f_name = function_stack.pop()
    context_stack.pop()
    function = function_directory.get_function_from_directory(f_name)
    
    if function.return_type != "void" and not function.return_bool:
        raise Exception(f"Function of type '{function.return_type}' is missing a return statement.")
    
    function.resources = temporal_memory_manager.get_resources()
    
    if function.return_type == "void":
        quadruples.add_quad(Quad("ENDSUB", None, None, None))
    
    # temporal_memory_manager.print()
    temporal_memory_manager.clear_memory_values()

def p_function_t(t):
    '''
    function_t : type FUNCTION ID
    function_v : VOID FUNCTION ID
    '''
    f_type = t[1]
    f_id = t[3]
    t[0] = (f_type, f_id)

def p_function_p(t):
    '''
    function_p : LPAREN RPAREN
               | LPAREN params RPAREN
    '''
    if len(t) == 3:
        t[0] = []
    else:
        t[0] = t[2]
    
def p_function_np1(t):
    '''
    function_np1 :
    '''
    f_type, f_name = t[-2]
    f_params = t[-1]
    # Check there isn't another function with same name
    if function_directory.check_function_exists(f_name):
        raise Exception(f"There is already a function with the name '{f_name}' in the directory.")
    # Reserve space for return
    if f_type == "void":
        return_address = None
    else:
        return_address = data_memory_manager.reserve_space(f_type)
    # Add function to memory, function directory, and to the context stack
    f_context = Context("function", temporal_memory_manager)
    f_address = data_memory_manager.add_value_to_memory(f_name)
    function = function_directory.add_function_to_directory(f_name, f_type, return_address, f_address, f_context)
    context_stack.push(f_context)
    # Update function parameters
    for p_type, p_name in f_params:
        variable = context_stack.add_variable_to_stack(p_name, p_type)
        function.parameters.append(Variable(p_name, p_type, variable.address))
    # Save in function stack
    function_stack.append(f_name)
    
def p_function_np2(t):
    '''
    function_np2 :
    '''
    f_name = function_stack[-1]
    function_directory.get_function_from_directory(f_name).initial_quad_address = quadruples.instr_ptr
    
def p_params_t(t):
    '''
    params_t : type ID
    '''
    f_type = t[1]
    f_id = t[2]
    t[0] = (f_type, f_id)

def p_params(t):
    '''
    params : params_t COMMA params
           | params_t
    '''
    if len(t) == 4:
        t[0] = [t[1], *t[3]]
    else:
        t[0] = [t[1]]
    
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
        quadruples.add_quad(Quad("=", right_address, None, left_address))
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
    quadruples.add_quad(Quad(t[2], left_address, right_address, address))
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