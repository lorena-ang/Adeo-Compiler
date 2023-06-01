import ast, codecs, re
from data_helper import DataHelper
from function_directory import FunctionDirectoryVM
from memory_manager import MemoryManager, SIZE
from program_error import raise_program_error, ProgramErrorType
from quadruples import Quadruples
from typing import Tuple

START_CONSTANT_MEMORY = SIZE * 5
START_FUNCTION_MEMORY = START_CONSTANT_MEMORY * 2

class VirtualMachine:
    """
    The VirtualMachine class represents a virtual machine that executes quadruples.
    Attributes:
        global_memory_manager (MemoryManager): The memory manager for the global memory.
        constant_memory_manager (MemoryManager): The memory manager for the constant memory.
        function_memory_manager (MemoryManager): The memory manager for the function memory.
        temporal_memory_manager (MemoryManager | None): The memory manager for the temporal memory, or None if not initialized.
        function_directory (FunctionDirectoryVM): The function directory.
        quadruples (Quadruples): The collection of quadruples.
        function_memory_stack (list): A stack that stores the instruction pointer and function memory manager during function calls.
        return_value (int | float | str | bool | None): The return value of a function.

    Methods:
        process_section_data(section_data: dict) -> None:
            Process the sections of data and populate memory, function directory, and quadruples.
        get_memory_manager_type(address: int | None) -> MemoryManager:
            Get the memory manager type based on the address.
        check_variable_initialized(memory: list[Tuple[int, int | float | str | bool]]) -> None:
            Check if variables in the memory list have been initialized.
        check_valid_ptr(curr_address: int, past_address: int, memory: MemoryManager) -> bool:
            Check if the current address corresponds to a valid pointer.
        start_execution() -> int:
            Start executing the quadruples.
    """

    def __init__(self):
        self.global_memory_manager = MemoryManager(0)
        self.constant_memory_manager = MemoryManager(START_CONSTANT_MEMORY)
        self.function_memory_manager = MemoryManager(START_FUNCTION_MEMORY)
        self.temporal_memory_manager = None
        self.function_directory = FunctionDirectoryVM()
        self.quadruples = Quadruples()
        self.function_memory_stack = []
        self.return_value = None

    def process_section_data(self, section_data):
        """
        Process the sections of data and populate memory, function directory, and quadruples.

         Parameters:
            section_data (dict): A dictionary containing the section names as keys and their data as values.
        """
        sections = ["--Global Memory--", "--Constants--", "--Functions--", "--Quadruples--"]
        for section, data in section_data.items():
            # Global memory
            if section == sections[0]:
                for elem in data:
                    v = re.findall(r'(\d+).*?-(.*)', elem)[0]
                    v_type = self.global_memory_manager.get_type_from_address(int(v[0]))
                    if v[1] == "None":
                        self.global_memory_manager.reserve_space(v_type)
                    else:
                        v_value = DataHelper.change_to_type(v_type, v[1])
                        self.global_memory_manager.find_memory_address(v_value)
            # Constant memory
            elif section == sections[1]:
                for elem in data:
                    c = re.findall(r'(\d+).*?-(.*)', elem)[0]
                    c_type = self.constant_memory_manager.get_type_from_address(int(c[0]))
                    c_value = DataHelper.change_to_type(c_type, c[1])
                    self.constant_memory_manager.find_memory_address(c_value)
            # Functions
            elif section == sections[2]:
                for elem in data:
                    f = re.findall(r'\([^)]*\)|[^,]+', elem)
                    f_resources = ast.literal_eval(f[2])
                    self.function_directory.add_function_to_directory(f[0], int(f[3]), f_resources)
            # Quadruples
            elif section == sections[3]:
                for elem in data:
                    q = elem[1:-1].split(',')
                    operator = q[0]
                    v1 = int(q[1]) if q[1] != 'None' else None
                    v2 = int(q[2]) if q[2] != 'None' else None
                    v3 = int(q[3]) if q[3] != 'None' else None
                    self.quadruples.add_quad(operator, v1, v2, v3)

    def get_memory_manager_type(self, address: int | None) -> MemoryManager:
        """
        Get the memory manager type based on the address.

        Parameters:
            address (int | None): The address number.

        Returns:
            MemoryManager: The memory manager corresponding to the address.
        """
        if address is not None and address >= START_FUNCTION_MEMORY:
            return self.function_memory_manager
        elif address is not None and address < START_FUNCTION_MEMORY and address >= START_CONSTANT_MEMORY:
            return self.constant_memory_manager
        else:
            return self.global_memory_manager

    def check_variable_initialized(self, memory: list[Tuple[int, int | float | str | bool]]):
        """
        Check if variables in the memory list have been initialized.

        Parameters:
            memory (list[Tuple[int, int | float | str | bool]]): The list of memory addresses and values.
        """
        for v_address, v_value in memory:
            if v_value is None:
                raise_program_error(ProgramErrorType.VARIABLE_NOT_INITIALIZED, None, f"The variable at address '{v_address}' was not initialized")
                
    def check_valid_ptr(self, curr_address: int, past_address: int, memory: MemoryManager) -> bool:
        """
        Check if the current address corresponds to a valid pointer.
        
        Parameters:
            curr_address (int): The current quad address, which would change from the original if there a pointer there.
            past_address (int): The original quad address, which will remain the same for the whole execution.
        
        Returns:
            bool: True or False depending on if the current address is a valid pointer.
        """
        return curr_address is not None and memory.get_type_from_address(past_address) == "ptr"

    def start_execution(self) -> int:
        """
        Start executing the quadruples.

        Returns:
            int: The return value of the program.
        """
        for quad in self.quadruples:
            left_address = quad.left_address
            right_address = quad.right_address
            return_address = quad.return_address
            # Get the type of memory manager for each address
            left_memory = self.get_memory_manager_type(left_address)
            right_memory = self.get_memory_manager_type(right_address)
            return_memory = self.get_memory_manager_type(return_address)
            # Update address and memory if there is a pointer
            if self.check_valid_ptr(left_address, quad.left_address, left_memory):
                memory = self.get_memory_manager_type(left_memory[left_address])
                left_address = left_memory[left_address]
                left_memory = memory
            if self.check_valid_ptr(right_address, quad.right_address, right_memory):
                memory = self.get_memory_manager_type(right_memory[right_address])
                right_address = right_memory[right_address]
                right_memory = memory
            if self.check_valid_ptr(return_address, quad.return_address, return_memory) and quad.operator != "PTR":
                memory = self.get_memory_manager_type(return_memory[return_address])
                return_address = return_memory[return_address]
                return_memory = memory

            # Perform quad operations
            if quad.operator == "=":
                self.check_variable_initialized([(left_address, left_memory[left_address])])
                return_memory[return_address] = left_memory[left_address]
                # In case the value assignment is for a return
                self.return_value = left_memory[left_address]
            elif quad.operator in ["+", "-", "*", "/"]:
                self.check_variable_initialized([(left_address, left_memory[left_address]), (right_address, right_memory[right_address])])
                if quad.operator == "+":
                    return_memory[return_address] = left_memory[left_address] + right_memory[right_address]
                elif quad.operator == "-":
                    return_memory[return_address] = left_memory[left_address] - right_memory[right_address]
                elif quad.operator == "*":
                    return_memory[return_address] = left_memory[left_address] * right_memory[right_address]
                elif quad.operator == "/":
                    if right_memory[right_address] == 0:
                        raise_program_error(ProgramErrorType.ARITHMETIC_EXCEPTION, None, "Cannot divide a number by zero")
                    return_memory[return_address] = left_memory[left_address] / right_memory[right_address]
            elif quad.operator in [">", ">=", "<", "<=", "==", "!="]:
                self.check_variable_initialized([(left_address, left_memory[left_address]), (right_address, right_memory[right_address])])
                if quad.operator == ">":
                    return_memory[return_address] = left_memory[left_address] > right_memory[right_address]
                elif quad.operator == ">=":
                    return_memory[return_address] = left_memory[left_address] >= right_memory[right_address]
                elif quad.operator == "<":
                    return_memory[return_address] = left_memory[left_address] < right_memory[right_address]
                elif quad.operator == "<=":
                    return_memory[return_address] = left_memory[left_address] <= right_memory[right_address]
                elif quad.operator == "==":
                    return_memory[return_address] = left_memory[left_address] == right_memory[right_address]
                elif quad.operator == "!=":
                    return_memory[return_address] = left_memory[left_address] != right_memory[right_address]
            elif quad.operator in ["||", "&&"]:
                self.check_variable_initialized([(left_address, left_memory[left_address]), (right_address, right_memory[right_address])])
                if quad.operator == "||":
                    return_memory[return_address] = left_memory[left_address] or right_memory[right_address]
                elif quad.operator == "&&":
                    return_memory[return_address] = left_memory[left_address] and right_memory[right_address]
            elif quad.operator == "PRINT":
                self.check_variable_initialized([(return_address, return_memory[return_address])])
                value = codecs.decode(str(return_memory[return_address]), "unicode_escape")
                print(value, end="")
            elif quad.operator == "READ":
                try:
                    return_memory[return_address] = input()
                except ValueError:
                    raise_program_error(ProgramErrorType.INPUT_TYPE_MISMATCH, None, f"The input cannot be stored in the variable because it is not of the same type")
            elif quad.operator == "GOTO":
                self.check_variable_initialized([(return_address, return_memory[return_address])])
                self.quadruples.instr_ptr = int(return_memory[return_address])
            elif quad.operator == "GOTOF":
                self.check_variable_initialized([(left_address, left_memory[left_address]), (return_address, return_memory[return_address])])
                if not left_memory[left_address]:
                    self.quadruples.instr_ptr = int(return_memory[return_address])
            elif quad.operator == "VER":
                self.check_variable_initialized([(left_address, left_memory[left_address]), (right_address, right_memory[right_address]), (return_address, return_memory[return_address])])
                if left_memory[left_address] < right_memory[right_address] or left_memory[left_address] >= return_memory[return_address]:
                    raise_program_error(ProgramErrorType.ARRAY_INDEX_OUT_OF_BOUNDS, None, f"The index '{left_memory[left_address]}' is outside of the valid range")
            elif quad.operator == "PTR":
                self.check_variable_initialized([(left_address, left_memory[left_address])])
                return_memory.add_ptr(return_address, left_memory[left_address])
            elif quad.operator == "ERA":
                # Get resources from function directory and initialize temporal memory
                f_name = self.global_memory_manager[return_address]
                f_resources = self.function_directory.get_function_from_directory(f_name).resources
                self.temporal_memory_manager = MemoryManager(START_FUNCTION_MEMORY, f_resources)
            elif quad.operator == "PARAM":
                self.check_variable_initialized([(left_address, left_memory[left_address])])
                # Add parameters to temporal memory
                self.temporal_memory_manager[return_address] = left_memory[left_address]
            elif quad.operator == "GOSUB":
                self.function_memory_stack.append((self.quadruples.instr_ptr, self.function_memory_manager))
                self.function_memory_manager = self.temporal_memory_manager
                # Set instruction pointer to the start of the function
                f_name = self.global_memory_manager[return_address]
                self.quadruples.instr_ptr = self.function_directory.get_function_from_directory(f_name).initial_quad_address
            elif quad.operator == "ENDFUNC" or quad.operator == "ENDPROG":
                # Clear temporal memory
                self.temporal_memory_manager.clear_memory_values()
                # Get previously stored function memory or use global memory
                self.quadruples.instr_ptr, self.function_memory_manager = self.function_memory_stack.pop()
                if len(self.function_memory_stack) == 0:
                    return self.return_value