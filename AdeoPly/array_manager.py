class Dimension:
    """
    The Dimension class represents a dimension of an array.
    
    Attributes:
        upper_lim (int): The upper limit of the dimension.
        R (int): The R value of the dimension.
        m (int): The m value of the dimension.

    Methods:
        __init__(upper_lim: int = 0, R: int = 0, m: int = 0):
            Initialize a new instance of the Dimension class.
        __str__() -> str:
            Return a string representation of the Dimension object.
    """
    
    def __init__(self, upper_lim: int = 0, R: int = 0, m: int = 0):
        self.upper_lim = upper_lim
        self.R = R
        self.m = m

    def __str__(self) -> str:
        """
        Return a string representation of the Dimension object.

        Returns:
            str: A string representing the Dimension object.
        """
        return f"upper_lim: {self.upper_lim}, R: {self.R}, m: {self.m}"

class ArrayManager:
    """
    The ArrayManager class handles the declaration of arrays and updates their dimensions.
    
    Attributes:
        dimensions (list): The list of dimension nodes for an array.
        size (int): The size of the array.

    Methods:
        __init__():
            Initialize a new instance of the ArrayManager class.
        add_dimension(upper_lim: int) -> Dimension:
            Add a new dimension node to the array.
        update_dimension():
            Update the dimension values in the array.
        __str__() -> str:
            Return a string representation of the ArrayManager object.
    """

    def __init__(self):
        self.dimensions = []
        self.size = 0

    def add_dimension(self, upper_lim: int) -> Dimension:
        """
        Add a new dimension node to the array.

        Parameters:
            upper_lim (int): The upper limit of the new dimension.

        Returns:
            Dimension: The newly added Dimension object.
        """
        if upper_lim > 0:
            if self.dimensions:
                new_R = self.dimensions[-1].R * upper_lim
                self.dimensions.append(Dimension(upper_lim, new_R, 0))
            else:
                self.dimensions.append(Dimension(upper_lim, upper_lim, 0))
            return self.dimensions[-1]
        else:
            raise ValueError("Incorrect dimension.")

    def update_dimension(self):
        """
        Update the dimension values in the array.
        """
        if len(self.dimensions) >= 1:
            # Set size to R value of last dimension
            self.size = self.dimensions[-1].R
            for i, dim in enumerate(self.dimensions):
                if i == 0:
                    self.dimensions[i].m = self.size // dim.upper_lim
                else:
                    self.dimensions[i].m = self.dimensions[i - 1].m // dim.upper_lim

    def __str__(self) -> str:
        """
        Return a string representation of the ArrayManager object.

        Returns:
            str: A string representing the ArrayManager object.
        """
        return f"Size: {self.size} -> {[str(dim) for dim in self.dimensions]}"