"""
Display system information using Rich.
"""

import platform
import psutil
from rich.console import Console
from rich.table import Table

console = Console()

def print_system_info():
    """
    Print OS, CPU, RAM, Python version in a nice table.
    """
    table = Table(title="System Information")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("OS", f"{platform.system()} {platform.release()}")
    table.add_row("Architecture", platform.machine())
    table.add_row("CPU Cores", str(psutil.cpu_count(logical=True)))
    table.add_row("RAM", f"{psutil.virtual_memory().total / (1024**3):.2f} GB")
    table.add_row("Python Version", platform.python_version())

    console.print(table)