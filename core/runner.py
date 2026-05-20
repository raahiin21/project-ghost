import subprocess        #tool to run external commands, launching other programs and interacting with system shell
import sys               #This module provides direct access to all 'built-in'identifiers of Python; for example, builtins.len is the full name for the built-in function len().

from core.classifier import classify_error

def run_process(command):
    process = subprocess.Popen(  #used to intract with a process while its running
        command,
        stdout=subprocess.PIPE,  #PIPE redirects these sterams into Ghost's hand
        stderr=subprocess.PIPE,  #so that it can read and process them programitically
        text=True                # used to make everything readble string automaticlly
    )

    stdout, stderr = process.communicate() #waits for the process to fully finish and returns everything at once in a single string

    #readlines(): works on a file or stream object, reads lines as they come, keeps the \n at the end of each line
    #splitlines(): works on a string (as I we are using communictae() which returns string), splits it by line breaks, and automatically strips the \n cleanly

    if stderr:
        stderr_lines = stderr.strip().splitlines()
        full_traceback = "".join(stderr_lines).strip()
        last_line = stderr_lines[-1].strip()
        error_type = classify_error(last_line) 

        print(f"\n[GHOST CAUGHT — {error_type}]")
        print(f"Details: {last_line}")
        print(f"\nFull traceback:\n{full_traceback}")
