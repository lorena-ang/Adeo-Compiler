from typing import Tuple
from variable_table import Variable
import re

class DataProcessor:
    # Returns a tuple with the type and address if data is a variable
    def process_data(self, data) -> Tuple[str, int]:
        if isinstance(data, Variable):
            return (data.type, data.address)
        elif isinstance(data, tuple):
            return data
        else:
            raise ValueError("Invalid variable format")
            
    # Checks that a string with the type is simple
    def check_type_simple(self, type: str) -> bool:
        simple_types = {"int", "float", "string", "bool"}
        return type in simple_types
    
    # Return the value in a specific data type
    def change_to_type(self, type: str, value: str):
        if type == 'int':
            return int(value) if value != 'None' else None
        elif type == 'float':
            return float(value) if value != 'None' else None
        elif type == 'string':
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            return value if value != 'None' else None
        else:
            if value == "true":
                return "true"
            elif value == "false":
                return "false"
            else:
                return None