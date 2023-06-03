class SemanticCube:
    """
    The SemanticCube class represents a semantic cube, which is used to determine the result type of operations based on the types of their operands.

    Attributes:
        semantic_cube (dict): A dictionary that stores the result types of operations based on their operands' types.

    Methods:
        change_to_number(value: str) -> int:
            Convert a type string to its corresponding number representation.
        change_to_string(value: int) -> str:
            Convert a number representation to its corresponding type string.
        get_result_type(left: str, operation: str, right: str) -> str:
            Get the result type of an operation.
        check_operation(left: str, operation: str, right: str) -> bool:
            Check if an operation is valid.
    """
    
    semantic_cube = {
        0: {
            "+": {0: 0, 1: 1},
            "-": {0: 0, 1: 1},
            "/": {0: 0, 1: 1},
            "*": {0: 0, 1: 1},
            ">": {0: 3},
            ">=": {0: 3},
            "<": {0: 3},
            "<=": {0: 3},
            "==": {0: 3},
            "!=": {0: 3},
            "=": {0: 0},
        },
        1: {
            "+": {0: 1, 1: 1},
            "-": {0: 1, 1: 1},
            "/": {0: 1, 1: 1},
            "*": {0: 1, 1: 1},
            "<": {1: 3},
            ">": {1: 3},
            "<=": {1: 3},
            ">=": {1: 3},
            "!=": {1: 3},
            "==": {1: 3},
            "=": {0: 1, 1: 1},
        },
        2: {
            "+": {2: 2},
            "!=": {2: 3},
            "==": {2: 3},
            "=": {2: 2},
        },
        3: {
            "!=": {3: 2},
            "==": {3: 3},
            "&&": {3: 3},
            "||": {3: 3},
            "=": {3: 3},
        },
    }

    @staticmethod
    def change_to_number(value: str) -> int:
        """
        Convert a type string to its corresponding number representation.

        Parameters:
            value (str): The type string to be converted.

        Returns:
            int: The number representation of the type string.
        """
        types = {"int": 0, "float": 1, "string": 2, "bool": 3}
        return types[value]

    @staticmethod
    def change_to_string(value: int) -> str:
        """
        Convert a number representation to its corresponding type string.

        Parameters:
            value (int): The number representation of the type string.

        Returns:
            str: The type string.
        """
        types = {0: "int", 1: "float", 2: "string", 3: "bool"}
        return types[value]

    @staticmethod
    def get_result_type(left: str, operation: str, right: str) -> str:
        """
        Get the result type of an operation.

        Parameters:
            left (str): The type of the left operand.
            operation (str): The operator of the operation.
            right (str): The type of the right operand.

        Returns:
            str: The result type of the operation.
        """
        try:
            result = SemanticCube.semantic_cube[SemanticCube.change_to_number(left)][operation][SemanticCube.change_to_number(right)]
            return SemanticCube.change_to_string(result)
        except KeyError:
            if left == right:
                return left
            else:
                return "TypeMismatch"

    @staticmethod
    def check_operation(left: str, operation: str, right: str) -> bool:
        """
        Check if an operation is valid.

        Parameters:
            left (str): The type of the left operand.
            operation (str): The operator of the operation.
            right (str): The type of the right operand.

        Returns:
            bool: True or False depending on if the operation is valid, False otherwise.
        """
        return SemanticCube.get_result_type(left, operation, right) is None