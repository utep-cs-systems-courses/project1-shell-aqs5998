import os, sys, time, re


shellPromptToken = os.getenv("PS1")
commandList = ["ls", "cd", "..", "mkdir", "exit", "bash"]
Value = False

while True:
        if 'PS1' in os.environ:
            os.write(1, (os.environ['PS1']).encode())
        else:
            os.write(1, ('$ ').encode())
            try:
                userInput = input()
            except EOFError:
                sys.exit(1)
        if userInput == "": 
            continue
        """Exits the program"""
        if 'exit' in userInput: 
            print("see ya")
            break
        """Changes Directory"""
        if 'cd' in userInput: 
                if '..' in userInput:
                    changeDir = '..'
                else:
                    changeDir = userInput.split('cd')[1].strip()
                try:
                    os.chdir(changeDir)
                except FileNotFoundError:
                    pass
                continue
