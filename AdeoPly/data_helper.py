from variable_table import Variable
from typing import Tuple

class DataHelper:
    """
    The DataHelper class provides utility methods for data processing and type checking.

    Methods:
        process_constant_or_variable(data: Tuple | Variable) -> Tuple[str, int]:
            Process a constant or a variable, and return the type and address as a tuple.
        check_type_simple(v_type: str) -> bool:
            Check if a type is simple.
        get_type_simple(value: int | float | str | bool) -> str:
            Get the simple type string representation of a value.
        change_to_type(v_type: str, value: str):
            Convert the value to the specified data type.
    """

    @staticmethod
    def process_constant_or_variable(data: Tuple | Variable) -> Tuple[str, int]:
        """
        Process a constant or a variable, and return the type and address as a tuple.

        Parameters:
            data (Tuple | Variable): The data to be processed.

        Returns:
            Tuple[str, int]: A tuple containing the type and address of the data.
        """
        if isinstance(data, Variable):
            return (data.type, data.address)
        elif isinstance(data, tuple):
            return data
        else:
            raise ValueError("Invalid variable format")

    @staticmethod
    def check_type_simple(v_type: str) -> bool:
        """
        Check if a type is simple.

        Parameters:
            v_type (str): The type to be checked.

        Returns:
            bool: True or False depending on if the type is simple (int, float, string, bool).
        """
        simple_types = {"int", "float", "string", "bool"}
        return v_type in simple_types

    @staticmethod
    def get_type_simple(value: int | float | str | bool) -> str:
        """
        Get the simple type string representation of a value.

        Parameters:
            value (int | float | str | bool): The value to get the type from.

        Returns:
            str: The string representation of the type.
        """
        if type(value) == bool or value in ("true", "false"):
            return "bool"
        elif type(value) == int:
            return "int"
        elif type(value) == float:
            return "float"
        elif type(value) == str:
            return "string"
        else:
            raise TypeError("Value type not supported.")

    @staticmethod
    def change_to_type(v_type: str, value: str):
        """
        Convert the value to the specified data type.

        Parameters:
            type (str): The target data type ("int", "float", "string", "bool").
            value (str): The value to be converted.

        Returns:
            The converted value according to the specified data type.
        """
        if v_type == 'int':
            return int(value) if value != 'None' else None
        elif v_type == 'float':
            return float(value) if value != 'None' else None
        elif v_type == 'string':
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