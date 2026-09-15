import subprocess        #tool to run external commands, launching other programs and interacting with system shell 

from core.classifier import classify_error
from core.db import log_error
from core.patterns import analyze_patterns
from core.display import print_error, print_insights

def run_process(command, session_id):
    process = subprocess.Popen(  #used to intract with a process while its running
        command,
        stdout=subprocess.PIPE,  #PIPE redirects these sterams into Ghost's hand
        stderr=subprocess.PIPE,  #so that it can read and process them programitically
        text=True                # used to make everything readble string automaticlly
    )

    stdout, stderr = process.communicate() #waits for the process to fully finish and returns everything at once in a single string
    file_name = command[1]

    #readlines(): works on a file or stream object, reads lines as they come, keeps the \n at the end of each line
    #splitlines(): works on a string (as we are using communictae() which returns string), splits it by line breaks, and automatically strips the \n cleanly

    if stderr:
        stderr_lines = stderr.strip().splitlines()
        full_traceback = stderr.strip()
        last_line = stderr_lines[-1].strip()
        error_type = classify_error(last_line) 
        error_log = log_error(session_id, error_type, last_line, file_name)

        print_error(error_type, last_line, full_traceback)
        insights = analyze_patterns(session_id)
        print_insights(insights)