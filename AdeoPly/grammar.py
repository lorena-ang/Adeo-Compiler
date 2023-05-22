# -----------------------------------------------------------------------------
# grammar.py
#
# Adeo grammar file for use with PLY library
# -----------------------------------------------------------------------------

import sys
from variable_table import Variable
from semantic_cube import SemanticCube
from memory_manager import MemoryManager
from quadruples import Quad, Quadruples
from function_directory import FunctionDirectory
from class_directory import ClassDirectory
from stack import Context, Stack
from data_processor import DataProcessor
from program_error import raise_program_error, ProgramErrorType
from typing import Tuple

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
    t.lexer.lineno += t.value.count('\n')

def t_error(t):
    print(f"Illegal character '{t.value[0]!r}' in line {t.lineno}")
    t.lexer.skip(1)

# Build the lexer
import ply.lex as lex
lexer = lex.lex()

#
# PARSER
#

# Memory management
global_memory_manager = MemoryManager(0)
constant_memory_manager = MemoryManager(4000)
temporal_memory_manager = MemoryManager(8000)

context_stack = Stack()
context_stack.push(Context("Global", global_memory_manager))

quadruples = Quadruples()
quadruples.add_quad(Quad("ERA", None, None, None))
quadruples.add_quad(Quad("GOSUB", None, None, None))
main_resources: str = ""
main_initial_quad: int = 0

# Class management
class_directory = ClassDirectory()

# Function management
function_directory = FunctionDirectory()
function_stack: list[str] = []

# Jump and counter stacks
jumps: list[int] = []
end_count: list[int] = []
end_jumps: list[int] = []

# Helper class for data processing
data_processor = DataProcessor()

def p_program(t):
    '''
    program : class_decl variables_decl function_decl main m_block end_program
    '''
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
    
def p_main(t):
    '''
    main : MAIN LPAREN RPAREN
    '''
    address = global_memory_manager.find_address_or_add_value_to_memory("main")
    function_directory.add_function_to_directory("main","void",None,address,context_stack.contexts[-1])
    function_directory.get_function_from_directory("main").initial_quad_address = quadruples.instr_ptr
    quadruples[1] = Quad("GOSUB", None, None, address)

