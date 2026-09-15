from rich.console import Console # replaces regular print, adds color support
from rich.panel import Panel # wraps output in a bordered box
from rich.table import Table # structured columns for the report
from rich import box

console = Console()

def print_banner():
    console.print(Panel.fit("[bold cyan]GHOST[/bold cyan] - Session-aware error tracker", 
    border_style="cyan"))

def print_watch_start(session_id, target):
    console.print(Panel.fit(
        f"[bold]Session ID:[/bold] [cyan]{session_id}[/cyan]\n"
        f"[bold]Watching:[/bold] [green]{' '.join(target)}[/green]",
        title="[bold cyan]GHOST WATCHING[/bold cyan]",
        border_style="cyan"
    ))

def print_error(error_type, details, traceback):
    color_map = {
        "RUNTIME": "red",
        "SYNTAX": "yellow",
        "LOGICAL": "magenta",
        "ENVIRONMENT": "blue",
        "CONFIG": "orange3",
        "UNKNOWN": "white"
    }
    color = color_map.get(error_type, "white")

    console.print(Panel(
        f"[bold]Type:[/bold] [{color}] {error_type}[/{color}]\n"
        f"[bold]Details:[/bold] {details}\n\n"
        f"[bold]Traceback:[/bold]\n[dim]{traceback}[/dim]",
        title="[bold red]GHOST CAUGHT[/bold red]",
        border_style=color
    ))

def print_insights(insights):
    if not insights:
        return
    console.print("\n[bold cyan][GHOST PATTERNS][/bold cyan]")
    for insight in insights:
        console.print(f"[cyan] >> [/cyan] {insight}")

def print_session_table(session_data):
    table = Table(box=box.SIMPLE, show_header=True, header_style="bold cyan")
    table.add_column("Session", style="dim")
    table.add_column("Started")
    table.add_column("Duration")
    table.add_column("Errors", justify="center")
    table.add_column("Top Error Type")
    table.add_column("Files")

    for row in session_data:
        table.add_row(*row)

    console.print(table)