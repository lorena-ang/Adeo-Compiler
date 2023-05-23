from variable_table import VariableTable

class ClassDetail:
    def __init__(self, name: str) -> None:
        self.name = name
        self.variable_table = VariableTable()
        
class ClassDirectory:
    def __init__(self):
        self.classes = {}

     # Get the information for a class in the directory
    def get_class_from_directory(self, name: str) -> ClassDetail:
        class_detail = self.classes.get(name)
        if class_detail is not None:
            return class_detail
        raise Exception(f"The information for class '{name}' does not exist.")

    # Add class to directory by name
    def add_class_to_directory(self, name: str):
        self.classes[name] = ClassDetail(name)
        
    # Check if a class exists in the directory
    def check_class_exists(self, name: str) -> bool:
        return name in self.classes
        
    def __str__(self) -> str:
        output = ""
        for class_name, class_detail in self.classes.items():
            output += f"\n{class_name},"
            output += f"{class_detail.variable_table}"
        return output