from array_manager import ArrayManager
from typing import Optional

class Variable:
    def __init__(self, name: str, type: str, address: int, array_manager: Optional[ArrayManager] = None):
        self.name = name
        self.type = type
        self.address = address
        self.array_manager = array_manager

    def __str__(self) -> str:
        return f"{self.name},{self.type},{self.address}"

class VariableTable:
    def __init__(self) -> None:
        self.variables = {}

    # Add a new variable to the table
    def add_variable(self, name: str, type: str, address: int = 0, array_manager: Optional[ArrayManager] = None) -> Variable:
        variable = Variable(name, type, address, array_manager)
        self.variables[name] = variable
        return variable

    # Get a variable from an address
    def get_variable_from_address(self, address: int) -> Variable:
        for variable in self.variables.values():
            if variable.address == address:
                return variable
        raise ValueError(f"The variable with the address '{address}' does not exist.")

    # Get a variable from a variable name
    def get_variable_from_name(self, name: str) -> Variable:
        for variable in self.variables.values():
            if variable.name == name:
                return variable
        raise ValueError(f"The variable with the name '{name}' does not exist.")

    # Check if a variable exists from its name
    def check_variable_exists(self, name: str) -> bool:
        return name in self.variables

    def __str__(self) -> str:
        addresses = [str(value.address) for value in self.variables.values()]
        var = "(" + ",".join(addresses) + ")"
        return var

    # DELETE: Print for debugging
    def print(self) -> None:
        print("\n---- Variable Table ----")
        for value in self.variables.values():
            print(value)