from collections import Counter
from core.db import get_connection

def analyze_patterns(session_id):
    conn = get_connection()
    cursor = conn.cursor()

    # Query 1 - errror type in current session | serves rule 1 and 4
    cursor.execute(
        "SELECT error_type, message, file_name FROM errors WHERE session_id = ?", (session_id,)
    )
    errors = cursor.fetchall()

    # Query 2 - error count per file in current session | serves rule 2
    cursor.execute(
        ("SELECT file_name, count (*) as COUNT from errors WHERE session_id = ? GROUP BY file_name"), (session_id,)
    )
    file_counts = cursor.fetchall() 

    # Query 3 - last 5 sesssion with error counts | serves rule 3 and 5
    cursor.execute(
        """SELECT s.id, COUNT(e.id) as error_count
        FROM sessions s
        LEFT JOIN errors e ON s.id=e.session_id
        WHERE s.id <= ? 
        GROUP BY s.id
        ORDER BY s.id DESC
        LIMIT 5 """,
        (session_id,)
    )

    recent_session = cursor.fetchall()
    conn.close()

    if not errors:
        return["Clean Session. No error recorded."]

    insights = []
    error_types = [e[0] for e in errors]
    type_counts = Counter(error_types)

    # in the above part I have made some rules around pattern/habits, session and error.. it should help in development to understand what thing is cuasing what.
    # additonally It should also be helpful to know which part may need some proper planning, attension and all.

    # RULE 1 - Repeat offender
    for error_type, count in type_counts.items():
        if count >= 3:
            habit_map={
                "RUNTIME" : "You might be making assumptions about data without veryfying it first.",
                "SYNTAX" : "You might be rushing things. slow-down a bit and re-read before running.",
                "LOGICAL" : "Your planning stage needs more thought before coding and continuing first",
                "NAMEERROR" : "You're referring things before defining them or might be using wrong ones. Plan structure first.",
                "ENVIRONMENT" : "check your setup and dependencies before starting a session",
                "CONFIG" : "Missing or inocerrect configuration is a recurring blind spot."
            }

            habit =  habit_map.get(error_type, "This error type is keep appearing, Please Investigate and fix the root cause.")
            insights.append(f"[PATTERN]{error_type} appeared {count} time. {habit}")

    # RULE 2 - Fragile file
    for file_name, count in file_counts:
        if count >= 3:
            insights.append(f"[FRAGILE FILE] {file_name} produced {count} errors in this session alone. This file may have too many resposibilites/tasks or needs restructuring.")

    # RULE 3- Session trend
    if len(recent_session) >= 3 :
        current_count = recent_session [0][1]

        previous_count = [s[1] for s in recent_session [1:]]
        # recent_session [1:]: list slicing - as recent_sessions is a list of all 5 sessions, So Index [0] is the current session. [1:] means "start from index 1 and take everything after it"
        # s[1]: s[0] is the session id and s[1] is the error count - the second value. We only need the count for averaging, not the id.
        
        avg_previous =  sum (previous_count) / len(previous_count)        

        if current_count > avg_previous * 1.5:
            insights.append(f"[TREND] Error count is rising. This session had {current_count} errors vs average of {avg_previous:.1f} in recent sessions. You may be moving into complex part without enough planning - ")

        elif current_count < avg_previous * 0.5:
            insights.append(f"[TREND] Improving. This session had {current_count} errors vs average of {avg_previous:.1f}. Keep the same approach going!")

        else:
            insights.append(f"[TREND] Stable. Consistent error rate across recent sessions..")

    # RULE 4 - ERROR type dominance
    total_errors = len(errors)
    for error_type, count in type_counts.items(): # returns each key-value pair as a tuple. So each loop gives us two things at once: the error type as a string and its count as a number.
        percentage = (count/total_errors) * 100
        if percentage >= 60:
            insights.append(f"[DOMINANCE]{int(percentage)}% of your errors in this session  were {error_type}. This is your main problem area right now.")

    # Rule 5 - Clean session streak
    streak = 0
    for session in recent_session:
        if session[1] == 0 :
            streak += 1

        else:
            break

        if streak >=2 :
            insights.append(f"[STREAK] {streak} consecutive clean sessions. Good consistency.")

        elif recent_session and recent_session[0][1] == 0 :
            insights.append("[STREAK] Clean session. No errors this time.")

    return insights