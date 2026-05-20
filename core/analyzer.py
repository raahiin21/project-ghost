import anthropic
import json
from core.db import get_connection

def analyze_session(session_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT error_type, message, file_name FROM errors WHERE session_id = ?",(session_id,)
    )
    errors = cursor.fetchall()
    conn.close()

    if not errors:
        return None
    
    error_list = []
    for error in errors:
        error_list.append({
            "type": error[0],
            "message": error[1],
            "file": error[2]
        })

    prompt = f"""You are a developer assistant analyzing a coding session. Here are the errors encountered during this session:
    
    {json.dumps(error_list, indent=2)}
    
    Provide a short analysis covering:
    1. What patterns you see across these errors
    2. What root cause is likely behind them
    3. One specific thing the developer should focus on improving
    
    Keep it concise, direct, and practical. Max 150 words."""
    
    client = anthropic.Anthropic()
    response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=300,
    messages=[
        {"role": "user", "content": prompt}
    ]
    )

    return response.content[0].text