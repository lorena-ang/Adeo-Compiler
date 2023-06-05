from array_manager import ArrayManager
from typing import List, Optional

class Variable:
    """
    The Variable class represents a variable in the program.

    Attributes:
        name (str): The name of the variable.
        type (str): The type of the variable.
        address (int): The memory address of the variable.
        array_manager (Optional[ArrayManager]): The array manager associated with the variable, if it is an array.

    Methods:
        __init__(name: str, type: str, address: int, array_manager: Optional[ArrayManager] = None):
            Initialize a new instance of the Variable class.
        __str__() -> str:
            Return a string representation of the Variable object.
    """

    def __init__(self, name: str, type: str, address: int, array_manager: Optional[ArrayManager] = None):
        self.name = name
        self.type = type
        self.address = address
        self.array_manager = array_manager

    def __str__(self) -> str:
        """
        Return a string representation of the Variable object.

        Returns:
            str: The string representation of the Variable object.
        """
        return f"{self.name}, {self.address}, {self.type}"

class VariableTable:
    """
    The VariableTable class stores the variables in the program.

    Attributes:
        variables (dict): A dictionary of variables with their names as keys.

    Methods:
        __init__():
            Initialize a new instance of the VariableTable class.
        add_variable(v_name: str, v_type: str, address: int = 0, array_manager: Optional[ArrayManager] = None) -> Variable:
            Add a new variable to the table.
        get_variable_from_name(v_name: str) -> Variable:
            Get a variable from the table by name.
        get_attribute_addresses_from_name(o_name: str) -> List[int]:
            Get the memory addresses of variables whose names contain the given substring.
        check_variable_exists(v_name: str) -> bool:
            Check if a variable exists in the table based on its name.
        __str__() -> str:
            Return a string representation of the VariableTable object.
    """
    def __init__(self):
        self.variables = {}

    def add_variable(self, v_name: str, v_type: str, address: int = 0, array_manager: Optional[ArrayManager] = None) -> Variable:
        """
        Add a new variable to the table.

        Parameters:
            v_name (str): The name of the variable.
            v_type (str): The type of the variable.
            address (int): The memory address of the variable - Defaults to 0.
            array_manager (Optional[ArrayManager]): The array associated with the variable - Defaults to None.

        Returns:
            Variable: The Variable object that was added to the table.
        """
        variable = Variable(v_name, v_type, address, array_manager)
        self.variables[v_name] = variable
        return variable

    def get_variable_from_name(self, v_name: str) -> Variable:
        """
        Get a variable from the table by name.

        Parameters:
            v_name (str): The name of the variable.

        Returns:
            Variable: The Variable object corresponding to the given name.
        """
        for variable in self.variables.values():
            if variable.name == v_name:
                return variable
        raise ValueError(f"The variable with the name '{v_name}' does not exist.")

    def get_attribue_addresses_from_name(self, o_name: str) -> List[int]:
        """
        Get the memory addresses of variables whose names contain the given substring. Useful for finding attributes of an object.

        Parameters:
            o_name (str): The object name followed by a '.' (ex. object1.)

        Returns:
            List[int]: A list of memory addresses of the attributes of an object.
        """
        addresses = []
        for variable in self.variables.values():
            if o_name in variable.name:
                addresses.append(variable.address)
        return addresses

    def check_variable_exists(self, v_name: str) -> bool:
        """
        Check if a variable exists in the table based on its name.

        Parameters:
            v_name (str): The name of the variable.

        Returns:
            bool: True or False depending on if the variable exists.
        """
        return v_name in self.variables
    
    def __str__(self) -> str:
        """
        Return a string representation of the VariableTable object.

        Returns:
            str: The string representation of the VariableTable object.
        """
        output = ""
        for variable in self.variables.values():
            output += str(variable) + "\n"
        return output

    def print(self):
        """
        Print the variables in the variable table.
        """
        print("\n--Variable Table--")
        for variable in self.variables.values():
            print(variable)