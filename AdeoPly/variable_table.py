class Variable:
    name: str
    type: str
    address: int

    def __init__(
        self,
        name: str,
        type: str,
        scope: str,
        address: int,
    ):
        self.name = name
        self.type = type
        self.scope = scope
        self.address = address

class VariableTable:
    dir: dict[str, Variable]
    def __init__(self) -> None:
        self.dir = {}

    def add(
        self,
        name: str,
        type: str,
        address: int = 0,
    ) -> Variable:
        if name in self.dir:
            raise Exception(f"A variable with the name '{name}' already exists in variable table.")
        else:
            self.dir[name] = Variable(name, type, address)
        return self.dir[name]

    def get_variable(self, address: int) -> Variable:
        for var in self.dir.values():
            if var.address == address:
                return var
        raise Exception(f"The variable with the address '{address}' does not exist.")

    # DELETE: Print for debugging
    def __str__(self) -> str:
        var_info = ""
        for key, value in self.dir.items():
            var_info += f"<var_name:{key},var_atr:{value}>\n"
        return var_info

    # DELETE: Print for debugging
    def print(self, table_name: str) -> None:
        print(f"# {table_name}")
        var_list = self.__str__().split("\n")
        for val in var_list:
            print(f"# {val}")