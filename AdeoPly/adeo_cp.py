import sys
from grammar import get_data_to_compiler, parser
from program_error import ProgramError
from pathlib import Path

if __name__ == '__main__':
    # Check if the correct number of arguments were provided
    if len(sys.argv) != 2:
        print("ERROR: Filename not added correctly.")
        sys.exit(1)
    file_name = sys.argv[1]
    # Check if the file has the correct extension
    if not file_name.endswith('.adeo'):
        print("ERROR: Please provide a .adeo file as input.")
        sys.exit(1)
    # Create output file name
    obj_file_name = Path(file_name).with_suffix(".adeoobj")
    try:
        with open(file_name, 'r') as file:
            file_lines = file.readlines()
            file_content = "".join(file_lines)
        # Parse file content
        if parser.parse(file_content, tracking=True) == "END":
            # Get data to add to the adeoobj file
            data = get_data_to_compiler()
            result = "".join(data)
        # Add data into the adeoobj file
        with open(obj_file_name, "w") as obj_file:
            obj_file.write(result)
    except ProgramError as e:
        error_message = "ADEO COMPILATION ERROR\n"
        error_message += f"{Path(file_name).name}:{e.line_num} {e.error_type} at line {e.line_num}: {e.description}.\n"
        # Calculate two lines before and after the error line
        start_line = max(1, e.line_num - 2)
        end_line = min(len(file_lines), e.line_num + 2)
        # Write the error message with surrounding lines to obj_file_name
        with open(obj_file_name, "w") as obj_file:
            obj_file.write(error_message)
            print(error_message.rstrip("\n"))
            for line_num in range(start_line, end_line + 1):
                line_to_write = file_lines[line_num - 1].rstrip('\n')
                arrow = "-->" if line_num == e.line_num else "   "
                obj_file.write(f"{arrow} {line_num:3} | {line_to_write}\n")
                print(f"{arrow} {line_num:3} | {line_to_write}")
    except (EOFError, FileNotFoundError) as e:
        print("ERROR: Cannot find the file or directory.")
        sys.exit(1)
    except Exception as e:
        print("ERROR: The data in the file is invalid for Adeo language.")
        sys.exit(1)
