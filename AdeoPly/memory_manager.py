from typing import TypeVar, Generic

TV = TypeVar("TV")
SIZE = 1000

class TypeSpace(Generic[TV]):
    initial_address: int
    values: list[TV]
    
    def __init__(self, start: int) -> None:
        self.initial_address = start
        self.values = []

class MemoryManager:
    ints_space: TypeSpace[int]
    floats_space: TypeSpace[float]
    strings_space: TypeSpace[str]
    bools_space: TypeSpace[bool]

    def __init__(self, base_address: int) -> None:
        self.ints_space = TypeSpace(base_address)
        self.floats_space = TypeSpace(base_address  + SIZE)
        self.strings_space = TypeSpace(base_address + SIZE * 2)
        self.bools_space = TypeSpace(base_address + SIZE * 3)

    # From a memory index you will get the type space with initial address and all variables stored
    def get_typespace_from_address(self, address: int) -> TypeSpace:
        if address < self.floats_space.initial_address:
            return self.ints_space
        elif address < self.strings_space.initial_address:
            return self.floats_space
        elif address < self.bools_space.initial_address:
            return self.strings_space
        else:
            return self.bools_space

    # From a value you will get the type space with initial address and all variables stored
    def get_typespace_from_value(self, value: int | float | str | bool) -> TypeSpace:
        if type(value) == bool or value == "true" or value == "false":
            return self.bools_space
        elif type(value) == int:
            return self.ints_space
        elif type(value) == float:
            return self.floats_space
        elif type(value) == str:
            return self.strings_space
        else:
            raise TypeError("Value doesn't exist.")
        
    # From the type of a value you will get the type space with initial address and all variables stored
    def get_typespace_from_type(self, type: str) -> TypeSpace:
        if type == 'int':
            return self.ints_space
        elif type == 'float':
            return self.floats_space
        elif type == 'string':
            return self.strings_space
        elif type == 'bool':
            return self.bools_space
        else:
            raise TypeError("Type doesn't exist.")

    # From an address you will get the value of the item
    def get_value_from_address(self, address: int) -> int | float | str | bool:
        buffer = self.get_typespace_from_address(address)
        return buffer.values[address - buffer.initial_address]

    # Adds a new value to the typespace
    def add_value_to_typespace(self, typespace: TypeSpace, value: int | None) -> int:
        if len(typespace.values) > SIZE:
            raise Exception("Maximum space for this type was exceeded.")
        typespace.values.append(value)
        return typespace.initial_address + len(typespace.values) - 1

    # Adds a new value depending on the type
    def add_value_to_memory(self, value: int | float | str | bool) -> int:
        typespace = self.get_typespace_from_value(value)
        return self.add_value_to_typespace(typespace, value)

    # Find memory address from a value
    def find_address(self, value: int | float | str | bool) -> int | None:
        typespace = self.get_typespace_from_value(value)
        try:
            return typespace.values.index(value) + typespace.initial_address
        except ValueError:
            return None

    # Reserves space for a variable that hasn't been assigned yet (only declared)
    def reserve_space(self, data_type: str) -> int:
        typespace = self.get_typespace_from_type(data_type)
        return self.add_value_to_typespace(typespace, None)

    def clear_memory_values(self) -> None:
        self.ints_space.values.clear()
        self.floats_space.values.clear()
        self.strings_space.values.clear()
        self.bools_space.values.clear()
    
    # DELETE: Print for debugging
    def __str__(self) -> str:
        output = "\n---- Memory Manager ----"
        output += "\nints"
        for addr, val in enumerate(self.ints_space.values):
            output += f"\n{addr + self.ints_space.initial_address}\t{val}"
        output += "\nfloats"
        for addr, val in enumerate(self.floats_space.values):
            output += f"\n{addr + self.floats_space.initial_address}\t{val}"
        output += "\nstrings"
        for addr, val in enumerate(self.strings_space.values):
            output += f"\n{addr + self.strings_space.initial_address}\t{val}"
        output += "\nbools"
        for addr, val in enumerate(self.bools_space.values):
            output += f"\n{addr + self.bools_space.initial_address}\t{val}"
        return output
    
    # DELETE: Print for debugging
    def print(self, scope: str):
        print("\n----" + scope + " Memory Manager----")
        print("ints")
        for addr, val in enumerate(self.ints_space.values):
            print(f"{addr + self.ints_space.initial_address}\t{val}")
        print("floats")
        for addr, val in enumerate(self.floats_space.values):
            print(f"{addr + self.floats_space.initial_address}\t{val}")
        print("strings")
        for addr, val in enumerate(self.strings_space.values):
            print(f"{addr + self.strings_space.initial_address}\t{val}")
        print("bools")
        for addr, val in enumerate(self.bools_space.values):
            print(f"{addr + self.bools_space.initial_address}\t{val}")