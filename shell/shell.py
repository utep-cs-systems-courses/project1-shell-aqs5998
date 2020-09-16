import os, sys, time, re


shellPromptToken = os.getenv("PS1")
commandList = ["ls", "cd", "..", "mkdir", "exit", "bash"]
Value = False

while True:
        if 'PS1' in os.environ:
            os.write(1, (os.environ['PS1']).encode())
        else:
            os.write(1, ('$$ ').encode())
            try:
                userInput = input()
            except EOFError:
                sys.exit(1)
