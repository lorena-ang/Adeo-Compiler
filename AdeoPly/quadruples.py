class Quad:
    operator: str
    left_address: int
    right_address: int | None
    return_address: int | None

    def __init__(
        self,
        operator: str,
        left_address: int,
        right_address: int | None,
        return_address: int | None
    ):
        self.operator = operator
        self.left_address = left_address
        self.right_address = right_address
        self.return_address = return_address

    # DELETE: Print for debugging
    def __str__(self) -> str:
        return f"<operator:{self.operator},left_address:{self.left_address},right_address:{self.right_address},return_address:{self.return_address}>"

class Quadruples:
    quadruples: list[Quad]
    instr_ptr: int

    def __init__(self) -> None:
        self.instr_ptr = 0
        self.quadruples = []

    def add(self, quad: Quad) -> None:
        self.quadruples.append(quad)
        self.instr_ptr = self.instr_ptr + 1

    def get(self, index: int) -> Quad:
        return self.quadruples[index]

    def fill(self, index: int, quad: Quad) -> None:
        self.quadruples[index] = quad

    def print(self) -> None:
        for quad in self.quadruples:
            print(quad)