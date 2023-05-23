from memory_manager import MemoryManager
from function_directory import FunctionDirectoryVM
from quadruples import Quad, Quadruples
from data_processor import DataProcessor
import re, ast

data_processor = DataProcessor()

class VirtualMachine:
    def __init__(self) -> None:
        self.function_directory = FunctionDirectoryVM()
        self.quadruples = Quadruples()
        self.memory_stack = []
        self.global_memory_manager = MemoryManager(0)
        self.constant_memory_manager = MemoryManager(5000)
        self.temporal_memory_manager = MemoryManager(10000, (20,20,20,20,20))

    # Store values from adeoobj file
    def process_section_data(self, section_data):
        sections = ["--Global Memory--", "--Constants--", "--Functions--", "--Classes--", "--Quadruples--"]
        for section, data in section_data.items():
            # Global memory
            if section == sections[0]:
                global_memory_resources = data[0]
                for elem in data[1:]:
                    v = elem.split("-")
                    v_type = self.global_memory_manager.get_type_from_address(int(v[0]))
                    v_val = data_processor.change_to_type(v_type, v[1])
                    if v_val is None:
                        self.global_memory_manager.reserve_space(v_type)
                    else:
                        self.global_memory_manager.add_value_to_memory(v_val)
            # Constant memory
            elif section == sections[1]:
                constant_memory_resources = data[0]
                for elem in data[1:]:
                    c = elem.split("-")
                    c_type = self.constant_memory_manager.get_type_from_address(int(c[0]))
                    c_val = data_processor.change_to_type(c_type, c[1])
                    self.constant_memory_manager.add_value_to_memory(c_val)
            # Functions
            elif section == sections[2]:
                for elem in data:
                    f = re.findall(r'\[[^\]]*\]|\([^)]*\)|[^,]+', elem)
                    f_resources = ast.literal_eval(f[2])
                    self.function_directory.add_function_to_directory(f[0], int(f[5]), f_resources)
            # Quadruples
            elif section == sections[4]:
                for elem in data:
                    q = elem[1:-1].split(',')
                    operator = q[0]
                    v1 = int(q[1]) if q[1] != 'None' else None
                    v2 = int(q[2]) if q[2] != 'None' else None
                    v3 = int(q[3]) if q[3] != 'None' else None
                    self.quadruples.add_quad(Quad(operator, v1, v2, v3))

    # Get the type of memory manager through the address number
    def get_memory_manager_type(self, address: int | None):
        if address is not None and address >= 8000:
            return self.temporal_memory_manager
        elif address is not None and address < 8000 and address >= 4000:
            return self.constant_memory_manager
        else:
            return self.global_memory_manager

    # Start processing quadruples
    def start_execution(self):
        for quad in self.quadruples:
            m1 = self.get_memory_manager_type(quad.left_address)
            m2 = self.get_memory_manager_type(quad.right_address)
            m3 = self.get_memory_manager_type(quad.return_address)
            
            if quad.operator == "=":
                m3[quad.return_address] = m1[quad.left_address]
            elif quad.operator == "+":
                m3[quad.return_address] = m1[quad.left_address] + m2[quad.right_address]
            elif quad.operator == "-":
                m3[quad.return_address] = m1[quad.left_address] - m2[quad.right_address]
            elif quad.operator == "*":
                m3[quad.return_address] = m1[quad.left_address] * m2[quad.right_address]
            elif quad.operator == "/":
                m3[quad.return_address] = m1[quad.left_address] / m2[quad.right_address]
            elif quad.operator == ">":
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
            elif quad.operator == "||":
                m3[quad.return_address] = m1[quad.left_address] or m2[quad.right_address]
            elif quad.operator == "&&":
                m3[quad.return_address] = m1[quad.left_address] and m2[quad.right_address]
            elif quad.operator == "PRINT":
                print(m3[quad.return_address])
            elif quad.operator == "READ":
                m3[quad.return_address] = input()