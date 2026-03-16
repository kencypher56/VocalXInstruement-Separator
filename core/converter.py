"""
Video to audio converter using pydub (requires ffmpeg).
"""

import subprocess
from pathlib import Path

from pydub import AudioSegment
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

from utils.logger import cindy_log, get_logger

logger = get_logger(__name__)

# Supported video extensions (common ones)
VIDEO_EXTENSIONS = ('.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.m4v')
# Supported audio output formats
AUDIO_FORMATS = ('.mp3', '.wav', '.flac')

def check_ffmpeg():
    """Return True if ffmpeg is installed, else False."""
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def convert_video_to_audio(input_path: Path, output_format: str, bitrate: str = None, output_dir: Path = None):
    """
    Convert video file to audio.
    input_path: Path to video file.
    output_format: e.g., '.mp3', '.wav', '.flac'
    bitrate: e.g., '192k' (only used for mp3)
    output_dir: Directory to save output. If None, use input file's directory.
    """
    if not check_ffmpeg():
        cindy_log("FFmpeg is not installed! I can't convert without it.")
        raise RuntimeError("FFmpeg not found. Please install ffmpeg.")

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    if output_format not in AUDIO_FORMATS:
        raise ValueError(f"Unsupported output format: {output_format}")

    # Determine output directory, expanding ~ if present
    if output_dir is None:
        output_dir = input_path.parent
    else:
        # Expand user home and resolve to absolute path
        output_dir = Path(output_dir).expanduser().resolve()
        output_dir.mkdir(parents=True, exist_ok=True)

    output_filename = input_path.stem + output_format
    output_path = output_dir / output_filename

    # Load video with pydub (requires ffmpeg)
    cindy_log("Loading video... this may take a moment.")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        transient=True,
    ) as progress:
        task = progress.add_task("Converting video to audio...", total=1)

        # pydub uses ffmpeg to read video files
        audio = AudioSegment.from_file(str(input_path))

        # Export with bitrate if applicable
        export_params = {}
        if output_format == '.mp3' and bitrate:
            export_params['bitrate'] = bitrate

        audio.export(str(output_path), format=output_format[1:], **export_params)

        progress.update(task, completed=1)

    cindy_log(f"Conversion complete! Audio saved to: {output_path}")
    return output_path