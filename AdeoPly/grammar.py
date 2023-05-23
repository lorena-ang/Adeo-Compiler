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
from array_manager import ArrayManager
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
constant_memory_manager = MemoryManager(5000)
temporal_memory_manager = MemoryManager(10000)

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
    # Add as a function to the function directory
    function_name = "main"
    address = global_memory_manager.find_address_or_add_value_to_memory(function_name)
    function_directory.add_function_to_directory(function_name, "void", None, address, context_stack.contexts[-1])
    function = function_directory.get_function_from_directory(function_name)
    function.initial_quad_address = quadruples.instr_ptr
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
    # Add context information for main function in function directory
    function_name = "main"
    address = global_memory_manager.find_address_or_add_value_to_memory(function_name)
    quadruples[0] = Quad("ERA", None, None, address)
    function = function_directory.get_function_from_directory(function_name)
    function.resources = context_stack.contexts[-1].context_memory_manager.get_resources()
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
    # Modify the quadruple associated with the last jump to point to the current instruction pointer
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
    # Check that the conditional expression is boolean
    if type != "bool":
        raise_program_error(ProgramErrorType.TYPE_MISMATCH, t.lineno(0), "Expression should be boolean")
    # Save current instruction pointer as a jump target for the GOTOFs
    jumps.append(quadruples.instr_ptr)
    # Add a GOTOF quadruple with the conditional address
    quadruples.add_quad(Quad("GOTOF", address, None, None))
    
def p_conditional_np2(t):
    '''
    conditional_np2 :
    '''
    # Save the current instruction pointer as a jump target for the end of the IF
    end_jumps.append(quadruples.instr_ptr)
    # Increase the count of pending end jumps
    end_count[-1] += 1
    # Add a GOTO quadruple to ELSEIF conditional
    quadruples.add_quad(Quad("GOTO", None, None, None))
    # Update the value of the previous GOTOF to point to the current instruction pointer
    last_jump = jumps.pop()
    quad = quadruples[last_jump]
    address = constant_memory_manager.find_address_or_add_value_to_memory(quadruples.instr_ptr)
    quadruples[last_jump] = Quad(quad.operator, quad.left_address, None, address)

def p_conditional_np3(t):
    '''
    conditional_np3 :
    '''
    # Add a GOTO quadruple to the ELSE conditional
    quadruples.add_quad(Quad("GOTO", None, None, None))
    # Update the value of the previous GOTOF to point to the current instruction pointer
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
        # Print a constant
        if type(elem) == tuple:
            quadruples.add_quad(Quad("PRINT", None, None, elem[1]))
        # Print a variable
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
    # Add GOTO to return to the beginning of the loop
    address = constant_memory_manager.find_address_or_add_value_to_memory(second_last_jump)
    quadruples.add_quad(Quad("GOTO", None, None, address))
    quad = quadruples[last_jump]
    # Update GOTO at the end of the loop to point to the current instruction
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
    # Look for constant 1 or save it
    value = 1
    one_address = constant_memory_manager.find_address_or_add_value_to_memory(value)
    # Add one to the loop variable
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
    # Check that variable to be used in for loop is an int and is declared
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
    # Determine the result type based on the left and right types
    operation_type = SemanticCube().get_result_type(left_type, "=", right_type)
    if operation_type == "TypeMismatch":
        raise_program_error(ProgramErrorType.TYPE_MISMATCH, t.lineno(1), "Operand does not match data type")
    # Make sure the element to assign value to is a variable that exists in the context
    if left_name is not None and context_stack.check_variable_exists(left_name):
        quadruples.add_quad(Quad("=", right_address, None, left_address))
        t[0] = (operation_type, left_address)
    # Save the instruction pointer for later use in jumps
    jumps.append(quadruples.instr_ptr)

def p_l_for_np3(t):
    '''
    l_for_np3 :
    '''
    left_type, left_address = data_processor.process_data(t[-4])
    right_type, right_address = data_processor.process_data(t[-1])
    # Determine the result type based on the left and right types
    operation_type = SemanticCube().get_result_type(left_type, "<", right_type)
    if operation_type == "TypeMismatch":
        raise_program_error(ProgramErrorType.TYPE_MISMATCH, t.lineno(1), "Operand does not match data type")
    # Reserve a temporary space to store the result
    address = temporal_memory_manager.reserve_space(operation_type)
    quadruples.add_quad(Quad("<", left_address, right_address, address))
    # Save the instruction pointer of the GOTOF quadruple for later use
    jumps.append(quadruples.instr_ptr)
    quadruples.add_quad(Quad("GOTOF", address, None, None))

