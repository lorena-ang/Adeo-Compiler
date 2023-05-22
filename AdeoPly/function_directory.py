from typing import Tuple
from stack import Context
from variable_table import Variable

class Function:
    name: str
    initial_quad_address: int
    resources: Tuple[int, int, int, int] # resources = (ints, floats, bools, strings)
    return_type: str
    return_address: int
    return_bool: bool
    address: int
    context: Context
    parameters: list[Variable] 

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
    
    def __str__(self) -> str:
        output = ""
        for key, value in self.dir.items():
            output += "\n"
            output += f"{key},"
            output += f"{value.return_type},"
            output += f"({','.join(str(res) for res in value.resources)}),"
            output += f"[{','.join([param.type for param in value.parameters])}],"
            output += f"{value.address},"
            output += f"{value.initial_quad_address},"
            output += f"{value.return_address}"
        return output

    # DELETE: Print for debugging
    def print(self) -> None:
        print("\n----Function Directory----")
        for key, value in self.dir.items():
            print(f"Function: {key}")
            print(f"Address: {value.address}")
            print(f"Return type: {value.return_type}")
            print(f"Return address: {value.return_address}")
            print(f"Parameters: {', '.join([param.type for param in value.parameters])}")
            print(f"Start quadruple: {value.initial_quad_address}")
            print(f"Resource: {','.join(str(res) for res in value.resources)}")
            print(value)
            
class FunctionVM:
    name: str
    initial_quad_address: int
    resources: Tuple[int, int, int, int] # resources = (ints, floats, bools, strings)

    def __init__(self, name: str, initial_quad_address: int, resources: Tuple[int, int, int, int]):
        self.name = name
        self.initial_quad_address = initial_quad_address
        self.resources = resources
        
class FunctionDirectoryVM:
    dir: dict[str, FunctionVM]
    
    def __init__(self) -> None:
        self.dir = {}

    # Get the information for a function in the directory
    def get_function_from_directory(self, name: str) -> FunctionVM:
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
    def add_function_to_directory(self, name: str, initial_quad_address: int, resources: Tuple[int, int, int, int]) -> FunctionVM:
        self.dir[name] = FunctionVM(name, initial_quad_address, resources)
        return self.dir[name]
    
    def __str__(self) -> str:
        output = ""
        for key, value in self.dir.items():
            output += "\n"
            output += f"{key},"
            output += f"{value.initial_quad_address},"
            output += f"({','.join(str(res) for res in value.resources)})"
        return output