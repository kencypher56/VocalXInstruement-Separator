"""
Cross-platform path utilities.
"""

from pathlib import Path
import os

def get_desktop_path() -> Path:
    """
    Return the path to the user's Desktop folder.
    """
    home = Path.home()
    if os.name == 'nt':  # Windows
        return home / 'Desktop'
    else:  # Linux, macOS
        return home / 'Desktop'