def p_f_call(t):
    '''
    f_call : ID LPAREN args RPAREN
    '''
    f_name = t[1]
    f_args = t[3]
    # Check that function has been declared
    if not function_directory.check_function_exists(f_name):
        raise_program_error(ProgramErrorType.UNDECLARED_IDENTIFIER, t.lineno(1), f"The function named '{f_name}' was not declared")
    function = function_directory.get_function_from_directory(f_name)
    f_params = function.parameters
    # Check if amount of parameters matches amount of arguments
    if len(f_params) != len(f_args):
        raise_program_error(ProgramErrorType.MISSING_REQUIRED_ARGUMENT, t.lineno(1), f"The amount of call arguments does not match the amount of parameters for function '{f_name}'")
    quadruples.add_quad(Quad("ERA", None, None, function.address))
    # Process each parameter and argument pair
    for param, arg in zip(f_params, f_args):
        p = param
        a_type, a_address = data_processor.process_data(arg)
        # Check that parameter and argument match types
        if p.type != a_type:
            raise_program_error(ProgramErrorType.TYPE_MISMATCH, t.lineno(1), f"One or more call arguments in function '{f_name}' do not match the parameter types")
        quadruples.add_quad(Quad("PARAM", a_address, None, p.address))
    quadruples.add_quad(Quad("GOSUB", None, None, function.address))
    if function.return_type != "void":
        # Generate assignment quadruple for return value
        r_address = temporal_memory_manager.reserve_space(function.return_type)
        quadruples.add_quad(Quad("=", function.return_address, None, r_address))
    else:
        r_address = function.return_address
    t[0] = (function.return_type, r_address)

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
    # Check that return statement is inside a function
    try:
        f_name = function_stack[-1]
    except IndexError:
        raise_program_error(ProgramErrorType.UNSUPPORTED_OPERATION, t.lineno(1), "Return statements must be inside a function")
    # Check that the function was declared
    if not function_directory.check_function_exists(f_name):
        raise_program_error(ProgramErrorType.UNDECLARED_IDENTIFIER, t.lineno(1), f"The function named '{f_name}' was not declared")
    function = function_directory.get_function_from_directory(f_name)
    # Check that the return is not in a void function
    if function.return_type == "void":
        raise_program_error(ProgramErrorType.UNSUPPORTED_OPERATION, t.lineno(1), f"A return statement cannot be used inside function '{f_name}' because it is of type void")
    # Check that the type of the expr returned matches the expected type
    if function.return_address is not None and expr_type == function.return_type:
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
    # Check if a return statement is missing for non-void functions
    if function.return_type != "void" and not function.return_bool:
        raise_program_error(ProgramErrorType.RETURN_STATEMENT_MISSING, t.lineno(0), f"The function named '{f_name}' is missing a return statement")
    function.resources = temporal_memory_manager.get_resources()
    # Add ENDFUNC quad for void functions
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
    if function_directory.check_function_exists(f_name):
        raise_program_error(ProgramErrorType.REDECLARATION_ERROR, t.lineno(0), f"There is already a function named '{f_name}' in the directory")
    # Reserve space for the return value
    if f_type == "void":
        return_address = None
    else:
        return_address = global_memory_manager.reserve_space(f_type)
    # Add function to memory, function directory, and the context stack
    f_context = Context("Function", temporal_memory_manager)
    f_address = global_memory_manager.add_value_to_memory(f_name)
    function = function_directory.add_function_to_directory(f_name, f_type, return_address, f_address, f_context)
    context_stack.push(f_context)
    # Update function parameters
    for p_type, p_name in f_params:
        # Check if another parameter with the same name already exists
        if context_stack.contexts[-1].check_variable_exists(p_name):
            raise_program_error(ProgramErrorType.REDECLARATION_ERROR, t.lineno(0), f"There is already a parameter named '{p_name}' in the directory")
        variable = context_stack.contexts[-1].add_variable_to_context(p_name, p_type)
        function.parameters.append(Variable(p_name, p_type, variable.address))
    # Save the function name in the function stack
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
            # Check if it's a single variable
            if type(var) == str:
                if context_stack.contexts[-1].check_variable_exists(var):
                    raise_program_error(ProgramErrorType.REDECLARATION_ERROR, t.lineno(1), f"There is already a variable named '{var}' in the directory")
                context_stack.contexts[-1].add_variable_to_context(var, v_type)
            # Check if it's an array variable
            else:
                if context_stack.contexts[-1].check_variable_exists(var[0]):
                    raise_program_error(ProgramErrorType.REDECLARATION_ERROR, t.lineno(1), f"There is already a variable named '{var[0]}' in the directory")
                array_manager = ArrayManager()
                for _, base_ad in var[1]:
                    val = constant_memory_manager[base_ad]
                    array_manager.add_dimension(val)
                array_manager.update_dimension()
                context_stack.contexts[-1].add_variable_to_context(var[0], v_type, array_manager)
    # For class objects
    else:
        c_name = t[2]
        variables = t[4]
        # Check if the class has been declared
        if not class_directory.check_class_exists(c_name):
            raise_program_error(ProgramErrorType.UNDECLARED_IDENTIFIER, t.lineno(1), f"The class '{c_name}' has not been declared")
        class_detail = class_directory.get_class_from_directory(c_name)
        for var in variables:
            # Check if variable name was already used
            if context_stack.check_variable_exists(var):
                raise_program_error(ProgramErrorType.REDECLARATION_ERROR, t.lineno(1), f"There is already a variable named '{var}' in the directory")
            # Add class variable to the context stack
            context_stack.contexts[-1].add_variable_to_context(var, c_name)
            # Add attributes as variables to the context
            for value in class_detail.variable_table.variables.values():
                nested_var = f"{var}.{value.name}"
                context_stack.contexts[-1].add_variable_to_context(nested_var, value.type)

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
    t[0] = (t[1], t[2])

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
        dim = None
    elif len(t) == 4:
        c_name = t[1]
        v_name = f"{c_name}.{t[3]}"
        dim = None
    else:
        v_name = t[1]
        dim = t[2]
    # Check that variable was declared
    if not context_stack.check_variable_exists(v_name):
        raise_program_error(ProgramErrorType.UNDECLARED_IDENTIFIER, t.lineno(1), f"The variable '{v_name}' has not been declared")
    variable = context_stack.get_variable_from_context(v_name)
    # If simple variable or object
    if variable.array_manager is None or dim is None:
        t[0] = variable
    else:
        array_manager = variable.array_manager
        # Check if the number of dimensions entered while trying to index is the same as the array's
        if len(dim) != len(array_manager.dimensions):
            raise_program_error(ProgramErrorType.ARRAY_INDEX_OUT_OF_BOUNDS, t.lineno(1), f"Wrong indexing when trying to access '{v_name}'")
        addresses = []
        lower_lim = constant_memory_manager.find_address_or_add_value_to_memory(0)
        for i, (dim, param) in enumerate(zip(array_manager.dimensions, dim)):
            addresses.append(param[1])
            if param[0] != "int":
                raise_program_error(ProgramErrorType.UNSUPPORTED_OPERATION, t.lineno(1), f"Cannot index '{v_name}' with a non-int expression")
            upper_lim = constant_memory_manager.find_address_or_add_value_to_memory(dim.upper_lim)
            m = constant_memory_manager.find_address_or_add_value_to_memory(dim.m)
            # Add VER quadruple to check if the index is within bounds
            quadruples.add_quad(Quad("VER", param[1], lower_lim, upper_lim))
            # If it's the first dimension of the array
            if i > 0:
                t1 = addresses.pop()
                t2 = addresses.pop()
                t3 = temporal_memory_manager.reserve_space("int")
                quadruples.add_quad(Quad("+", t2, t1, t3))
                addresses.append(t3)
            # If it's not the last dimension of the array
            if i < len(array_manager.dimensions) - 1:
                t1 = temporal_memory_manager.reserve_space("int")
                # S * m
                quadruples.add_quad(Quad("*", addresses.pop(), m, t1))
                addresses.append(t1)
        # Add the address of index value and base address, and store the result in t1
        base_address = constant_memory_manager.find_address_or_add_value_to_memory(variable.address)
        t1 = temporal_memory_manager.reserve_space("int")
        quadruples.add_quad(Quad("+", addresses.pop(), base_address, t1))
        # Create a pointer quad to store t1 in t2
        t2 = temporal_memory_manager.reserve_space("ptr")
        quadruples.add_quad(Quad("PTR", t1, None, t2))
        t[0] = Variable(variable.name, variable.type, t2)

