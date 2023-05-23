import sys
from grammar import parser, get_data_to_compiler

if __name__ == '__main__':
    if len(sys.argv) == 2:
        file_name = sys.argv[1]
        if file_name.endswith('.adeo'):
            try:
                with open(file_name, 'r') as file:
                    file_content = file.read()
                    result = ""
                    if parser.parse(file_content, tracking=True) == "END":
                        data = get_data_to_compiler()
                        for d in data:
                            result += d
                    else:
                        result += "\nThe data from the .adeo file is invalid for Adeo language.\n"
                    obj_file_name = file_name.rsplit(".", 1)[0] + ".adeoobj"
                    with open(obj_file_name, "w") as obj_file:
                        obj_file.write(result)
                    # print(result)
            except (EOFError, FileNotFoundError) as e:
                print(e)
        else:
            print("ERROR: Please provide a .adeo file as input.")
    else:
        print("ERROR: Filename not added correctly.")
