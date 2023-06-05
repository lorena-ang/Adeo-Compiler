from array_manager import ArrayManager
from data_helper import DataHelper
from memory_manager import MemoryManager
from variable_table import Variable, VariableTable
from typing import Optional

class Context:
    """
    The Context class represents a context or scope during program compilation.

    Attributes:
        scope (str): The scope of the context.
        context_memory_manager (MemoryManager): The memory manager associated with the context.
        variable_table (VariableTable): The variable table associated with the context.

    Methods:
        __init__(scope: str, context_memory_manager: MemoryManager, variable_table: Optional[VariableTable] = None):
            Initialize a new instance of the Context class.
        add_variable_to_context(v_name: str, v_type: str, array_manager: Optional[ArrayManager] = None) -> Variable:
            Add a new variable to the context and to the variable table of the context.
        get_variable_from_name(v_name: str) -> Variable:
            Get the information of a variable from its name.
        check_variable_exists(v_name: str) -> bool:
            Check if a variable exists in this context.
        __str__() -> str:
            Get a string representation of the Context object.
    """

    def __init__(self, scope: str, context_memory_manager: MemoryManager, variable_table: Optional[VariableTable] = None):
        self.scope = scope
        self.context_memory_manager = context_memory_manager
        self.variable_table = variable_table or VariableTable()

    def add_variable_to_context(self, v_name: str, v_type: str, array_manager: Optional[ArrayManager] = None) -> Variable:
        """
        Add a new variable to the context and to the variable table of the context.

        Parameters:
            v_name (str): The name of the variable.
            v_type (str): The type of the variable.
            array_manager (Optional[ArrayManager]): The array associated with the variable - Defaults to None.

        Returns:
            Variable: The Variable object representing the added variable.
        """
        if self.scope != "Class" and DataHelper.check_type_simple(v_type):
            if array_manager is None:
                address = self.context_memory_manager.reserve_space(v_type)
            else:
                address = self.context_memory_manager.reserve_space(v_type, array_manager.size)
        elif self.scope == "Class":
            address = self.context_memory_manager.reserve_space(v_type)
        else:
            address = 0
        variable = self.variable_table.add_variable(v_name, v_type, address, array_manager)
        return variable

    def get_variable_from_name(self, v_name: str) -> Variable:
        """
        Get the information of a variable from its name.

        Parameters:
            v_name (str): The name of the variable to retrieve.

        Returns:
            Variable: The Variable object representing the variable.
        """
        return self.variable_table.get_variable_from_name(v_name)

    def check_variable_exists(self, v_name: str) -> bool:
        """
        Check if a variable exists in this context.

        Parameters:
            v_name (str): The name of the variable to check.

        Returns:
            bool: True or False depending on if the variable exists in the context.
        """
        return self.variable_table.check_variable_exists(v_name)
    
    def __str__(self) -> str:
        """
        Get a string representation of the Context object.

        Returns:
            str: A string representation of the Context object.
        """
        return f"Scope: {self.scope}\n--Variable Table--\n{self.variable_table}\n--Temporal Memory Manager--{self.context_memory_manager}"

class ContextStack:
    """
    The ContextStack class manages the stack of contexts.

    Attributes:
        contexts (List[Context]): The stack of contexts.

    Methods:
        __init__():
            Initialize a new instance of the ContextStack class.
        push(context: Context):
            Push a context onto the context stack.
        pop() -> Context:
            Pop a context from the top of the context stack.
        get_variable_from_context(v_name: str) -> Variable:
            Get a variable from any context of the stack.
        get_context_from_name(v_name: str) -> Variable:
            Get a context from the stack if the variable with the given name exists in it.
        check_variable_exists(v_name: str) -> bool:
            Check if a variable exists in any context of the stack.
        print():
            Print the contexts in the context stack.
    """

    def __init__(self):
        self.contexts = []

    def push(self, context: Context):
        """
        Push a context onto the context stack.

        Parameters:
            context (Context): The context to push onto the stack.
        """
        self.contexts.append(context)

    def pop(self) -> Context:
        """
        Pop a context from the top of the context stack.

        Returns:
            Context: The context that was popped.
        """
        return self.contexts.pop()

    def get_variable_from_context(self, v_name: str) -> Variable:
        """
        Get a variable from any context of the stack.

        Parameters:
            v_name (str): The name of the variable to retrieve.

        Returns:
            Variable: The Variable object representing the variable.
        """
        for context in reversed(self.contexts):
            if context.check_variable_exists(v_name):
                return context.get_variable_from_name(v_name)
    
    def get_context_from_name(self, v_name: str) -> Variable:
        """
        Get a context from the stack if the variable with the given name exists in it.

        Parameters:
            v_name (str): The name of the variable that should be in the context.

        Returns:
            Context: The Context object containing the variable.
        """
        for context in reversed(self.contexts):
            if context.check_variable_exists(v_name):
                return context
    
    def check_variable_exists(self, v_name: str) -> bool:
        """
        Check if a variable exists in any context of the stack.

        Parameters:
            v_name (str): The name of the variable to check.

        Returns:
            bool: True or False depending on if the variable exists in any context of the stack.
        """
        for context in reversed(self.contexts):
            if context.check_variable_exists(v_name):
                return True
        return False
    
    def print(self):
        """
        Print the contexts in the context stack.
        """
        for i, context in enumerate(self.contexts):
            print(f"\nContext {i+1}")
            print(context)