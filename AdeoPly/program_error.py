class ProgramError(Exception):
    """
    Represents an error that occurs during program execution.
    
    Attributes:
        error_type (str): The type of the error.
        line_num (int): The line number where the error occurred.
        description (str): A description of the error.
    """

    def __init__(self, error_type: str, line_num: int, description: str):
        self.error_type = error_type
        self.line_num = line_num
        self.description = description

class ProgramErrorType:
    """
    Represents the types of program errors that can occur.
    """
    ARITHMETIC_EXCEPTION = "ARITHMETIC_EXCEPTION"
    ARRAY_INDEX_OUT_OF_BOUNDS = "ARRAY_INDEX_OUT_OF_BOUNDS"
    INPUT_TYPE_MISMATCH = "INPUT_TYPE_MISMATCH"
    MISSING_REQUIRED_ARGUMENT = "MISSING_REQUIRED_ARGUMENT"
    REDECLARATION_ERROR = "REDECLARATION_ERROR"
    RETURN_STATEMENT_MISSING = "RETURN_STATEMENT_MISSING"
    RETURN_TYPE_MISMATCH = "RETURN_TYPE_MISMATCH"
    SYNTAX_ERROR = "SYNTAX_ERROR"
    TYPE_MISMATCH = "TYPE_MISMATCH"
    UNDECLARED_IDENTIFIER = "UNDECLARED_IDENTIFIER"
    UNSUPPORTED_OPERATION = "UNSUPPORTED_OPERATION"
    VARIABLE_NOT_INITIALIZED = "VARIABLE_NOT_INITIALIZED"

def raise_program_error(error_type: str, line_num: int | None, description: str):
    """
    Raise a ProgramError with the specified error type, line number, and description.

    Parameters:
        error_type (str): The type of the program error.
        line_num (int | None): The line number where the error occurred.
        description (str): A description of the error.
    """
    raise ProgramError(error_type, line_num, description)