import sys
from program_error import ProgramError
from virtual_machine import VirtualMachine
from pathlib import Path

if __name__ == '__main__':
    # Check if the correct number of arguments were provided
    if len(sys.argv) != 2:
        print("ERROR: Filename not added correctly.")
        sys.exit(1)
    file_name = sys.argv[1]
    # Check if the file has the correct extension
    if not file_name.endswith('.adeoobj'):
        print("ERROR: Please provide a .adeoobj file as input.")
        sys.exit(1)
    try:
        with open(file_name, 'r') as file:
            lines = file.readlines()
            # Check if there was a compilation error
            if lines[0] == "ADEO COMPILATION ERROR\n":
                print("ADEO EXECUTION ERROR")
                print(f"{Path(file_name).name} COMPILATION_ERROR_PRESENT: Cannot perform execution because there are compilation errors that need to be fixed.")
            else:
                virtual_machine = VirtualMachine()
                sections = ["--Global Memory--", "--Constants--", "--Functions--", "--Quadruples--"]
                section_data = {}
                current_section = None
                # Save all the data from the object file
                for line in lines:
                    line = line.removesuffix("\n")
                    if line.strip() in sections:
                        current_section = line.strip()
                        section_data[current_section] = []
                    elif current_section is not None:
                        section_data[current_section].append(line.strip())
                # Process the sections of data and populate memory, function directory, and quadruples
                virtual_machine.process_section_data(section_data)
                try:
                    # Start execution of quadruples
                    virtual_machine.start_execution()
                except ProgramError as e:
                    # Display execution error
                    print("\n--------------------")
                    print("ADEO EXECUTION ERROR")
                    print(f"{Path(file_name).name} {e.error_type}: {e.description}.")
    except (EOFError, FileNotFoundError) as e:
        print("ERROR: Cannot find the file or directory.")
        sys.exit(1)
