import os
#from Testing import hdmain

print_menu_again = 0
menu_exit_program = 1
higher_definition_huge_size = 2

def print_menu(invalid_entry):
    os.system('cls')
    if invalid_entry:
        print("Invalid Entry, please enter from the following\n")
    else:
        print("What you thinking today?\n")
    menu_file = open("menu_file.txt","r")
    print(menu_file.read())
    menu_file.close()

def menu_functions(menu_input):
    if menu_input == menu_exit_program:
        os.system('cls')
        return -1
    elif menu_input == print_menu_again:
        print_menu(False)
    elif menu_input == higher_definition_huge_size:
        print("Running this file python3 ./Testing/hdmain.py")
        os.system('python3 ./Testing/hdmain.py')
        print("File Run Successfully")
        #hdmain.run_hd_case()
    else:
        print_menu(True)
    return 0

def main():
    program_running = True
    print("Welcome to BITS-GIS")
    print_menu(False)
    while program_running == True:
        menu_input=input()
        if menu_input=='' or not menu_input.isnumeric():
            print_menu(True)
            continue
        menu_input=int(menu_input)
        if menu_functions(menu_input)==-1:
            program_running=False

if __name__ == "__main__":
    main()