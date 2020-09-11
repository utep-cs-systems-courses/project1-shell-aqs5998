import os, re, sys
import subprocess

shellPromptToken = os.getenv("PS1")
commandList = ["ls", "cd", "..", "mkdir", "exit", "bash"]
Value = False

#shellPrompt = str(input(f"{shellPromptToken} "))
def push_cd(path): #Convert the path into another path
    try:
        os.chdir(os.path.abspath(path))
    except Exception:
        print("cd: no such file or directory: {}".format(path))

def execute_commands(command):
    try:
        subprocess.run(command.split())
    except Exception:
        print("{}: command not found".format(command))

def main():
    while True:
        command = input("$ ")
        if command == "exit":
            print("see ya")
            sys.exit(0)
        elif command[:3] == "cd ":
            push_cd(command[3:])
        elif command == "help":
            print("{}: is a sample command directory that has not been finished".format(command))
        else:
            execute_commands(command)

main()