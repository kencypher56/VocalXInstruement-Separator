#!/usr/bin/env python3
"""
Interactive CLI menu for VocalxInstrument Separator.
Now includes video‑to‑audio conversion as option 3.
All file prompts support TAB completion and ~ expansion.
"""

import sys
import psutil
from pathlib import Path

from prompt_toolkit import prompt
from prompt_toolkit.completion import PathCompleter
from prompt_toolkit.shortcuts import CompleteStyle
from rich.console import Console
from rich.prompt import Confirm, Prompt
from rich import print as rprint

from core.separator import Separator
from core.converter import convert_video_to_audio, check_ffmpeg, VIDEO_EXTENSIONS, AUDIO_FORMATS
from utils.sysinfo import print_system_info
from utils.logger import cindy_log
from utils.paths import get_desktop_path

console = Console()

def show_banner():
    """Display a fancy banner."""
    banner = r"""
╔══════════════════════════════════════════╗
║   🎤 VocalxInstrument Separator 🎸       ║
║       AI-powered audio exorcist          ║
║         + Video to Audio Converter       ║
╚══════════════════════════════════════════╝
            @Kencypher
    """
    console.print(banner, style="bold magenta")
    cindy_log("Okay... so like... this thing separates vocals and converts videos... or something. I'm scared.")

def show_menu():
    """Display main menu and return choice."""
    console.print("\n[bold cyan]===============================[/]")
    console.print("[bold yellow] Main Menu[/]")
    console.print("[bold cyan]===============================[/]")
    console.print("1) Separate Audio")
    console.print("2) System Info")
    console.print("3) Convert Video to Audio")
    console.print("4) Exit")
    console.print("[bold cyan]===============================[/]")
    choice = Prompt.ask("Select an option", choices=["1", "2", "3", "4"])
    return choice

def get_recommended_stems(free_ram_gb):
    """Return the maximum stems recommended based on free RAM."""
    if free_ram_gb >= 8.0:
        return 5
    elif free_ram_gb >= 4.0:
        return 4
    else:
        return 2

def select_stems_with_memory_check():
    """
    Let user choose stem count, with memory-based recommendation.
    Returns chosen stem count (int).
    """
    available_gb = psutil.virtual_memory().available / (1024**3)
    cindy_log(f"Your system has {available_gb:.1f} GB RAM free right now.")
    recommended = get_recommended_stems(available_gb)
    cindy_log(f"I'd recommend using {recommended} stems for smooth sailing.")

    while True:
        stems_str = Prompt.ask(
            "Number of stems? (2, 4, or 5)",
            choices=["2", "4", "5"],
            default=str(recommended)
        )
        stems = int(stems_str)

        # Rough memory requirements (GB)
        req = {2: 2.0, 4: 4.0, 5: 8.0}[stems]
        if available_gb < req:
            console.print(f"[yellow]Warning: {stems}‑stem separation may need ~{req} GB RAM, "
                          f"but only {available_gb:.1f} GB is free.[/]")
            proceed = Confirm.ask("Do you want to continue anyway? (may crash)", default=False)
            if not proceed:
                continue
        break
    return stems

def separate_audio_interactive():
    """Interactive flow for audio separation with robust path handling and error recovery."""
    cindy_log("Oh no... you want to separate something? Alright, give me the path...")

    completer = PathCompleter(only_directories=False, expanduser=True)

    try:
        file_path_str = prompt(
            "Enter audio file path (TAB to autocomplete): ",
            completer=completer,
            complete_style=CompleteStyle.MULTI_COLUMN,
            complete_while_typing=True
        )
    except KeyboardInterrupt:
        cindy_log("Okay, okay! No need to be rude! Returning to menu...")
        return

    raw_path = file_path_str.strip()
    # Try several interpretations of the path
    candidates = [
        Path(raw_path),                     # as typed
        Path(raw_path).expanduser(),        # expand ~
        Path(raw_path).expanduser().resolve()  # absolute
    ]

    found_path = None
    for p in candidates:
        if p.exists():
            found_path = p
            break

    if found_path is None:
        console.print("[red]File not found! Tried:[/]")
        for p in candidates:
            console.print(f"  {p}")
        cindy_log("That file doesn't exist! Did the ghost hide it? Maybe try using quotes around the path?")
        return

    path = found_path

    # Validate extension
    supported = ('.mp3', '.wav', '.flac', '.ogg')
    if path.suffix.lower() not in supported:
        console.print(f"[red]Unsupported format. Supported: {', '.join(supported)}[/]")
        cindy_log("Eww, what kind of alien format is that?")
        return

    stems = select_stems_with_memory_check()
    bitrate = Prompt.ask("MP3 bitrate (e.g., 192k, 320k)", default="192k")

    custom_output = Confirm.ask("Do you want to specify a custom output directory?", default=False)
    if custom_output:
        try:
            out_dir_str = prompt(
                "Enter output directory path (TAB to autocomplete): ",
                completer=PathCompleter(only_directories=True, expanduser=True),
                complete_style=CompleteStyle.MULTI_COLUMN,
                complete_while_typing=True
            )
        except KeyboardInterrupt:
            cindy_log("Changed your mind? Back to menu.")
            return
        out_dir = Path(out_dir_str.strip()).expanduser().resolve()
        out_dir.mkdir(parents=True, exist_ok=True)
    else:
        out_dir = None

    try:
        separator = Separator(stems=stems, bitrate=bitrate)
    except MemoryError as e:
        console.print(f"[red]{e}[/]")
        cindy_log("We don't have enough RAM! Try a lower stem count or close other apps.")
        return
    except Exception as e:
        console.print(f"[red]Failed to initialize separator: {e}[/]")
        cindy_log("The AI model refused to load! Maybe restart the app?")
        return

    if out_dir is None:
        out_dir = get_desktop_path() / path.stem

    try:
        separator.process_file(path, out_dir)
        cindy_log(f"Phew! It worked! Files saved in: {out_dir}")
    except KeyboardInterrupt:
        cindy_log("Okay, okay! I'm stopping! Don't yell at me!")
        console.print("[yellow]Separation interrupted by user.[/]")
        return
    except MemoryError:
        console.print("[red]Out of memory during separation! Try a lower stem count.[/]")
        cindy_log("The ghost ate all the RAM!")
    except Exception as e:
        console.print(f"[red]Error during separation: {e}[/]")
        cindy_log("Something went wrong! The ghost must have messed with the code!")

