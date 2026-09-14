from core.db import get_connection
from core.patterns import analyze_patterns
from core.display import print_session_table
from core.patterns import Counter

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
    
    rows=[]
    
    for session in sessions:
        session_id, started_at, directory =  session

        cursor.execute("SELECT error_type, message, file_name FROM errors WHERE session_id =?", (session_id,))
        errors = cursor.fetchall()

        error_count = len(errors)

        if errors:
            error_types = [e[0] for e in errors]
            top_type = Counter(error_types).most_common(1)[0][0]
        else:
            top_type = "None"

        rows.append((
            str(session_id),
            started_at[:19],
            str(error_count),
            top_type
        ))

    print_session_table(rows)
    conn.close()