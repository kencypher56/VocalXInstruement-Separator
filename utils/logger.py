"""
Logging setup using Rich.
"""

import logging
from rich.logging import RichHandler
from rich.console import Console
from rich.text import Text

console = Console()

def setup_logger():
    """
    Configure logging with Rich handler for internal debug logs.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True, markup=True)]
    )
    return logging.getLogger("vocalx")

def get_logger(name):
    return logging.getLogger(name)

def cindy_log(message: str):
    """
    Print a humorous Cindy-style log message.
    """
    styled = Text()
    styled.append("[CINDY] ", style="bold bright_red")
    styled.append(message, style="italic bright_yellow")
    console.print(styled)