#!/usr/bin/env python3
"""
Main launcher for VocalxInstrument Separator.
Sets environment variables for CPU-only mode before any imports.
If no arguments, starts interactive mode; otherwise passes to CLI.
Works with both venv and conda environments.
"""

import os
import sys
from pathlib import Path

# --- Force CPU-only mode and suppress TensorFlow logs ---
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'          # Hide all GPUs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'           # Suppress TF logs (including errors)
# -------------------------------------------------------

# Now we can import other modules
import subprocess

VENV_DIR = Path(__file__).parent / ".venv"

def main():
    # If we are inside a conda environment, skip venv checks
    if 'CONDA_PREFIX' in os.environ:
        # Just run the CLI or interactive module
        if len(sys.argv) == 1:
            import interactive
            interactive.main()
        else:
            from cli import app
            app()
        return

    # Otherwise, use the venv logic
    if not VENV_DIR.exists():
        print("❌ Virtual environment not found. Please run setup.py first:")
        print("   python setup.py")
        sys.exit(1)

    # Determine python path inside venv
    if sys.platform == "win32":
        python_path = VENV_DIR / "Scripts" / "python"
    else:
        python_path = VENV_DIR / "bin" / "python"

    if not python_path.exists():
        print("❌ Virtual environment seems corrupted. Please delete .venv and run setup.py again.")
        sys.exit(1)

    # Launch the appropriate module with the same arguments
    if len(sys.argv) == 1:
        cmd = [str(python_path), "-m", "interactive"]
    else:
        cmd = [str(python_path), "-m", "cli"] + sys.argv[1:]
    subprocess.run(cmd)

if __name__ == "__main__":
    main()