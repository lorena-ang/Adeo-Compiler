from typing import Tuple
from variable_table import Variable

class DataProcessor:

    def process_data(self, data) -> Tuple[str, int]:
            if isinstance(data, Variable):
                return (data.type, data.address)
            elif isinstance(data, tuple):
                return data
            else:
                raise ValueError("Invalid variable format")