def p_class(t):
    '''
    class : CLASS ID class_np1 LBRACE class_attributes class_np2 RBRACE SEMICOLON
    '''
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

def p_class_np1(t):
    '''
    class_np1 :
    '''
    c_name = t[-1]
    # Check if class name was already used
    if class_directory.check_class_exists(c_name):
        raise_program_error(ProgramErrorType.REDECLARATION_ERROR, t.lineno(0), f"There is already a class named '{c_name}' in the directory")
    # Add class to the class directory
    class_directory.add_class_to_directory(c_name)
    class_detail = class_directory.get_class_from_directory(c_name)
    # Push a new context for the class to the context stack
    context_stack.push(Context("Class", global_memory_manager, class_detail.variable_table))
    t[0] = c_name
    
def p_class_np2(t):
    '''
    class_np2 :
    '''
    attributes = t[-1]
    # Process each attribute in the class
    for atr in attributes:
        a_type, a_name = atr
        # Check if the attribute type is of simple type
        if data_processor.check_type_simple(a_type):
            if context_stack.check_variable_exists(a_name):
                raise_program_error(ProgramErrorType.REDECLARATION_ERROR, t.lineno(0), f"There is already an attribute named '{a_name}' in the directory")
            # Add attribute to the current context in the context stack
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
    # Determine the result type based on the left and right types
    operation_type = SemanticCube().get_result_type(left_type, t[2], right_type)
    if operation_type == "TypeMismatch":
        raise_program_error(ProgramErrorType.TYPE_MISMATCH, t.lineno(1), "Operand does not match data type")
    # Make sure the element to assign the value to is a variable that exists in the context
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
    # Determine the result type based on the left and right types
    operation_type = SemanticCube().get_result_type(left_type, t[2], right_type)
    if operation_type == "TypeMismatch":
        raise_program_error(ProgramErrorType.TYPE_MISMATCH, t.lineno(1), "Operand does not match data type")
    # Reserve a temporary space to store the result
    address = temporal_memory_manager.reserve_space(operation_type)
    # Add the quadruple for the operation
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