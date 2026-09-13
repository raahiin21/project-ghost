from core.db import get_connection
from core.patterns import analyze_patterns

def generate_report(limit=5):
    conn = get_connection()
    cursor = conn.cursor()

    if limit:
        cursor.execute("SELECT id, started_at, directory FROM sessions ORDER BY id DESC LIMIT ?", (limit,))
    else:
        cursor.execute("SELECT id, started_at, directory FROM sessions ORDER BY id DESC")

    sessions =  cursor.fetchall()

    if not sessions:
        print("No session found")
        conn.close()
        return
    
    for session in sessions:
        session_id, started_at, directory =  session

        cursor.execute("SELECT error_type, message, file_name FROM errors WHERE session_id =?", (session_id,))
        errors = cursor.fetchall()

        print(f"\n SESSION {session_id} | {started_at}")
        print(f" Directory: {directory}")
        print(f" Errors caught: {len(errors)}")

        if errors:
            for error in errors:
                error_type, message, file_name = error
                print(f" [{error_type} in {file_name}]")

        insights = analyze_patterns(session_id)
        if insights: 
            print(f"\n [PATTERNS]")
            for insights in insights:
                print(f"    {insights}")

        else:
            print(f"No errors recorded")

    conn.close()