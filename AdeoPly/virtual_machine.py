from memory_manager import MemoryManager
from function_directory import FunctionDirectoryVM
from quadruples import Quad, Quadruples
from data_processor import DataProcessor
from typing import Tuple
import re, ast, codecs

data_processor = DataProcessor()

class VirtualMachine:    
    def __init__(self) -> None:
        self.global_memory_manager = MemoryManager(0)
        self.constant_memory_manager = MemoryManager(5000)
        self.function_memory_manager = MemoryManager(10000, (0, 0, 0, 0, 0))
        self.function_directory = FunctionDirectoryVM()
        self.quadruples = Quadruples()
        self.function_memory_stack = []
        self.temporal_memory_manager = None
        self.return_value = None

    def initialize_function_memory(self, address: int):
        f_name = self.global_memory_manager[address]
        f_resources = self.function_directory.get_function_from_directory(f_name).resources
        self.temporal_memory_manager = MemoryManager(10000, f_resources)

    # Store values from adeoobj file
    def process_section_data(self, section_data):
        sections = ["--Global Memory--", "--Constants--", "--Functions--", "--Quadruples--"]
        for section, data in section_data.items():
            # Global memory
            if section == sections[0]:
                for elem in data:
                    v = elem.split("-")
                    v_type = self.global_memory_manager.get_type_from_address(int(v[0]))
                    v_val = data_processor.change_to_type(v_type, v[1])
                    if v_val is None:
                        self.global_memory_manager.reserve_space(v_type)
                    else:
                        self.global_memory_manager.add_value_to_memory(v_val)
            # Constant memory
            elif section == sections[1]:
                for elem in data:
                    c = elem.split("-")
                    c_type = self.constant_memory_manager.get_type_from_address(int(c[0]))
                    c_val = data_processor.change_to_type(c_type, c[1])
                    self.constant_memory_manager.add_value_to_memory(c_val)
            # Functions
            elif section == sections[2]:
                for elem in data:
                    f = re.findall(r'\[[^\]]*\]|\([^)]*\)|[^,]+', elem)
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
                    self.quadruples.add_quad(Quad(operator, v1, v2, v3))

    # Get the type of memory manager through the address number
    def get_memory_manager_type(self, address: int | None):
        if address is not None and address >= 10000:
            return self.function_memory_manager
        elif address is not None and address < 10000 and address >= 5000:
            return self.constant_memory_manager
        else:
            return self.global_memory_manager
    
    # Check the variables in the list have been initialized
    def check_variable_initialized(self, memory: list[Tuple[int, int | float | str | bool]]) -> None:
        for v_address, v_value in memory:
            if v_value is None:
                raise Exception(f"The constant at '{v_address}' was not initialized.")

    # Start processing quadruples
    def start_execution(self) -> int:
        for quad in self.quadruples:
            # Get the type of memory manager for each address
            m1 = self.get_memory_manager_type(quad.left_address)
            m2 = self.get_memory_manager_type(quad.right_address)
            m3 = self.get_memory_manager_type(quad.return_address)
            
            if quad.operator == "=":
                self.check_variable_initialized([(quad.left_address, m1[quad.left_address])])
                m3[quad.return_address] = m1[quad.left_address]
                # In case the value assignment is for a return
                self.return_value = m1[quad.left_address]
            elif quad.operator in ["+", "-", "*", "/"]:
                self.check_variable_initialized([(quad.left_address, m1[quad.left_address]), (quad.right_address, m2[quad.right_address])])
                if quad.operator == "+":
                    m3[quad.return_address] = m1[quad.left_address] + m2[quad.right_address]
                elif quad.operator == "-":
                    m3[quad.return_address] = m1[quad.left_address] - m2[quad.right_address]
                elif quad.operator == "*":
                    m3[quad.return_address] = m1[quad.left_address] * m2[quad.right_address]
                elif quad.operator == "/":
                    m3[quad.return_address] = m1[quad.left_address] / m2[quad.right_address]
            elif quad.operator in [">", ">=", "<", "<=", "==", "!="]:
                self.check_variable_initialized([(quad.left_address, m1[quad.left_address]), (quad.right_address, m2[quad.right_address])])
                if quad.operator == ">":
                    m3[quad.return_address] = m1[quad.left_address] > m2[quad.right_address]
                elif quad.operator == ">=":
                    m3[quad.return_address] = m1[quad.left_address] >= m2[quad.right_address]
                elif quad.operator == "<":
                    m3[quad.return_address] = m1[quad.left_address] < m2[quad.right_address]
                elif quad.operator == "<=":
                    m3[quad.return_address] = m1[quad.left_address] <= m2[quad.right_address]
                elif quad.operator == "==":
                    m3[quad.return_address] = m1[quad.left_address] == m2[quad.right_address]
                elif quad.operator == "!=":
                    m3[quad.return_address] = m1[quad.left_address] != m2[quad.right_address]
            elif quad.operator in ["||", "&&"]:
                self.check_variable_initialized([(quad.left_address, m1[quad.left_address]), (quad.right_address, m2[quad.right_address])])
                if quad.operator == "||":
                    m3[quad.return_address] = m1[quad.left_address] or m2[quad.right_address]
                elif quad.operator == "&&":
                    m3[quad.return_address] = m1[quad.left_address] and m2[quad.right_address]
            elif quad.operator == "PRINT":
                self.check_variable_initialized([(quad.return_address, m3[quad.return_address])])
                value = codecs.decode(str(m3[quad.return_address]), "unicode_escape")
                print(value, end="")
            elif quad.operator == "READ":
                m3[quad.return_address] = input()
            elif quad.operator == "GOTO":
                self.check_variable_initialized([(quad.return_address, m3[quad.return_address])])
                self.quadruples.instr_ptr = int(m3[quad.return_address])
            elif quad.operator == "GOTOF":
                self.check_variable_initialized([(quad.left_address, m1[quad.left_address]), (quad.return_address, m3[quad.return_address])])
                if m1[quad.left_address] == False:
                    self.quadruples.instr_ptr = int(m3[quad.return_address])
            elif quad.operator == "ERA":
                self.initialize_function_memory(quad.return_address)
            elif quad.operator == "PARAM":
                self.check_variable_initialized([(quad.left_address, m1[quad.left_address])])
                self.temporal_memory_manager[quad.return_address] = m1[quad.left_address]
            elif quad.operator == "GOSUB":
                if quad.return_address is None:
                    raise Exception(f"The variable at address '{quad.return_address}' is not present in memory.")
                self.function_memory_stack.append((self.quadruples.instr_ptr, self.function_memory_manager))
                self.function_memory_manager = self.temporal_memory_manager
                # Set instruction pointer to the start of the function
                f_name = self.global_memory_manager[quad.return_address]
                self.quadruples.instr_ptr = self.function_directory.get_function_from_directory(f_name).initial_quad_address
            elif quad.operator == "ENDFUNC" or quad.operator == "ENDPROG":
                # Clear temporal memory
                self.temporal_memory_manager.clear_memory_values()
                # Get previously stored function memory or use global memory
                self.quadruples.instr_ptr, self.function_memory_manager = self.function_memory_stack.pop()
                if len(self.function_memory_stack) == 0:
                    return self.return_value