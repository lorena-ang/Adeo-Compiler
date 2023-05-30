class Quad:
    def __init__(self, operator: str, left_address: int | None, right_address: int | None, return_address: int):
        self.operator = operator
        self.left_address = left_address
        self.right_address = right_address
        self.return_address = return_address
        
    def __str__(self) -> str:
        return f"({self.operator},{self.left_address},{self.right_address},{self.return_address})"

class Quadruples:
    def __init__(self) -> None:
        self.instr_ptr = 0
        self.quadruples = []

    # Add a new quadruple to list of quadruples
    def add_quad(self, quad: Quad) -> None:
        self.instr_ptr += 1
        self.quadruples.append(quad)
    
    # Get quadruple in an address
    def __getitem__(self, address: int) -> Quad:
        return self.quadruples[address]

    # Set quadruple value in an address
    def __setitem__(self, address: int, quad: Quad) -> None:
        self.quadruples[address] = quad
    
    # Initialize iteration from first instruction
    def __iter__(self):
        self.instr_ptr = 0
        return self

    # Retrieve next quadruple during iteration
    def __next__(self):
        # Check that instruction pointer is valid
        if self.instr_ptr < len(self.quadruples):
            # Retrieve next quadruple
            self.instr_ptr += 1
            return self.quadruples[self.instr_ptr - 1]
        else:
            raise StopIteration
    
    def __str__(self) -> str:
        result = "\n"
        for quad in self.quadruples:
            result += f"{str(quad)}\n"
        return result
    
    # Print quadruples with quadruple number
    def print(self) -> None:
        i = 0
        print("\n--Quadruples--")
        for quad in self.quadruples:
            print(f"{i} {str(quad)}")
            i += 1
        print()