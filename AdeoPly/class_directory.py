from variable_table import VariableTable

class ClassDetail:
    name: str
    variable_table: VariableTable

    def __init__(self, name: str) -> None:
        self.name = name
        self.variable_table = VariableTable()
        
class ClassDirectory:
    dir: dict[str, ClassDetail]
    
    def __init__(self):
        self.dir = {}

     # Get the information for a class in the directory
    def get_class_from_directory(self, name: str) -> ClassDetail:
        if (class_detail := self.dir.get(name)) is not None:
            return class_detail
        else:
            raise Exception(f"The information for class '{name}' does not exist.")

    # Add class to directory by name
    def add_class_to_directory(self, name: str):
        self.dir[name] = ClassDetail(name)
        
    # Check if a class exists in the directory
    def check_class_exists(self, name: str) -> bool:
        if self.dir.get(name) is None:
            return False
        else:
            return True
        
    def print(self) -> None:
        for c in self.dir.items():
            print(f"# {c.name}")