def convert_video_interactive():
    """Interactive flow for video to audio conversion."""
    cindy_log("Alright, let's turn a video into audio. Spooky transformation!")

    # Check ffmpeg first
    if not check_ffmpeg():
        console.print("[red]FFmpeg is not installed! Please install it:[/]")
        console.print("  - Linux: sudo apt install ffmpeg")
        console.print("  - macOS: brew install ffmpeg")
        console.print("  - Windows: download from https://ffmpeg.org/download.html")
        cindy_log("Can't convert without ffmpeg. Come back later!")
        return

    completer = PathCompleter(only_directories=False, expanduser=True)
    try:
        file_path_str = prompt(
            "Enter video file path (TAB to autocomplete): ",
            completer=completer,
            complete_style=CompleteStyle.MULTI_COLUMN,
            complete_while_typing=True
        )
    except KeyboardInterrupt:
        cindy_log("Okay, okay! No video today. Back to menu.")
        return

    raw_path = file_path_str.strip()
    # Try multiple interpretations
    candidates = [
        Path(raw_path),
        Path(raw_path).expanduser(),
        Path(raw_path).expanduser().resolve()
    ]

    found_path = None
    for p in candidates:
        if p.exists():
            found_path = p
            break

    if found_path is None:
        console.print("[red]File not found! Tried:[/]")
        for p in candidates:
            console.print(f"  {p}")
        cindy_log("That video doesn't exist! Did the ghost hide it?")
        return

    path = found_path

    if path.suffix.lower() not in VIDEO_EXTENSIONS:
        console.print(f"[red]Unsupported video format. Supported: {', '.join(VIDEO_EXTENSIONS)}[/]")
        cindy_log("That's not a video I recognize!")
        return

    # Choose output audio format
    format_choice = Prompt.ask(
        "Choose output audio format",
        choices=["mp3", "wav", "flac"],
        default="mp3"
    )
    output_format = '.' + format_choice

    # Bitrate (only relevant for mp3)
    bitrate = None
    if output_format == '.mp3':
        bitrate = Prompt.ask("MP3 bitrate (e.g., 192k, 320k)", default="192k")
        if bitrate.isdigit():
            bitrate = bitrate + 'k'
    elif output_format == '.flac':
        cindy_log("FLAC is lossless – bitrate is not applicable.")
    elif output_format == '.wav':
        cindy_log("WAV is uncompressed – bitrate is not applicable.")

    # Output directory (with tab completion)
    custom_output = Confirm.ask("Do you want to specify an output directory?", default=False)
    if custom_output:
        try:
            out_dir_str = prompt(
                "Enter output directory path (TAB to autocomplete): ",
                completer=PathCompleter(only_directories=True, expanduser=True),
                complete_style=CompleteStyle.MULTI_COLUMN,
                complete_while_typing=True
            )
        except KeyboardInterrupt:
            cindy_log("Changed your mind? Back to menu.")
            return
        out_dir = Path(out_dir_str.strip()).expanduser().resolve()
        out_dir.mkdir(parents=True, exist_ok=True)
    else:
        out_dir = None

    # Perform conversion
    try:
        convert_video_to_audio(path, output_format, bitrate, out_dir)
    except KeyboardInterrupt:
        cindy_log("Conversion interrupted! Returning to menu.")
    except Exception as e:
        console.print(f"[red]Conversion failed: {e}[/]")
        cindy_log("Oh no! The video fought back!")

def main():
    try:
        show_banner()
        while True:
            choice = show_menu()
            if choice == "1":
                separate_audio_interactive()
            elif choice == "2":
                cindy_log("Let's see what this computer is hiding...")
                print_system_info()
            elif choice == "3":
                convert_video_interactive()
            elif choice == "4":
                cindy_log("Okay I'm leaving... this is too scary.")
                console.print("[bold red]Goodbye.[/]")
                sys.exit(0)
    except KeyboardInterrupt:
        cindy_log("Fine, fine! I'm going! Don't shout!")
        console.print("[bold red]Exiting...[/]")
        sys.exit(0)

if __name__ == "__main__":
    main()