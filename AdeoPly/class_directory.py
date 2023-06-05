from variable_table import VariableTable

class Class:
    """
    The Class class represents a class in the program.
    
    Attributes:
        name (str): The name of the class.
        variable_table (VariableTable): The variable table associated with the class.

    Methods:
        __init__(name: str):
            Initialize a new instance of the Class class.
    """
    
    def __init__(self, name: str):
        self.name = name
        self.variable_table = VariableTable()
        
class ClassDirectory:
    """
    The ClassDirectory class stores the classes in the program.
    
    Attributes:
        classes (dict): A dictionary of classes with their names as keys.

    Methods:
        __init__():
            Initialize a new instance of the ClassDirectory class.
        add_class_to_directory(c_name: str):
            Add a class to the directory by name.
        get_class_from_directory(c_name: str) -> Class:
            Get the information for a class in the directory.
        check_class_exists(c_name: str) -> bool:
            Check if a class exists in the directory by name.
        __str__() -> str:
            Get a string representation of the ClassDirectory object.
    """

    def __init__(self):
        self.classes = {}

    def add_class_to_directory(self, c_name: str):
        """
        Add a class to the directory by name.

        Parameters:
            c_name (str): The name of the class to add.
        """
        self.classes[c_name] = Class(c_name)

    def get_class_from_directory(self, c_name: str) -> Class:
        """
        Get the information for a class in the directory.

        Parameters:
            c_name (str): The name of the class to retrieve.

        Returns:
            Class: The Class object representing the class.
        """
        class_detail = self.classes.get(c_name)
        if class_detail is not None:
            return class_detail
        raise Exception(f"The information for class '{c_name}' does not exist.")

    def check_class_exists(self, c_name: str) -> bool:
        """
        Check if a class exists in the directory by name.

        Parameters:
            c_name (str): The name of the class to check.

        Returns:
            bool: True or False depending on if the class exists in the directory.
        """
        return c_name in self.classes
        
    def __str__(self) -> str:
        """
        Get a string representation of the ClassDirectory object.

        Returns:
            str: A string representation of the ClassDirectory object.
        """
        output = ""
        for c_name, class_detail in self.classes.items():
            output += f"\n{c_name}\n"
            output += f"{class_detail.variable_table}"
        return output