from typing import Tuple
from variable_table import Variable

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
        return (type == "int" or type == "float" or type == "string" or type == "bool")