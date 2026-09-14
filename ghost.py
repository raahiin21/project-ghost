import argparse
import os
from core.db import init_db
from core.db import create_session
from core.runner import run_process
from core.db import get_connection
from core.reporter import generate_report
from core.display import print_banner

def main():
    parser = argparse.ArgumentParser(
        prog="ghost",
        description="Session-aware error tracker for developers"
    )

    parser.add_argument("command", choices=["watch", "report"], help="command to run")
    parser.add_argument("target", nargs="*", help = "command to run your project i.e python app.py")
    parser.add_argument("--all", action="store_true", help="Show all session in report")
    parser.add_argument("--last", type=int, default=5, help="Number of recent sessions to show [deafult: 5]")

    args = parser.parse_args()
    print(f"Running command: {args.command}")

    if args.command == "watch":
        init_db()
        session_id = create_session(os.getcwd())

        target = args.target if args.target else ["python","test_error.py"]

        print_banner()
        print(f"Ghost is watching... Session ID: {session_id}")

        run_process(target, session_id)

    elif args.command == "report": 
        if args.all:
            generate_report(limit=None)
        else:
            generate_report(limit=args.last)

#used to run the file if its being executed directly not if its being imported. else we can use main() too. 
if __name__=="__main__":
    main()