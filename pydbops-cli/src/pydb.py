import subprocess
import sys
from pydbops_cli import Pydbops_cli

if __name__ == "__main__":
    if (sys.argv[1] == "init") or (sys.argv[1] == "connect"):
        try:
            from pydbops import *
        except:
            choice = input("It seems 'pydbops' is not installed. Do you wish to install it first? (Y/N): ")
            if (choice == "Y") or (choice == "y"):
                subprocess.call("")
                with open("install_information.txt") as f:
                    print("\n", f.read())
                print("\nInstallation complete!\n")
                exit(1)
            elif (choice == "n") or (choice == "N"):
                exit(1)
        obj = Pydbops_cli()
        print("  Connected!")
        while True:
            choice = input("> ")
            command = choice.split(" ")
            if choice == "":
                print("  Helpful commands :\n", obj.command_list, "\n")
                continue
            elif (choice == "close") or (choice == "Close"):
                print("  Closed!")
                del obj
                break
            elif command[0] in obj.command_list:
                obj.check(choice)
            else:
                print("  Invalid Command!")
                continue