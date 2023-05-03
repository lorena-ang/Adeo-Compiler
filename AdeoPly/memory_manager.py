from typing import TypeVar, Generic, Optional

TV = TypeVar("TV")

class TypeSpace(Generic[TV]):
    initial_address: int
    values: list[TV]
    
    def __init__(
        self, start: int
    ) -> None:
        self.initial_address = start
        #self.values = [None for _ in range(1000)]
        self.values = []

class MemoryManager:
    ints: TypeSpace[int]
    floats: TypeSpace[float]
    strings: TypeSpace[str]
    bools: TypeSpace[bool]

    def __init__(self, base_address: int) -> None:
        size = 1000
        self.ints = TypeSpace(base_address)
        self.floats = TypeSpace(base_address  + size)
        self.strings = TypeSpace(base_address + size * 2)
        self.bools = TypeSpace(base_address + size * 3)

    # From a memory index you will get the type space with initial addr and all variables stored
    def get_typespace_from_address(self, address: int) -> TypeSpace:
        if address < self.floats.initial_address:
            return self.ints
        elif address < self.strings.initial_address:
            return self.floats
        elif address < self.bools.initial_address:
            return self.strings
        else:
            return self.bools

    # From a value you will get the typespace with initial address and all variables stored
    def get_typespace_from_value(self, value: int | float | str | bool) -> TypeSpace:
        if isinstance(value, int):
            return self.ints
        elif isinstance(value, float):
            return self.floats
        elif isinstance(value, str):
            return self.strings
        elif isinstance(value, bool):
            return self.bools
        else:
            raise TypeError("Value doesn't exist.")
        
    def get_typespace_from_type(self, t: str) -> TypeSpace:
        if t == 'int':
            return self.ints
        elif t == 'float':
            return self.floats
        elif t == 'string':
            return self.strings
        elif t == 'bool':
            return self.bools
        else:
            raise TypeError("Type doesn't exist.")

    # From an address it gives you the value of the item
    def get_value_from_address(self, address: int) -> int | float | str | bool:
        buffer = self.get_typespace_from_address(address)
        return buffer.values[address - buffer.initial_address]

    # Updates a variable using its address and giving it a new value
    def set_value(self, address: int, value: int) -> None:
        buffer = self.get_typespace_from_address(address)
        address -= buffer.initial_address
        buffer.values[address] = value

    # Adds a new variable to the typespace
    def append_to_typespace(self, tv: TypeSpace, value: int | None) -> int:
        tv.values.append(value)
        tv_len = len(tv.values) - 1
        if tv_len > 1000:
            raise Exception("Maximum space for this type was exceeded.")
        else:
            return tv_len + tv.initial_address

    # Adds a new variable depending on the type
    def append(self, value: int | float | str | bool) -> int:
        buffer = self.get_typespace_from_value(value)
        return self.append_to_typespace(buffer, value)

    # Reserves space for a variable that hasn't been assigned yet (only declared)
    def reserve(self, type: str) -> int:
        buffer = self.get_typespace_from_type(type)
        return self.append_to_typespace(buffer, None)

    # Find memory address from a value
    def find(self, value: int | float | str | bool) -> int:
        buffer = self.get_typespace_from_value(value)
        try:
            return buffer.values.index(value) + buffer.initial_address
        except ValueError:
            print("Value " + str(value) + " was not found, so it was added.")

    def clear(self) -> None:
        self.ints.values.clear()
        self.floats.values.clear()
        self.strings.values.clear()
        self.bools.values.clear()

    # DELETE: Print for debugging
    def print(self):
        print("ints")
        for index, item in enumerate(self.ints.values):
            print(f"{index + self.ints.initial_address}\t{item}")
        print("floats")
        for index, item in enumerate(self.floats.values):
            print(f"{index + self.floats.initial_address}\t{item}")
        print("strings")
        for index, item in enumerate(self.strings.values):
            print(f"{index + self.strings.initial_address}\t{item}")
        print("bools")
        for index, item in enumerate(self.bools.values):
            print(f"{index + self.bools.initial_address}\t{item}")