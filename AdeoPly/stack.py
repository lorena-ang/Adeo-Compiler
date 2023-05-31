from typing import Optional
from variable_table import Variable, VariableTable
from memory_manager import MemoryManager
from array_manager import ArrayManager
from data_processor import DataProcessor

data_processor = DataProcessor()

class Context:
    def __init__(self, scope: str, context_memory_manager: MemoryManager, variable_table: Optional[VariableTable] = None) -> None:
        self.scope = scope
        self.context_memory_manager = context_memory_manager
        self.variable_table = variable_table or VariableTable()

    # Check if a variable exists in this context
    def check_variable_exists(self, name: str) -> bool:
        return self.variable_table.check_variable_exists(name)

    # Get attributes of variable from its name
    def get_variable_from_name(self, name: str) -> Variable:
        return self.variable_table.get_variable_from_name(name)

    # Add a new variable to the context
    def add_variable_to_context(self, name: str, type: str, array_manager: Optional[ArrayManager] = None) -> Variable:
        if self.scope != "Class" and data_processor.check_type_simple(type):
            if array_manager is None:
                address = self.context_memory_manager.reserve_space(type)
            else:
                address = self.context_memory_manager.reserve_space(type, array_manager.size)
        elif self.scope == "Class":
            address = self.context_memory_manager.reserve_space(type)
        else:
            address = 0
        variable = self.variable_table.add_variable(name, type, address, array_manager)
        return variable
    
    # DELETE: Print for debugging
    def __str__(self) -> str:
        return f"Scope: {self.scope} {self.variable_table}{self.context_memory_manager}"

class Stack:
    def __init__(self) -> None:
        self.contexts = []

    def push(self, context: Context) -> None:
        self.contexts.append(context)

    def pop(self) -> Context:
        if self.contexts:
            return self.contexts.pop()
        else:
            raise IndexError("Cannot pop from an empty stack")

    # Check if a variable exists in any context
    def check_variable_exists(self, name: str) -> bool:
        for context in reversed(self.contexts):
            if context.check_variable_exists(name):
                return True
        return False

    # Get a variable from any context
    def get_variable_from_context(self, name: str) -> Variable:
        for context in reversed(self.contexts):
            if context.check_variable_exists(name):
                return context.get_variable_from_name(name)
    
    def print(self) -> None:
        for i, context in enumerate(self.contexts):
            print(f"\nContext {i+1}:")
            print(context)