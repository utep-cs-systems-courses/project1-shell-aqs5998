import os, re, sys

shellPromptToken = os.getenv("PS1")
shellPromptToken = "Wierdo program"
if shellPromptToken is None:
    shellPrompt = str(input("?> ")) 
else:
    shellPrompt = str(input(f"{shellPromptToken} "))
    os.write(1, ("About to fork (pid:%d)\n" % pid).encode())

    rc = os.fork()

    if rc < 0:
        os.write(2, ("fork failed, returning %d\n" % rc).encode())
        sys.exit(1)
    elif rc == 0:                   # child
        os.write(1, ("I am child.  My pid==%d.  Parent's pid=%d\n" % (os.getpid(), pid)).encode())
    else:                           # parent (forked ok)
        os.write(1, ("I am parent.  My pid=%d.  Child's pid=%d\n" % (pid, rc)).encode())