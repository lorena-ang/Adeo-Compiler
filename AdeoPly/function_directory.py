from typing import Tuple

class Function():
    name: str
    type: str
    scope: str
    address: int
    parameters: list[Tuple[str, int, str]]
    has_return: bool
    return_address: int
    start_quad: int

    def __init__(
        self,
        name: str,
        type: str,
        scope: str,
        address: int,
        return_address: int = 0,
    ):
        self.name = name
        self.type = type
        self.scope = scope
        self.address = address
        self.parameters = []
        self.has_return = False
        self.return_address = return_address

    # DELETE: Print for debugging
    def __str__(self) -> str:
        return f"{self.name},{self.start_quad},{self.__resources_str()}"

    # DELETE: Print for debugging
    def __str__(self) -> str:
        """
        Stringify the resources' information for operations.
        """
        return super().__str__()

class FunctionDirectory():
    dir: dict[str, Function]
    def __init__(self) -> None:
        self.dir = {}

    def add(
        self,
        name: str,
        scope: str,
        address: int,
        return_type: str,
        return_address: int,
    ) -> Function:
        if self.contains(name):
            raise Exception(f"A function with the name '{name}' already exists in the function directory.")
        else:
            self.dir[name] = Function(
                name,
                scope,
                address,
                return_type,
                return_address,
            )
            return self.dir[name]
        
    def get(self, name: str) -> Function:
        if (func := self.get(name)) is not None:
            return func
        else:
            raise Exception(f"The information for function '{name}' does not exist.")

    def contains(self, name: str) -> bool:
        if self.get(name) is None:
            return False
        else:
            return True

    # DELETE: Print for debugging
    def print(self) -> None:
        for key, value in self.dir.items():
            print(f"# Function: {key}")
            print(f"# Address: {value.address}")
            print(f"# Return type: {value.type}")
            print(f"# Return address: {value.return_address}")
            print(f"# Parameters: {[param for param in value.param_list]}")
            print(f"# Start quadruple: {value.start_quad}")
        print(value)