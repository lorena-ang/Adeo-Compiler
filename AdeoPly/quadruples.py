class Quad:
    """
    The Quad class represents a quadruple, which consists of an operator and addresses for the left operand, right operand, and return value.
    
    Attributes:
        operator (str): The operator of the quadruple.
        left_address (int | None): The address of the left operand, or None if the field is empty.
        right_address (int | None): The address of the right operand, or None if the field is empty.
        return_address (int): The address of the return value.

    Methods:
        __init__(operator: str, left_address: int | None, right_address: int | None, return_address: int):
            Initialize a new instance of the Quad class.
        __str__() -> str:
            Return a string representation of the quadruple.
    """
    
    def __init__(self, operator: str, left_address: int | None, right_address: int | None, return_address: int):
        self.operator = operator
        self.left_address = left_address
        self.right_address = right_address
        self.return_address = return_address
        
    def __str__(self) -> str:
        """
        Return a string representation of the quadruple.

        Returns:
            str: The string representation of the quadruple.
        """
        return f"({self.operator},{self.left_address},{self.right_address},{self.return_address})"

class Quadruples:
    """
    The Quadruples class represents a list of quadruples.
    
    Attributes:
        instr_ptr (int): The current instruction pointer.
        quadruples (list): The list of quadruples.

    Methods:
        __init__():
            Initialize a new instance of the Quadruples class.
        add_quad(operator: str, left_address: int | None, right_address: int | None, result_address: int | None):
            Adds a new quadruple to the quadruples list and updates the instruction pointer.
        __getitem__(instr: int) -> Quad:
            Get the quadruple at the specified instruction number.
        __setitem__(instr: int, quad: Quad):
            Set the quadruple at the specified instruction number.
        __iter__() -> Quadruples:
            Initialize the iteration from the first instruction.
        __next__() -> Quad:
            Retrieve the next quadruple during iteration and update the instruction pointer.
        __str__() -> str:
            Return a string representation of the quadruples list.
        print():
            Print the quadruples with the instruction number.
    """
    
    def __init__(self):
        self.instr_ptr = 0
        self.quadruples = []
        
    def add_quad(self, operator: str, left_address: int | None, right_address: int | None, result_address: int | None):
        """
        Adds a new quadruple to the quadruples list and update the instruction pointer.

        Parameters:
            operator (str): The operator for the quadruple.
            left_address (int | None): The address of the left operand, or None if the field should be empty.
            right_address (int | None): The address of the right operand, or None if the field should be empty.
            result_address (int | None): The address of the result operand, or None if the field should be empty.
        """
        self.instr_ptr += 1
        quad = Quad(operator, left_address, right_address, result_address)
        self.quadruples.append(quad)
    
    def __getitem__(self, instr: int) -> Quad:
        """
        Get the quadruple at the specified instruction number.

        Parameters:
            instr (int): The instruction number of the quadruple.

        Returns:
            Quad: The quadruple at the specified instruction number.
        """
        return self.quadruples[instr]

    def __setitem__(self, instr: int, quad: Quad):
        """
        Set the quadruple at the specified instruction number.

        Parameters:
            instr (int): The instruction number of the quadruple.
            quad (Quad): The new quadruple.
        """
        self.quadruples[instr] = quad
    
    def __iter__(self):
        """
        Initialize the iteration from the first instruction.

        Returns:
            Quadruples: The Quadruples object itself.
        """
        self.instr_ptr = 0
        return self

    def __next__(self) -> Quad:
        """
        Retrieve the next quadruple during iteration and update the instruction pointer.

        Returns:
            Quad: The next quadruple.
        """
        # Check that instruction pointer is valid
        if self.instr_ptr < len(self.quadruples):
            # Retrieve next quadruple
            self.instr_ptr += 1
            return self.quadruples[self.instr_ptr - 1]
        else:
            raise StopIteration
    
    def __str__(self) -> str:
        """
        Return a string representation of the quadruples list.

        Returns:
            str: The string representation of the quadruples list.
        """
        output = "\n"
        for quad in self.quadruples:
            output += f"{str(quad)}\n"
        return output
    
    def print(self):
        """
        Print the quadruples with the instruction number.
        """
        i = 0
        print("\n--Quadruples--")
        for quad in self.quadruples:
            print(f"{i} {str(quad)}")
            i += 1
        print()