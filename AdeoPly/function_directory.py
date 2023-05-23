from typing import Tuple
from stack import Context
from variable_table import Variable

class Function:
    def __init__(self, name: str, return_type: str, return_address: int, context: Context, address: int):
        self.name = name
        self.initial_quad_address = 0
        self.resources = (0, 0, 0, 0)  # (ints, floats, bools, strings)
        self.return_type = return_type
        self.return_address = return_address
        self.return_bool = False
        self.address = address
        self.context = context
        self.parameters = []

class FunctionVM:
    def __init__(self, name: str, initial_quad_address: int, resources: Tuple[int, int, int, int]):
        self.name = name
        self.initial_quad_address = initial_quad_address
        self.resources = resources

class FunctionDirectory:
    def __init__(self) -> None:
        self.functions = {}

    # Get the information for a function in the directory
    def get_function_from_directory(self, name: str) -> Function:
        function = self.functions.get(name)
        if function is not None:
            return function
        raise Exception(f"The information for function '{name}' does not exist.")

    # Check if a function exists in the directory
    def check_function_exists(self, name: str) -> bool:
        return name in self.functions

    # Add a funcion to function directory
    def add_function_to_directory(self, name: str, return_type: str, return_address: int, address: int, context: Context) -> Function:
        function = Function(name, return_type, return_address, context, address)
        self.functions[name] = function
        return function
    
    def __str__(self) -> str:
        output = ""
        for key, value in self.functions.items():
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
        for key, value in self.functions.items():
            print(f"Function: {key}")
            print(f"Address: {value.address}")
            print(f"Return type: {value.return_type}")
            print(f"Return address: {value.return_address}")
            print(f"Parameters: {', '.join([param.type for param in value.parameters])}")
            print(f"Start quadruple: {value.initial_quad_address}")
            print(f"Resource: {','.join(str(res) for res in value.resources)}")
            print(value)
        
class FunctionDirectoryVM:
    def __init__(self) -> None:
        self.functions = {}

    # Get the information for a function in the directory
    def get_function_from_directory(self, name: str) -> FunctionVM:
        function = self.functions.get(name)
        if function is not None:
            return function
        raise Exception(f"The information for function '{name}' does not exist.")

    # Check if a function exists in the directory
    def check_function_exists(self, name: str) -> bool:
        return name in self.functions

    # Add a funcion to function directory
    def add_function_to_directory(self, name: str, initial_quad_address: int, resources: Tuple[int, int, int, int]) -> FunctionVM:
        function = FunctionVM(name, initial_quad_address, resources)
        self.functions[name] = function
        return function
    
    def __str__(self) -> str:
        output = ""
        for key, value in self.functions.items():
            output += "\n"
            output += f"{key},"
            output += f"{value.initial_quad_address},"
            output += f"({','.join(str(res) for res in value.resources)})"
        return output