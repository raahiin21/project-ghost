from collections import Counter
from datetime import datetime
from core.db import get_connection
from rich.console import Console
from rich.panel import Panel
from rich import box
from rich.table import Table

def generate_insights():
    conn = get_connection()
    cursor =  conn.cursor()

    # getting all session with error counts
    cursor.execute("""
        SELECT s.id, s.started_at, s.ended_at, COUNT(e.id) as error_count
        FROM sessions s
        LEFT JOIN errors e ON s.id = e.session_id
        GROUP BY s.id
        ORDER BY s.id ASC
    """)
    sessions = cursor.fetchall()

    # gwtting all errors
    cursor.execute("SELECT session_id, error_type, file_name from errors")
    all_errors = cursor.fetchall()

    conn.close()

    if not sessions:
        print("No session data found")
        return

    print_insight_report(sessions, all_errors)

def print_insight_report(sessions, all_errors):

    console = Console()

    console.print(Panel.fit("[bold cyan]GHOST INSIGHTS[/bold cyan] — Developer pattern analysis",
        border_style="cyan"))

    # STREAK
    streak = 0
    for session in reversed(sessions):
        if session[3] == 0:
            streak += 1
        else:
            break

    console.print(f"\n[bold]Clean Session Streak:[/bold] [cyan]{streak}[/cyan] consecutive clean sessions")

    # Total State

    total_sessions = len(sessions)
    total_errors = len(all_errors)
    avg_errors = total_errors / total_sessions if total_sessions else 0

    console.print(f"[bold]Total Sessions:[/bold] {total_sessions}")
    console.print(f"[bold]Total Errors:[/bold] {total_errors}")
    console.print(f"[bold]Avg Errors per Session:[/bold] {avg_errors:.1f}")

    # Error type frequency bar
    if all_errors:
        console.print("\n[bold]Error Type Frequency:[/bold]\n")
        type_counts = Counter([e[1] for e in all_errors])
        max_counts = max(type_counts.values())

        for error_type, count in type_counts.most_common():
            bar_length = int((count / max_counts) * 30)
            bar = "█" * bar_length
            console.print(f" [cyan]{error_type:<12}[/cyan]{bar} {count}\n")

    # most fragile file
    if all_errors:
        file_counts = Counter([e[2] for e in all_errors])
        most_fragile = file_counts.most_common(1)[0]
        console.print(f"\n[bold]Most Fragile File:[/bold] [red]{most_fragile[0]}[/red]")

    # Trend
    if len(sessions) >= 3 :
        recent = [s[3] for s in sessions[-3:]]
        if recent[-1] > recent[0]:
            trend = "[red]Rising[/red] — error rate increasing recently"
        elif recent[-1] < recent[0]:
            trend = "[green]Improving[/green] — error rate decreasing"
        else:
            trend = "[yellow]Stable[/yellow] — consistent error rate"
        console.print(f"[bold]Trend:[/bold] {trend}")