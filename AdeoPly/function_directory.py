from typing import Tuple
from stack import Context

class Function:
    name: str
    initial_quad_address: int
    resources: Tuple[int, int, int, int] # resources = (ints, floats, bools, strings)
    return_type: str
    return_address: int
    return_bool: bool
    address: int
    context: Context
    parameters: list[str] # str = type of var --> ["int", "float", "int"]

    def __init__(self, name: str, return_type: str, return_address: int, context: Context, address: int):
        self.name = name
        self.return_type = return_type
        self.return_address = return_address
        self.return_bool = False
        self.address = address
        self.context = context
        self.parameters = []
        self.resources = (0, 0, 0, 0)

class FunctionDirectory:
    dir: dict[str, Function]
    
    def __init__(self) -> None:
        self.dir = {}

    # Get the information for a function in the directory
    def get_function_from_directory(self, name: str) -> Function:
        if (function := self.dir.get(name)) is not None:
            return function
        else:
            raise Exception(f"The information for function '{name}' does not exist.")

    # Check if a function exists in the directory
    def check_function_exists(self, name: str) -> bool:
        if self.dir.get(name) is None:
            return False
        else:
            return True

    # Add a funcion to function directory
    def add_function_to_directory(self, name: str, return_type: str, return_address: int, address: int, context: Context) -> Function:
        self.dir[name] = Function(name, return_type, return_address, context, address)
        return self.dir[name]

    # DELETE: Print for debugging
    def print(self) -> None:
        print("\n----Function Directory----")
        for key, value in self.dir.items():
            print(f"Function: {key}")
            print(f"Address: {value.address}")
            print(f"Return type: {value.type}")
            print(f"Return address: {value.return_address}")
            print(f"Parameters: {[param for param in value.param_list]}")
            print(f"Start quadruple: {value.start_quad}")
            print(value)