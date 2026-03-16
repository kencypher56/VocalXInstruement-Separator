#!/usr/bin/env python3
"""
Main CLI interface using Typer.
"""

import typer
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.table import Table

from core.separator import Separator
from utils.logger import setup_logger
from utils.sysinfo import print_system_info
from utils.paths import get_desktop_path

app = typer.Typer(name="vocalx", help="AI-powered audio source separation tool")
console = Console()
logger = setup_logger()

@app.command()
def separate(
    input_path: str = typer.Argument(..., help="Path to audio file or folder"),
    stems: int = typer.Option(5, "--stems", "-s", help="Number of stems: 2, 4, or 5", min=2, max=5),
    bitrate: str = typer.Option("192k", "--bitrate", "-b", help="Output MP3 bitrate"),
    output_dir: Optional[Path] = typer.Option(None, "--output", "-o", help="Custom output directory (default: Desktop/<filename>)"),
):
    """
    Separate an audio file or all files in a folder.
    """
    logger.info(f"Starting separation with {stems} stems, bitrate {bitrate}")

    input_path = Path(input_path)
    if not input_path.exists():
        logger.error(f"Input path does not exist: {input_path}")
        raise typer.Exit(code=1)

    separator = Separator(stems=stems, bitrate=bitrate)

    if input_path.is_file():
        # Single file
        logger.info(f"Processing single file: {input_path.name}")
        if output_dir is None:
            output_dir = get_desktop_path() / input_path.stem
        separator.process_file(input_path, output_dir)
    else:
        # Batch mode: process all supported audio files in folder
        logger.info(f"Batch processing folder: {input_path}")
        supported_ext = ('.mp3', '.wav', '.flac', '.ogg')
        files = [f for f in input_path.iterdir() if f.suffix.lower() in supported_ext]
        if not files:
            logger.error(f"No supported audio files found in {input_path}")
            raise typer.Exit(code=1)

        for file in files:
            logger.info(f"Processing: {file.name}")
            if output_dir is None:
                out_dir = get_desktop_path() / file.stem
            else:
                out_dir = output_dir / file.stem
            separator.process_file(file, out_dir)

    logger.info("All tasks completed.")

@app.command()
def info():
    """
    Display system information.
    """
    print_system_info()

@app.command()
def batch(
    folder: str = typer.Argument(..., help="Folder containing audio files"),
    stems: int = typer.Option(5, "--stems", "-s", help="Number of stems: 2, 4, or 5"),
    bitrate: str = typer.Option("192k", "--bitrate", "-b", help="Output MP3 bitrate"),
):
    """
    Batch process all audio files in a folder.
    (Alias for 'separate' with a folder)
    """
    separate(folder, stems, bitrate)

if __name__ == "__main__":
    app()