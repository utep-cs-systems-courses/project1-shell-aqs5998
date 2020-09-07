import os, re, sys

shellPromptToken = os.getenv("PS1")
shellPromptToken = "Wierdo program"
if shellPromptToken is None:
    shellPrompt = str(input("?> ")) 
else:
    shellPrompt = str(input(f"{shellPromptToken} "))