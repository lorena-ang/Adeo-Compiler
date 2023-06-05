from typing import Tuple

class Function:
    """
    The Function class represents a function in the program.
    
    Attributes:
        name (str): The name of the function.
        initial_quad_address (int): The initial quadruple address of the function.
        resources (Tuple[int, int, int, int, int]): The resources required by the function - (ints, floats, bools, strings, ptrs)
        address (int): The address of the function name.
        return_type (str): The return type of the function.
        return_address (int): The address where the return value of the function will be stored.
        return_present (bool): Indicates if the function has a return statement.
        parameters (list): The list of parameters of the function.

    Methods:
        __init__(name: str, address: int, return_type: str, return_address: int):
            Initialize a new instance of the Function class.
    """

    def __init__(self, name: str, address: int, return_type: str, return_address: int):
        self.name = name
        self.initial_quad_address = 0
        self.resources = (0, 0, 0, 0, 0)
        self.address = address
        self.return_type = return_type
        self.return_address = return_address
        self.return_present = False
        self.parameters = []

class FunctionVM:
    """
    The FunctionVM class represents a function in the virtual machine.
    
    Attributes:
        name (str): The name of the function.
        initial_quad_address (int): The initial quadruple address of the function.
        resources (Tuple[int, int, int, int]): The resources required by the function. (ints, floats, bools, strings)

    Methods:
        __init__(name: str, initial_quad_address: int, resources: Tuple[int, int, int, int]):
            Initialize a new instance of the FunctionVM class.
    """

    def __init__(self, name: str, initial_quad_address: int, resources: Tuple[int, int, int, int]):
        self.name = name
        self.initial_quad_address = initial_quad_address
        self.resources = resources

class FunctionDirectory:
    """
    The FunctionDirectory class stores the functions in the program.
    
    Attributes:
        functions (dict): A dictionary of functions with their names as keys.

    Methods:
        __init__():
            Initialize a new instance of the FunctionDirectory class.
        add_function_to_directory(f_name: str, address: int, return_type: str, return_address: int) -> Function:
            Add a function to the function directory.
        get_function_from_directory(f_name: str) -> Function:
            Get the information for a function in the directory.
        check_function_exists(f_name: str) -> bool:
            Check if a function exists in the directory.
        __str__() -> str:
            Get a string representation of the FunctionDirectory object.
        print():
            Print the functions in the function directory.
    """

    def __init__(self):
        self.functions = {}

    def add_function_to_directory(self, f_name: str, address: int, return_type: str, return_address: int) -> Function:
        """
        Add a function to the function directory.

        Parameters:
            f_name (str): The name of the function.
            return_type (str): The return type of the function.
            return_address (int): The address where the return value of the function will be stored.
            address (int): The address of the function name.
            context (Context): The context associated with the function.

        Returns:
            Function: The Function object representing the added function.
        """
        function = Function(f_name, address, return_type, return_address)
        self.functions[f_name] = function
        return function

    def get_function_from_directory(self, f_name: str) -> Function:
        """
        Get the information for a function in the directory.

        Parameters:
            f_name (str): The name of the function to retrieve.

        Returns:
            Function: The Function object representing the function.
        """
        function = self.functions.get(f_name)
        if function is not None:
            return function
        raise Exception(f"The information for function '{f_name}' does not exist.")

    def check_function_exists(self, f_name: str) -> bool:
        """
        Check if a function exists in the directory.

        Parameters:
            f_name (str): The name of the function to check.

        Returns:
            bool: True or False depending on if the function exists in the directory.
        """
        return f_name in self.functions
    
    def __str__(self) -> str:
        """
        Get a string representation of the FunctionDirectory object.

        Returns:
            str: A string representation of the FunctionDirectory object.
        """
        output = ""
        for f_name, function in self.functions.items():
            output += "\n"
            output += f"{f_name},"
            output += f"{function.return_type},"
            output += f"({','.join(str(resources) for resources in function.resources)}),"
            output += f"{function.initial_quad_address}"
        return output

    def print(self):
        """
        Print the functions in the function directory.
        """
        print("\n----Function Directory----")
        for f_name, function in self.functions.items():
            print(f"Function: {f_name}")
            print(f"Address: {function.address}")
            print(f"Return type: {function.return_type}")
            print(f"Return address: {function.return_address}")
            print(f"Parameters: {', '.join([param.type for param in function.parameters])}")
            print(f"Start quadruple: {function.initial_quad_address}")
            print(f"Resource: {','.join(str(resources) for resources in function.resources)}")
        
class FunctionDirectoryVM:
    """
    The FunctionDirectoryVM class stores the functions in the virtual machine.
    
    Attributes:
        functions (dict): A dictionary of functions with their names as keys.

    Methods:
        __init__():
            Initialize a new instance of the FunctionDirectoryVM class.
        add_function_to_directory(f_name: str, initial_quad_address: int, resources: Tuple[int, int, int, int]) -> FunctionVM:
            Add a function to the function directory.
        get_function_from_directory(f_name: str) -> FunctionVM:
            Get the information for a function in the directory.
        check_function_exists(f_name: str) -> bool:
            Check if a function exists in the directory.
        __str__() -> str:
            Get a string representation of the FunctionDirectoryVM object.
    """

    def __init__(self):
        self.functions = {}

    def get_function_from_directory(self, f_name: str) -> FunctionVM:
        """
        Get the information for a function in the directory.

        Parameters:
            f_name (str): The name of the function to retrieve.

        Returns:
            FunctionVM: The FunctionVM object representing the function.
        """
        function = self.functions.get(f_name)
        if function is not None:
            return function
        raise Exception(f"The information for function '{f_name}' does not exist.")

    def check_function_exists(self, f_name: str) -> bool:
        """
        Check if a function exists in the directory.

        Parameters:
            f_name (str): The name of the function to check.

        Returns:
            bool: True or False depending on if the function exists in the directory.
        """
        return f_name in self.functions

    def add_function_to_directory(self, f_name: str, initial_quad_address: int, resources: Tuple[int, int, int, int]) -> FunctionVM:
        """
        Add a function to the function directory.

        Parameters:
            name (str): The name of the function.
            initial_quad_address (int): The initial quadruple address of the function.
            resources (Tuple[int, int, int, int]): The resources required by the function. (ints, floats, bools, strings)

        Returns:
            FunctionVM: The FunctionVM object representing the added function.
        """
        function = FunctionVM(f_name, initial_quad_address, resources)
        self.functions[f_name] = function
        return function
    
    def __str__(self) -> str:
        """
        Get a string representation of the FunctionDirectoryVM object.

        Returns:
            str: A string representation of the FunctionDirectoryVM object.
        """
        output = ""
        for f_name, function in self.functions.items():
            output += "\n"
            output += f"{f_name},"
            output += f"{function.initial_quad_address},"
            output += f"({','.join(str(resources) for resources in function.resources)})"
        return output