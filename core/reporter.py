from core.db import get_connection

def generate_report():
    conn = get_connection()
    cursor = conn.cursor()

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

        else:
            print(f"No errors recorded")

    conn.close()