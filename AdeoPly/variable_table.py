class Variable:
    name: str
    type: str
    address: int

    def __init__(self, name: str, type: str, address: int):
        self.name = name
        self.type = type
        self.address = address

    def __str__(self) -> str:
        return f"{self.name},{self.type},{self.address}"

class VariableTable:
    table: dict[str, Variable]
    
    def __init__(self) -> None:
        self.table = {}

    def add_variable(self, name: str, type: str, address: int = 0) -> Variable:
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

    def __str__(self) -> str:
        addresses = [str(value.address) for value in self.table.values()]
        var = "(" + ",".join(addresses) + ")"
        return var

    # DELETE: Print for debugging
    def print(self) -> None:
        variables = self.__str__().split("\n")
        print("\n---- Variable Table ----")
        for value in variables:
            print(f"{value}")