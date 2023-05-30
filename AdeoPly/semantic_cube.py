class SemanticCube:
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
            "=": {1: 1},
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
        types = {"int": 0, "float": 1, "string": 2, "bool": 3}
        return types[value]

    @staticmethod
    def change_to_string(value: int) -> str:
        types = {0: "int", 1: "float", 2: "string", 3: "bool"}
        return types[value]

    # Get the result type of an operation
    def get_result_type(self, left: str, operation: str, right: str) -> str:
        try:
            result = self.semantic_cube[self.change_to_number(left)][operation][self.change_to_number(right)]
            return self.change_to_string(result)
        except KeyError:
            if left == right:
                return left
            else:
                return "TypeMismatch"

    # Check if an operation is valid
    def check_operation(self, left: str, operation: str, right: str) -> bool:
        return self.get_result_type(left, operation, right) is None