class ArrayDimension:
    def __init__(self, upper_lim: int = 0, R: int = 0, m: int = 0) -> None:
        self.upper_lim = upper_lim
        self.R = R
        self.m = m

    def __str__(self) -> str:
        return f"{self.upper_lim},{self.R},{self.m}"

class ArrayManager:
    def __init__(self) -> None:
        self.dimensions = []
        self.size = 0

    # Add a new dimension by upper limit
    def add_dimension(self, upper_lim: int) -> ArrayDimension:
        if upper_lim > 0:
            if self.dimensions:
                new_R = self.dimensions[-1].R * upper_lim
                self.dimensions.append(ArrayDimension(upper_lim, new_R, 0))
            else:
                self.dimensions.append(ArrayDimension(upper_lim, upper_lim, 0))
            return self.dimensions[-1]
        else:
            raise ValueError("Incorrect dimension.")

    # Update the dimension values
    def update_dimension(self) -> None:
        if len(self.dimensions) >= 1:
            # Set size to R value of last dimension
            self.size = self.dimensions[-1].R
            for i, dim in enumerate(self.dimensions):
                if i == 0:
                    self.dimensions[i].m = self.size // dim.upper_lim
                else:
                    self.dimensions[i].m = self.dimensions[i - 1].m // dim.upper_lim

    def __str__(self) -> str:
        return f"{self.size}, {[str(dim) for dim in self.dimensions]}"