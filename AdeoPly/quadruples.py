class Quad:
    operator: str
    left_address: int
    right_address: int | None
    return_address: int | None

    def __init__(self, operator: str, left_address: int, right_address: int | None, return_address: int | None):
        self.operator = operator
        self.left_address = left_address
        self.right_address = right_address
        self.return_address = return_address
        
    def __str__(self) -> str:
        return f"({self.operator}, {self.left_address}, {self.right_address}, {self.return_address})"

class Quadruples:
    instr_ptr: int
    quadruples: list[Quad]

    def __init__(self) -> None:
        self.instr_ptr = 0
        self.quadruples = []

    # Add a new quadruple to list of quadruples
    def add_quad(self, quad: Quad) -> None:
        self.instr_ptr += 1
        self.quadruples.append(quad)

    # Get quadruple from an address by searching through memory
    def get_quad_from_address(self, address: int) -> Quad:
        return self.quadruples[address]
    
    # Get quadruple in an address
    def __getitem__(self, address: int) -> Quad:
        return self.quadruples[address]

    # Set quadruple value in an address
    def __setitem__(self, address: int, quad: Quad) -> None:
        self.quadruples[address] = quad

    # DELETE: Print for debugging
    def print(self) -> None:
        print("\nQuadruples")
        i = 0
        for quad in self.quadruples:
            print(str(i) + " " + str(quad))
            i += 1