from core.db import get_connection
from core.patterns import analyze_patterns
from core.display import print_session_table
from core.patterns import Counter
from datetime import datetime

def generate_report(limit=5):
    conn = get_connection()
    cursor = conn.cursor()

    if limit:
        cursor.execute("SELECT id, started_at, ended_at, directory FROM sessions ORDER BY id DESC LIMIT ?", (limit,))
    else:
        cursor.execute("SELECT id, started_at, ended_at, directory FROM sessions ORDER BY id DESC")

    sessions =  cursor.fetchall()

    if not sessions:
        print("No session found")
        conn.close()
        return
    
    rows=[]
    
    for session in sessions:
        session_id, started_at, ended_at, directory =  session

        cursor.execute("SELECT error_type, message, file_name FROM errors WHERE session_id =?", (session_id,))
        errors = cursor.fetchall()

        error_count = len(errors)

        if errors:
            error_types = [e[0] for e in errors]
            top_type = Counter(error_types).most_common(1)[0][0]
            files = list(set([e[2] for e in errors]))
            files_str = ", ".join(files)

        else:
            top_type = "None"
            files_str = "None"

        if started_at and ended_at:
            start = datetime.fromisoformat(started_at)
            end = datetime.fromisoformat(ended_at)
            duration = str( end - start ).split(".")[0]

        else:
            duration = "N/A"


        rows.append((
            str(session_id),
            started_at[:19],
            duration,
            str(error_count),
            top_type,
            files_str
        ))

    print_session_table(rows)
    conn.close()