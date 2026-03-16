"""
Progress tracking utilities (wrapper around Rich progress).
"""

from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TaskProgressColumn,
    TimeRemainingColumn,
)

def track_task(description: str, total: float = 1.0):
    """
    Create a progress bar context manager.
    Usage:
        with track_task("Processing...") as progress:
            task = progress.add_task("Task", total=100)
            # do work
            progress.update(task, advance=50)
    """
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TimeRemainingColumn(),
    )