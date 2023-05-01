class SemanticCube:
    semantic_cube: dict[str, dict[str, dict[str, str]]]

    def __init__(self):
        self.semantic_cube = {
            "int": {
                "+": {
                    "int": "int",
                    "float": "float",
                },
                "-": {
                    "int": "int",
                    "float": "float",
                },
                "/": {
                    "int": "int",
                    "float": "float",
                },
                "*": {
                    "int": "int",
                    "float": "float",
                },
                ">": {
                    "int": "bool",
                },
                ">=": {
                    "int": "bool",
                },
                "<": {
                    "int": "bool",
                },
                "<=": {
                    "int": "bool",
                },
                "==": {
                    "int": "bool",
                },
                "!=": {
                    "int": "bool",
                },
                "=": {
                    "int": "int",
                },
            },
            "float": {
                "+": {
                    "int": "float",
                    "float": "float",
                },
                "-": {
                    "int": "float",
                    "float": "float",
                },
                "/": {
                    "int": "float",
                    "float": "float",
                },
                "*": {
                    "int": "float",
                    "float": "float",
                },
                "<": {
                    "float": "bool",
                },
                ">": {
                    "float": "bool",
                },
                "<=": {
                    "float": "bool",
                },
                ">=": {
                    "float": "bool",
                },
                "!=": {
                    "float": "bool",
                },
                "==": {
                    "float": "bool",
                },
                "=": {
                    "float": "float",
                },
            },
            "string": {
                "+": {"string": "string"},
                "!=": {"string": "bool"},
                "==": {"string": "bool"},
                "=": {"string": "string"},
            },
            "bool": {
                "!=": {"bool": "string"},
                "==": {"bool": "bool"},
                "&&": {"bool": "bool"},
                "||": {"bool": "bool"},
                "=": {"bool": "bool"},
            },
        }

    def get_type(self, left: str, oper: str, right: str) -> str:
        try:
            result = self.semantic_cube[left][oper][right]
        except KeyError as e:
            raise TypeError("Type mismatch error: Operand doesn't match data type.") from None
        return result