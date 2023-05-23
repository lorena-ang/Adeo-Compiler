import sys
from virtual_machine import VirtualMachine

if __name__ == '__main__':
    if len(sys.argv) == 2:
        file_name = sys.argv[1]
        if file_name.endswith('.adeoobj'):
            try:
                with open(file_name, 'r') as file:
                    virtual_machine = VirtualMachine()
                    lines = file.readlines()

                    sections = ["--Global Memory--", "--Constants--", "--Functions--", "--Classes--", "--Quadruples--"]
                    section_data = {}

                    current_section = None
                    for line in lines:
                        line = line.removesuffix("\n")
                        if line.strip() in sections:
                            current_section = line.strip()
                            section_data[current_section] = []
                        elif current_section is not None:
                            section_data[current_section].append(line.strip())

                    virtual_machine.process_section_data(section_data)
                    virtual_machine.start_execution()
            except (EOFError, FileNotFoundError) as e:
                print(e)
        else:
            print("ERROR: Please provide an .adeoobj file as input.")
    else:
        print("ERROR: Filename not added correctly.")
