import argparse
import os
from core.db import init_db
from core.db import create_session

def main():
    parser = argparse.ArgumentParser(
        prog="ghost",
        description="Session-aware error tracker for developers"
    )
    parser.add_argument("command", choices=["watch", "report"], help="command to run")
    args = parser.parse_args()
    print(f"Running command: {args.command}")

    if args.command == "watch":
        init_db()
        session_id = create_session(os.getcwd())
        print(f"Ghost is watching... Session ID: {session_id}")

        from core.runner import run_process
        run_process(["python", "test_error.py"], session_id)  #Popen expect a list where first iteam is the program and rest are passed arguments. its like similar as running python [filename].py

    elif args.command == "report":
        print("Generating report...")


#used to run the file if its being executed directly not if its being imported. else we can use main() too. 
if __name__=="__main__":
    main()