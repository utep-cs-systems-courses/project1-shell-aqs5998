#! /usr/bin/env python3


import os, sys, time, re


shellPromptToken = os.getenv("PS1")
commandList = ["ls", "cd", "..", "mkdir", "exit", "bash"]
Value = False

def redirect(userInput):
        #print(userInput[0])
        #print(userInput[1])
        if '>' in userInput:
            userInput = userInput.split('>')
            os.close(1) #closes the read output to terminal
            sys.stdout = open(userInput[1].strip(), "w") #opens the file out.txt to the system stout
            os.set_inheritable(1, True) #makes sure that output after is written to file
            pathCommand(userInput[0].split()) #executes command
        else:
            os.close(0) #closes the read output to terminal
            sys.stdin = open(userInput[1].strip(), 'r')  #opens the file out.txt to the system stout
            os.set_inheritable(0, True) #makes sure that output after is written to file
            pathCommand(userInput[0].split()) #executes command
def pathCommand(args): #Taken from execute demo
        for dir in re.split(":", os.environ['PATH']): # try each directory in the path
            program = "%s/%s" % (dir, args[0])
            try:
                os.execve(program, args, os.environ) # try to exec program
            except FileNotFoundError:             # ...expected
                pass                              # ...fail quietly
        os.write(2, ("Child:    Could not exec %s\n" % args[0]).encode())
        sys.exit(1) # terminate with error

def changeDirectory(userInput):
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

def tryCommand(userInput):
    pid = os.getpid()
    os.write(1, ("About to fork (pid:%d)\n" % pid).encode())
    rc = os.fork()
    if rc < 0:
        os.write(2, ("fork failed, returning %d\n" % rc).encode())
        sys.exit(1)
    elif rc == 0:                   # child
        os.write(1, ("Child: My pid==%d.  Parent's pid=%d\n" %(os.getpid(), pid)).encode())
        args = userInput.split()
        if "|" in userInput: 
            pipe = userInput.split("|")
            pipeCommand1= pipe[0].split()
            pipeCommand2 = pipe[1].split()
            pr, pw = os.pipe()  # file descriptors pr, pw for reading and writing
            for f in (pr, pw):
                os.set_inheritable(f, True)
            pipeFork = os.fork()
            if pipeFork < 0:  # fork failed
                os.write(2, ('Fork failed').encode())
                sys.exit(1)
            if pipeFork == 0: # child - will write to pipe
                os.close(1) # redirect child's stdout
                os.dup(pw)
                os.set_inheritable(1, True)
                for fd in (pr, pw):
                    os.close(fd)
                pathCommand(pipeCommand1)    
            else: # parent (forked ok)
                os.close(0) #closed the terminal input
                os.dup(pr) #called pr to read from input pre
                os.set_inheritable(0, True)
                for fd in (pw, pr):
                    os.close(fd)
                pathCommand(pipeCommand2)                            
        if '>' in userInput:
            redirect(userInput)
        elif '<' in userInput:
            redirect(userInput)
        else:
            pathCommand(args)
    else:                      # parent (forked ok)
        os.write(1, ("Parent: My pid=%d.  Child's pid=%d\n" %(pid, rc)).encode())
        childPidCode = os.wait()
        os.write(1, ("Parent: Child %d terminated with exit code %d\n" %childPidCode).encode())

def main():
    while True:
        if 'PS1' in os.environ:
            os.write(1, (os.environ['PS1']).encode())
        else:
            os.write(1, ('$ ').encode())
            try:
                i = os.read(0, 500)
                s = i.decode()
                userInput = s
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
            changeDirectory(userInput)
        if userInput != "":
            tryCommand(userInput)
main()
