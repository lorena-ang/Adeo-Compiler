from typing import Tuple

class Variable:
    name: str
    type: str
    address: int

    def __init__(self, name: str, type: str, address: int):
        self.name = name
        self.type = type
        self.address = address
        
    # Returns a tuple with only the type and address - needed for assignments and expr_operations
    def process_variable(self) -> Tuple[str, int]:
        return (self.type, self.address)
    
    # DELETE: Print for debugging
    def __str__(self) -> str:
        return f"name = {self.name}, type = {self.type}, address = {self.address}"

class VariableTable:
    table: dict[str, Variable]
    
    def __init__(self) -> None:
        self.table = {}

    def add_variable(self, name: str, type: str, address: int = 0) -> Variable:
        if name in self.table:
            raise Exception(f"A variable with the name '{name}' already exists in the variable table.")
        self.table[name] = Variable(name, type, address)
        return self.table[name]

    # Get a variable from an address
    def get_variable_from_address(self, address: int) -> Variable:
        for var in self.table.values():
            if var.address == address:
                return var
        raise Exception(f"The variable with the address '{address}' does not exist.")

    # Get a variable from a name
    def get_variable_from_name(self, name: str) -> Variable:
        for var in self.table.values():
            if var.name == name:
                return var
        raise Exception(f"The variable with the name '{name}' does not exist.")

    # Check if a variable exists from its name
    def check_variable_exists(self, name: str) -> bool:
        return name in self.table

    # DELETE: Print for debugging
    def __str__(self) -> str:
        var = "\n---- Variable Table ----\n"
        for key, value in self.table.items():
            var += f"{value}\n"
        return var

    # DELETE: Print for debugging
    def print(self) -> None:
        variables = self.__str__().split("\n")
        print("\n---- Variable Table ----")
        for value in variables:
            print(f"{value}")