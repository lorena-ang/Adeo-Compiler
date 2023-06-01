from data_helper import DataHelper
from typing import Generic, Optional, Tuple, TypeVar

T = TypeVar("T")
SIZE = 1000

class TypeSpace(Generic[T]):
    """
    The TypeSpace class represents a space for values of a specific type.

    Attributes:
        initial_address (int): The starting memory address of the type space.
        values (List[T | None]): A list to store the values in the type space.
    
    Methods:
        __init__(self, initial_address: int, resource_size: Optional[int] = None):
            Initialize a TypeSpace object.
    """

    def __init__(self, initial_address: int, resource_size: Optional[int] = None):
        self.initial_address = initial_address
        if resource_size is None:
            self.values = []
        else:
            self.values = [None for _ in range(resource_size)]

class MemoryManager:
    """
    The MemoryManager class manages memory allocation for different types of variables.

    Attributes:
        ints_space (TypeSpace[int | None]): The TypeSpace for integers.
        floats_space (TypeSpace[float | None]): The TypeSpace for floats.
        strings_space (TypeSpace[str | None]): The TypeSpace for strings.
        bools_space (TypeSpace[bool | None]): The TypeSpace for booleans.
        ptrs_space (TypeSpace[int | None]): The TypeSpace for pointers.
    
    Methods:
        __init__(self, start_address: int, resources: Optional[Tuple[int, int, int, int, int]] = None):
            Initialize a MemoryManager object.
        add_value_to_typespace(self, typespace: TypeSpace, value: int | None) -> int:
            Adds a new value to the type space.
        add_ptr(self, address: int, value: int):
            Add a new pointer to the pointer type space.
        reserve_space(self, v_type: str, size: int = 1) -> int:
            Reserves space for a variable that hasn't been assigned yet, only declared.
        get_typespace_from_address(self, address: int) -> TypeSpace:
            Get the TypeSpace object corresponding to a memory address.
        get_typespace_from_type(self, v_type: str) -> TypeSpace:
            Get the TypeSpace object corresponding to a variable type.
        get_type_from_address(self, address: int) -> str:
            Get the type of a variable based on its memory address.
        find_memory_address(self, value: int | float | str | bool) -> int:
            Find the memory address of a value in the memory manager or add it to memory.
        get_resources(self) -> Tuple[int, int, int, int, int]:
            Get the number of resources (values) per type.
        clear_memory_values(self):
            Clear the values stored in the type spaces of the memory manager.
        __getitem__(self, address: int) -> int | float | str | bool | None:
            Get the value at a memory address.
        __setitem__(self, address: int, value: int):
            Set the value at a memory address.
        __str__(self) -> str:
            Return a string representation of the MemoryManager object.
        print(self, scope: str):
            Print the memory manager's contents.
    """

    ints_space: TypeSpace[int | None]
    floats_space: TypeSpace[float | None]
    strings_space: TypeSpace[str | None]
    bools_space: TypeSpace[bool | None]
    ptrs_space: TypeSpace[int | None]

    def __init__(self, start_address: int, resources: Optional[Tuple[int, int, int, int, int]] = None):
        if resources is None:
            self.ints_space = TypeSpace(start_address)
            self.floats_space = TypeSpace(start_address  + SIZE)
            self.strings_space = TypeSpace(start_address + SIZE * 2)
            self.bools_space = TypeSpace(start_address + SIZE * 3)
            self.ptrs_space = TypeSpace(start_address + SIZE * 4)
        else:
            self.ints_space = TypeSpace(start_address, resources[0])
            self.floats_space = TypeSpace(start_address  + SIZE, resources[1])
            self.strings_space = TypeSpace(start_address + SIZE * 2, resources[2])
            self.bools_space = TypeSpace(start_address + SIZE * 3, resources[3])
            self.ptrs_space = TypeSpace(start_address + SIZE * 4, resources[4])
    
    def add_value_to_typespace(self, typespace: TypeSpace, value: int | None) -> int:
        """
        Adds a new value to the type space.

        Parameters:
            typespace (TypeSpace): The TypeSpace object to add the value to.
            value (int | None): The value to add.

        Returns:
            int: The memory address where the value was added.
        """
        if len(typespace.values) >= SIZE:
            raise Exception("Maximum space for this type was exceeded.")
        typespace.values.append(value)
        return typespace.initial_address + len(typespace.values) - 1
    
    def add_ptr(self, address: int, value: int):
        """
        Add a new pointer to the pointer type space.

        Parameters:
            address (int): The memory address where the pointer will be stored.
            value (int): The value of the pointer.
        """
        typespace = self.ptrs_space
        typespace.values[address - typespace.initial_address] = value
    
    def reserve_space(self, v_type: str, size: int = 1) -> int:
        """
        Reserves space for a variable that hasn't been assigned yet, only declared.

        Parameters:
            v_type (str): The type of the variable.
            size (int): The size of the variable - Defaults to 1.

        Returns:
            int: The memory address of the reserved space.
        """
        typespace = self.get_typespace_from_type(v_type)
        address = self.add_value_to_typespace(typespace, None)
        for _ in range(size - 1):
            self.add_value_to_typespace(typespace, None)
        return address

    def get_typespace_from_address(self, address: int) -> TypeSpace:
        """
        Get the TypeSpace object corresponding to a memory address.

        Parameters:
            address (int): The memory address of the variable.

        Returns:
            TypeSpace: The TypeSpace object corresponding to the memory address.
        """
        if address < self.floats_space.initial_address:
            return self.ints_space
        elif address < self.strings_space.initial_address:
            return self.floats_space
        elif address < self.bools_space.initial_address:
            return self.strings_space
        elif address < self.ptrs_space.initial_address:
            return self.bools_space
        else:
            return self.ptrs_space
        
    def get_typespace_from_type(self, v_type: str) -> TypeSpace:
        """
        Get the TypeSpace object corresponding to a variable type.

        Parameters:
            v_type (str): The type of the variable.

        Returns:
            TypeSpace: The TypeSpace object corresponding to the variable type.
        """
        if v_type == 'int':
            return self.ints_space
        elif v_type == 'float':
            return self.floats_space
        elif v_type == 'string':
            return self.strings_space
        elif v_type == 'bool':
            return self.bools_space
        elif v_type == 'ptr':
            return self.ptrs_space
        else:
            raise TypeError("Type doesn't exist.")
    
    def get_type_from_address(self, address: int) -> str:
        """
        Get the type of a variable based on its memory address.

        Parameters:
            address (int): The memory address of the variable.

        Returns:
            str: The type of the variable.
        """
        if address < self.floats_space.initial_address:
            return "int"
        elif address < self.strings_space.initial_address:
            return "float"
        elif address < self.bools_space.initial_address:
            return "string"
        elif address < self.ptrs_space.initial_address:
            return "bool"
        else:
            return "ptr"

    def find_memory_address(self, value: int | float | str | bool) -> int:
        """
        Find the memory address of a value in the memory manager or add it to memory.

        Parameters:
            value (int | float | str | bool): The value to find or add.

        Returns:
            int: The memory address of the value.

        Notes:
            - The value is added to the appropriate type space based on its type.
        """
        type = DataHelper.get_type_simple(value)
        typespace = self.get_typespace_from_type(type)
        try:
            return typespace.values.index(value) + typespace.initial_address
        except ValueError:
            address = self.add_value_to_typespace(typespace, value)
            return address

    def get_resources(self) -> Tuple[int, int, int, int, int]:
        """
        Get the number of resources (values) per type.

        Returns:
            Tuple[int, int, int, int, int]: The number of resources per type in the memory manager.
        """
        return (len(self.ints_space.values), len(self.floats_space.values), len(self.strings_space.values), len(self.bools_space.values), len(self.ptrs_space.values))

    def clear_memory_values(self):
        """
        Clear the values stored in the type spaces of the memory manager.
        """
        self.ints_space.values.clear()
        self.floats_space.values.clear()
        self.strings_space.values.clear()
        self.bools_space.values.clear()
        self.ptrs_space.values.clear()

    def __getitem__(self, address: int) -> int | float | str | bool | None:
        """
        Get the value at a memory address.

        Parameters:
            address (int): The memory address.

        Returns:
            int | float | str | bool | None: The value at the memory address, or None if the address is out of bounds.
        """
        typespace = self.get_typespace_from_address(address)
        try:
            return typespace.values[address - typespace.initial_address]
        except IndexError:
            return None

    def __setitem__(self, address: int, value: int):
        """
        Set the value at a memory address.

        Parameters:
            address (int): The memory address.
            value (int): The value to set.
        """
        typespace = self.get_typespace_from_address(address)
        if typespace == self.bools_space:
            if value != None:
                if not isinstance(value, bool):
                    value = True if value == "true" else False
        elif typespace == self.ints_space:
            if value != None:
                value = int(value)
        elif typespace == self.floats_space:
            if value != None:
                value = float(value)
        elif typespace == self.strings_space:
            if value != None:
                value = str(value)
        elif typespace == self.ptrs_space:
            if value != None:
                self[typespace.values[address - typespace.initial_address]] = value
                return
        typespace.values[address - typespace.initial_address] = value

    def __str__(self) -> str:
        """
        Return a string representation of the MemoryManager object.

        Returns:
            str: The string representation of the MemoryManager object.
        """
        output = ""
        for space in [self.ints_space, self.floats_space, self.strings_space, self.bools_space, self.ptrs_space]:
            for address, value in enumerate(space.values):
                output += f"\n{address + space.initial_address}-{value}"
        return output
    
    def print(self, scope: str):
        """
        Print the memory manager's contents.

        Parameters:
            scope (str): The scope of the memory manager.
        """
        print(f"\n--{scope} Memory Manager--")
        memory_spaces = [("ints", self.ints_space), ("floats", self.floats_space), ("strings", self.strings_space), ("bools", self.bools_space), ("ptrs", self.ptrs_space)]
        for space_name, space in memory_spaces:
            print(space_name)
            for address, value in enumerate(space.values):
                print(f"{address + space.initial_address}\t{value}")