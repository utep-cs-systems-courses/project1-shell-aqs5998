import os, re, sys, time, subprocess


shellPromptToken = os.getenv("PS1")
commandList = ["ls", "cd", "..", "mkdir", "exit", "bash"]
Value = False

#shellPrompt = str(input(f"{shellPromptToken} "))
def push_cd(path): #Convert the path into another path
    try:
        os.chdir(os.path.abspath(path))
    except Exception:
        print("cd: no such file or directory: {}".format(path))

#execute commands and handle lspiping
def execute_command(command):
    try:
        if ">" in command:  # save for restoring later on
            #print(command)
            #print("Command works")
            s_in = 0
            s_out = 0
            s_in = os.dup(0)
            s_out = os.dup(1)
            # first command takes commandut from stdin
            # iterate over all the commands that are piped
            # fdin will be stdin if it's the first iterationls
            path = ""
            if command == command.split(">")[-1]:
                pass
            else:
                path = command.split(">")[-1]
            cmd = command.split(">")
            # first command takes commandut from stdin
            fdin = os.dup(s_in)
            #print(cmd[1])
            fd = os.open(path, os.O_CREAT | os.O_WRONLY) 
            #when reading < make ready only file O_RDONLY
            fd_out = os.dup2(fd, 1)
            os.close(fd)
            os.set_inheritable(1,True)
            count = 0
            for cmd in command.split(">"):
                count = count + 1
                try:
                    #print("Does it reach here try")
                    #print(cmd.strip().split())
                    #sys.stdout = open(cmd.strip().split(), "w")
                    subprocess.run(cmd.strip().split())
                    pass
                except Exception:
                    #print("Does it reach here exception")
                    pass
            #os.set_inheritable(1,False)
            # restore stdout and stdin
            #os.dup2(fd_out, 1)
            os.dup2(s_in, 0)
            os.dup2(s_out, 1)
            os.close(fd)
            os.close(s_in)
            os.close(s_out)
            #print("Does it reach here")
        elif "|" in command:  # save for restoring later on
            s_in = 0
            s_out = 0
            s_in = os.dup(0)
            s_out = os.dup(1)

            # first command takes commandut from stdin
            fdin = os.dup(s_in)

            # iterate over all the commands that are piped
           # fdin will be stdin if it's the first iteration
            # and the readable end of the pipe if not.
            for cmd in command.split("|"):
                os.dup2(fdin, 0)
                os.close(fdin)

                # restore stdout if this is the last command
                if cmd == command.split("|")[-1]:
                    fdout = os.dup(s_out)
                else:
                    fdin, fdout = os.pipe()

                # redirect stdout to pipe
                os.dup2(fdout, 1)
                os.close(fdout)
                try:
                    subprocess.run(cmd.strip().split())
                except Exception:
                    print("pipe command not found: {}".format(cmd.strip()))

            # restore stdout and stdin
            os.dup2(s_in, 0)
            os.dup2(s_out, 1)
            os.close(s_in)
            os.close(s_out)
        else:
            #print("End")
            subprocess.run(command.split(" "))
    except Exception:
        #print("Arrived to the bottom of exepction")
        pass

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
            print(command)
            execute_command(command)

main()