def p_end_program(t):
    '''
    end_program :
    '''
    quadruples.add_quad(Quad("ENDPROG", None, None, None))

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
    block_1 : statement block_1
            |
    m_block : LBRACE b_push_context variables_decl block_1 RBRACE mb_pop_context
    l_block : LBRACE l_push_context block_1 RBRACE l_pop_context
    c_block : LBRACE block_1 RBRACE
    '''
    
def p_b_push_context(t):
    '''
    b_push_context :
    '''
    context_stack.push(Context("Local", temporal_memory_manager))
    
def p_b_pop_context(t):
    '''
    b_pop_context :
    '''
    context_stack.pop()

def p_mb_pop_context(t):
    '''
    mb_pop_context :
    '''
    address = global_memory_manager.find_address_or_add_value_to_memory("main")
    quadruples[0] = Quad("ERA", None, None, address)
    function_directory.get_function_from_directory("main").resources = context_stack.contexts[-1].context_memory_manager.get_resources()
    context_stack.pop()
    
def p_l_push_context(t):
    '''
    l_push_context :
    '''
    context_stack.push(Context("Loop", temporal_memory_manager))
    end_count.append(0)

def p_l_pop_context(t):
    '''
    l_pop_context :
    '''
    context_stack.pop()
    for _ in range(end_count.pop()):
        address = constant_memory_manager.find_address_or_add_value_to_memory(quadruples.instr_ptr)
        quadruples[end_jumps.pop()] = Quad("GOTO", None, None, address)

def p_conditional(t):
    '''
    conditional : IF LPAREN expression conditional_np1 RPAREN l_push_context c_block conditional_1 l_pop_context
    '''
    last_jump = jumps.pop()
    quad = quadruples[last_jump]
    address = constant_memory_manager.find_address_or_add_value_to_memory(quadruples.instr_ptr)
    quadruples[last_jump] = Quad(quad.operator, quad.left_address, None, address)
    
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
    type, address = data_processor.process_data(t[-1])
    if type != "bool":
        raise_program_error(ProgramErrorType.TYPE_MISMATCH, t.lineno(0), "Expression should be boolean")
    jumps.append(quadruples.instr_ptr)
    quadruples.add_quad(Quad("GOTOF", address, None, None))
    
def p_conditional_np2(t):
    '''
    conditional_np2 :
    '''
    end_jumps.append(quadruples.instr_ptr)
    end_count[-1] += 1
    quadruples.add_quad(Quad("GOTO", None, None, None))
    last_jump = jumps.pop()
    quad = quadruples[last_jump]
    address = constant_memory_manager.find_address_or_add_value_to_memory(quadruples.instr_ptr)
    quadruples[last_jump] = Quad(quad.operator, quad.left_address, None, address)

def p_conditional_np3(t):
    '''
    conditional_np3 :
    '''
    quadruples.add_quad(Quad("GOTO", None, None, None))
    last_jump = jumps.pop()
    jumps.append(quadruples.instr_ptr - 1)
    quad = quadruples[last_jump]
    address = constant_memory_manager.find_address_or_add_value_to_memory(quadruples.instr_ptr)
    quadruples[last_jump] = Quad(quad.operator, quad.left_address, None, address)

def p_write(t):
    '''
    write : PRINT LPAREN write_1 RPAREN SEMICOLON
    '''
    elements = t[3]
    if elements is None:
        raise_program_error(ProgramErrorType.UNSUPPORTED_OPERATION, t.lineno(1), "The data to be printed is invalid")
    for elem in elements:
        if type(elem) == tuple:
            quadruples.add_quad(Quad("PRINT", None, None, elem[1]))
        elif type(elem) == Variable:
            address = elem.address
            quadruples.add_quad(Quad("PRINT", None, None, address))

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
    variable = t[3]
    if variable is None:
        raise_program_error(ProgramErrorType.UNDECLARED_IDENTIFIER, t.lineno(1), f"The variable '{t[3]}' has not been declared")
    address = variable.address
    quadruples.add_quad(Quad("READ", None, None, address))

def p_l_while(t):
    '''
    l_while : WHILE LPAREN l_while_np1 expression conditional_np1 RPAREN l_block
    '''
    last_jump = jumps.pop()
    second_last_jump = jumps.pop()
    address = constant_memory_manager.find_address_or_add_value_to_memory(second_last_jump)
    quadruples.add_quad(Quad("GOTO", None, None, address))
    quad = quadruples[last_jump]
    address = constant_memory_manager.find_address_or_add_value_to_memory(quadruples.instr_ptr)
    quadruples[last_jump] = Quad(quad.operator, quad.left_address, None, address)
    
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
    one_address = constant_memory_manager.find_address_or_add_value_to_memory(value)
    # Add one
    left_type, left_address = data_processor.process_data(t[2])
    operation_type = SemanticCube().get_result_type(left_type, "+", "int")
    if operation_type == "TypeMismatch":
        raise_program_error(ProgramErrorType.TYPE_MISMATCH, t.lineno(1), "Operand does not match data type")
    address = global_memory_manager.reserve_space(operation_type)
    quadruples.add_quad(Quad("+", left_address, one_address, address))
    quadruples.add_quad(Quad("=", address, one_address, left_address))
    # Update quadruples
    address = constant_memory_manager.find_address_or_add_value_to_memory(first_jump)
    quadruples.add_quad(Quad("GOTO", None, None, address))
    quad = quadruples[last_jump]
    address = constant_memory_manager.find_address_or_add_value_to_memory(quadruples.instr_ptr)
    quadruples[last_jump] = Quad(quad.operator, quad.left_address, None, address)

def p_l_for_np1(t):
    '''
    l_for_np1 : ID
    '''
    variable = context_stack.get_variable_from_context(t[1])
    if variable is not None:
        if variable.type == "int":
            t[0] = variable
        else:
            raise_program_error(ProgramErrorType.TYPE_MISMATCH, t.lineno(1), "Variable in for loop should be an integer")
    else:
        raise_program_error(ProgramErrorType.UNDECLARED_IDENTIFIER, t.lineno(1), f"The variable '{t[1]}' has not been declared")
    
def p_l_for_np2(t):
    '''
    l_for_np2 :
    '''
    left_name = t[-3].name
    left_type, left_address = data_processor.process_data(t[-3])
    right_type, right_address = data_processor.process_data(t[-1])
    operation_type = SemanticCube().get_result_type(left_type, "=", right_type)
    if operation_type == "TypeMismatch":
        raise_program_error(ProgramErrorType.TYPE_MISMATCH, t.lineno(1), "Operand does not match data type")
    if left_name is not None and context_stack.check_variable_exists(left_name):
        quadruples.add_quad(Quad("=", right_address, None, left_address))
        t[0] = (operation_type, left_address)
    jumps.append(quadruples.instr_ptr)

def p_l_for_np3(t):
    '''
    l_for_np3 :
    '''
    left_type, left_address = data_processor.process_data(t[-4])
    right_type, right_address = data_processor.process_data(t[-1])
    operation_type = SemanticCube().get_result_type(left_type, "<", right_type)
    if operation_type == "TypeMismatch":
        raise_program_error(ProgramErrorType.TYPE_MISMATCH, t.lineno(1), "Operand does not match data type")
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
            raise_program_error(ProgramErrorType.MISSING_REQUIRED_ARGUMENT, t.lineno(1), f"The amount of call arguments does not match the amount of parameters for function '{f_name}'")
        else:
            quadruples.add_quad(Quad("ERA", None, None, function.address))
            for param, arg in zip(f_params, f_args):
                p = param
                a_type, a_address = data_processor.process_data(arg)
                if (p.type == a_type):
                    quadruples.add_quad(Quad("PARAM", a_address, None, p.address))
                else:
                    raise_program_error(ProgramErrorType.TYPE_MISMATCH, t.lineno(1), f"One or more call arguments in function '{f_name}' do not match the parameter types")
            quadruples.add_quad(Quad("GOSUB", None, None, function.address))
            if function.return_type != "void":
                r_address = temporal_memory_manager.reserve_space(function.return_type)
                quadruples.add_quad(Quad("=", function.return_address, None, r_address))
            else:
                r_address = function.return_address
            t[0] = (function.return_type, r_address)
    else:
        raise_program_error(ProgramErrorType.UNDECLARED_IDENTIFIER, t.lineno(1), f"The function named '{f_name}' was not declared")

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
    expr_type, expr_address = data_processor.process_data(t[2])
    try:
        f_name = function_stack[-1]
    except IndexError:
        raise_program_error(ProgramErrorType.UNSUPPORTED_OPERATION, t.lineno(1), "Return statements must be inside a function")
    if function_directory.check_function_exists(f_name):
        function = function_directory.get_function_from_directory(f_name)
        if function.return_type == "void":
            raise_program_error(ProgramErrorType.UNSUPPORTED_OPERATION, t.lineno(1), f"A return statement cannot be used inside function '{f_name}' because it is of type void")
        elif function.return_address is not None and expr_type == function.return_type:
            quadruples.add_quad(Quad("=", expr_address, None, function.return_address))
            quadruples.add_quad(Quad("ENDFUNC", None, None, None))
            function.return_bool = True
        else:
            raise_program_error(ProgramErrorType.RETURN_TYPE_MISMATCH, t.lineno(1), f"The item returned for the function '{f_name}' does not match its expected return type")

def p_function(t):
    '''
    function : function_t function_p function_np1 function_np2 block
             | function_v function_p function_np1 function_np2 block
    '''
    f_name = function_stack.pop()
    function = function_directory.get_function_from_directory(f_name)
    if function.return_type != "void" and not function.return_bool:
        raise_program_error(ProgramErrorType.RETURN_STATEMENT_MISSING, t.lineno(0), f"The function named '{f_name}' is missing a return statement")
    function.resources = temporal_memory_manager.get_resources()
    if function.return_type == "void":
        quadruples.add_quad(Quad("ENDFUNC", None, None, None))
    temporal_memory_manager.clear_memory_values()
    context_stack.pop()

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
        raise_program_error(ProgramErrorType.REDECLARATION_ERROR, t.lineno(0), f"There is already a function named '{f_name}' in the directory")
    # Reserve space for return
    if f_type == "void":
        return_address = None
    else:
        return_address = global_memory_manager.reserve_space(f_type)
    # Add function to memory, function directory, and to the context stack
    f_context = Context("Function", temporal_memory_manager)
    f_address = global_memory_manager.add_value_to_memory(f_name)
    function = function_directory.add_function_to_directory(f_name, f_type, return_address, f_address, f_context)
    context_stack.push(f_context)
    # Update function parameters
    for p_type, p_name in f_params:
        if context_stack.contexts[-1].check_variable_exists(p_name):
            raise_program_error(ProgramErrorType.REDECLARATION_ERROR, t.lineno(0), f"There is already a parameter named '{p_name}' in the directory")
        variable = context_stack.contexts[-1].add_variable_to_context(p_name, p_type)   
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
    attributes_t : type COLON ID
    '''
    if len(t) == 3:
        f_type = t[1]
        f_id = t[2]
    else:
        f_type = t[1]
        f_id = t[3]
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
    variables : VAR type COLON variables_2 SEMICOLON
              | VAR ID COLON variables_1 SEMICOLON
    '''
    # For simple data types
    if data_processor.check_type_simple(t[2]):
        v_type = t[2]
        variables = t[4]
        for var in variables:
            if context_stack.contexts[-1].check_variable_exists(var):
                raise_program_error(ProgramErrorType.REDECLARATION_ERROR, t.lineno(1), f"There is already a variable named '{var}' in the directory")
            context_stack.contexts[-1].add_variable_to_context(var, v_type)
    # For class objects
    else:
        c_name = t[2]
        variables = t[4]
        if not class_directory.check_class_exists(c_name):
            raise_program_error(ProgramErrorType.UNDECLARED_IDENTIFIER, t.lineno(1), f"The class '{c_name}' has not been declared")
        class_detail = class_directory.get_class_from_directory(c_name)
        for var in variables:
            if context_stack.check_variable_exists(var):
                raise_program_error(ProgramErrorType.REDECLARATION_ERROR, t.lineno(1), f"There is already a variable named '{var}' in the directory")
            context_stack.contexts[-1].add_variable_to_context(var, c_name)
            for value in class_detail.variable_table.table.values():
                context_stack.contexts[-1].add_variable_to_context(f"{var}.{value.name}", value.type)
                    
def p_variables_1(t):
    '''
    variables_1 : ID COMMA variables_1
                | ID
    '''
    if len(t) == 4:
        t[0] = [t[1], *t[3]]
    else:
        t[0] = [t[1]]
        
def p_variables_2(t):
    '''
    variables_2 : ID COMMA variables_2
                | ID
                | array COMMA variables_2
                | array   
    '''
    if len(t) == 4:
        t[0] = [t[1], *t[3]]
    else:
        t[0] = [t[1]]
        
def p_array(t):
    '''
    array : ID array_dimension
    '''
    t[0] = t[1]

def p_array_dimension(t):
    '''
    array_dimension : LBRACK expr RBRACK
                    | LBRACK expr RBRACK LBRACK expr RBRACK
    '''
    if len(t) == 4:
        t[0] = [t[2]]
    elif len(t) == 7:
        t[0] = [t[2], t[5]]

def p_var(t):
    '''
    var : ID DOT ID
        | ID array_dimension
        | ID
    '''
    if len(t) == 2:
        v_name = t[1]
    elif len(t) == 4:
        c_name = t[1]
        v_name = f"{c_name}.{t[3]}"
    else:
        pass
    
    if not context_stack.check_variable_exists(v_name):
        raise_program_error(ProgramErrorType.UNDECLARED_IDENTIFIER, t.lineno(1), f"The variable '{v_name}' has not been declared")
    variable = context_stack.get_variable_from_context(v_name)
    t[0] = variable

def p_class(t):
    '''
    class : CLASS ID class_np1 LBRACE class_attributes class_np2 RBRACE SEMICOLON
    '''
    # Once class has been processed
    context_stack.pop()

def p_class_attributes(t):
    '''
    class_attributes : attributes_t COMMA class_attributes
                     | attributes_t
    '''
    if len(t) == 4:
        t[0] = [t[1], *t[3]]
    else:
        t[0] = [t[1]]

# Add class to directory and to context stack  
def p_class_np1(t):
    '''
    class_np1 :
    '''
    c_name = t[-1]
    if class_directory.check_class_exists(c_name):
        raise_program_error(ProgramErrorType.REDECLARATION_ERROR, t.lineno(0), f"There is already a class named '{c_name}' in the directory")
    class_directory.add_class_to_directory(c_name)
    class_detail = class_directory.get_class_from_directory(c_name)
    context_stack.push(Context("Class", global_memory_manager, class_detail.variable_table))
    t[0] = c_name

# Add attributes to context stack
def p_class_np2(t):
    '''
    class_np2 :
    '''
    attributes = t[-1]
    for atr in attributes:
        a_type, a_name = atr
        if data_processor.check_type_simple(a_type):
            if context_stack.check_variable_exists(a_name):
                raise_program_error(ProgramErrorType.REDECLARATION_ERROR, t.lineno(0), f"There is already an attribute named '{a_name}' in the directory")
            context_stack.contexts[-1].add_variable_to_context(a_name, a_type)     

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
    address = constant_memory_manager.find_address_or_add_value_to_memory(int(t[1]))
    t[0] = ("int", address)

def p_float_const(t):
    '''
    float_const : FLOAT_CONST
    '''
    address = constant_memory_manager.find_address_or_add_value_to_memory(float(t[1]))
    t[0] = ("float", address)

def p_string_const(t):
    '''
    string_const : STRING_CONST
    '''
    address = constant_memory_manager.find_address_or_add_value_to_memory(str(t[1]))
    t[0] = ("string", address)

def p_bool_const(t):
    '''
    bool_const : TRUE
               | FALSE
    '''
    address = constant_memory_manager.find_address_or_add_value_to_memory(str(t[1]))
    t[0] = ("bool", address)
    
def p_assignment(t):
    '''
    assignment : var ASSIGNOP assignment
               | var ASSIGNOP expression
    '''
    left_name = t[1].name
    left_type, left_address = data_processor.process_data(t[1])
    right_type, right_address = data_processor.process_data(t[3])
    operation_type = SemanticCube().get_result_type(left_type, t[2], right_type)
    if operation_type == "TypeMismatch":
        raise_program_error(ProgramErrorType.TYPE_MISMATCH, t.lineno(1), "Operand does not match data type")
    # Make sure element to assign value to is a variable that exists in context
    if left_name is not None and context_stack.check_variable_exists(left_name):
        quadruples.add_quad(Quad("=", right_address, None, left_address))
        t[0] = (operation_type, left_address)

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
    left_type, left_address = data_processor.process_data(t[1])
    right_type, right_address = data_processor.process_data(t[3])
    operation_type = SemanticCube().get_result_type(left_type, t[2], right_type)
    if operation_type == "TypeMismatch":
        raise_program_error(ProgramErrorType.TYPE_MISMATCH, t.lineno(1), "Operand does not match data type")
    address = temporal_memory_manager.reserve_space(operation_type)
    quadruples.add_quad(Quad(t[2], left_address, right_address, address))
    t[0] = (operation_type, address)

# Syntax error
def p_error(t):
    raise_program_error(ProgramErrorType.SYNTAX_ERROR, t.lineno, f"Invalid syntax in value '{t.value}'")
    
def get_data_to_compiler():
    data: list[str] = []
    d_temp = "--Global Memory--"
    d_temp += "\n(" + ",".join(str(item) for item in global_memory_manager.get_resources()) + ")"
    d_temp += str(global_memory_manager)
    data.append(d_temp)
    d_temp = "\n--Constants--"
    d_temp += "\n(" + ",".join(str(item) for item in constant_memory_manager.get_resources()) + ")"
    d_temp += str(constant_memory_manager)
    data.append(d_temp)
    d_temp = "\n--Functions--" + str(function_directory)
    data.append(d_temp)
    d_temp = "\n--Classes--" + str(class_directory)
    data.append(d_temp)
    d_temp = "\n--Quadruples--" + str(quadruples)
    data.append(d_temp)
    return data

# Build the parser
import ply.yacc as yacc
parser = yacc.yacc()