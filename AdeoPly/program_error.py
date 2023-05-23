class ProgramError(Exception):    
    def __init__(self, error_type: str, line_num: int, description: str):
        self.error_type = error_type
        self.line_num = line_num
        self.description = description
        error_message = f"{error_type} at line {line_num}: {description}."
        super().__init__(error_message)

class ProgramErrorType:
    ARRAY_INDEX_OUT_OF_BOUNDS = "ARRAY_INDEX_OUT_OF_BOUNDS"
    MISSING_REQUIRED_ARGUMENT = "MISSING_REQUIRED_ARGUMENT"
    REDECLARATION_ERROR = "REDECLARATION_ERROR"
    RETURN_STATEMENT_MISSING = "RETURN_STATEMENT_MISSING"
    RETURN_TYPE_MISMATCH = "RETURN_TYPE_MISMATCH"
    SYNTAX_ERROR = "SYNTAX_ERROR"
    TYPE_MISMATCH = "TYPE_MISMATCH"
    UNDECLARED_IDENTIFIER = "UNDECLARED_IDENTIFIER"
    UNSUPPORTED_OPERATION = "UNSUPPORTED_OPERATION"
    VARIABLE_NOT_INITIALIZED = "VARIABLE_NOT_INITIALIZED"

def raise_program_error(error_type: str, line_num: int, description: str):
    raise ProgramError(error_type, line_num, description)