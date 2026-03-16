🎤 VocalxInstrument Separator 🎸

AI-powered audio exorcist – separate vocals, instruments, and background from any song, and convert videos to audio, all on CPU.
Built with spooky Cindy-style logs and hacker-terminal vibes.

✨ Features

🎵 Source separation – extract vocals, instruments, background from mp3, wav, flac, ogg
🥁 Choose stem count – 2, 4, or 5 stems (more stems = finer separation)
💾 Automatic model caching – downloads pretrained models into pretrained_models/
🎬 Video to audio converter – convert mp4, mkv, avi to mp3, wav, flac
🧠 Smart memory check – recommends best stem count based on free RAM
🖥️ Tab completion – for all file/folder prompts
🌈 Rich terminal UI – progress bars, spinners, and Cindy’s narration
🌍 Cross-platform – Linux, macOS, Windows (CPU only)
⚡ Two interfaces – interactive menu or CLI commands

🧩 What is a Stem?

🎤 2 stems – vocals + accompaniment
🥁 4 stems – vocals + drums + bass + other
🎹 5 stems – adds piano to the 4-stem set

The tool combines all non-vocal stems into instruments and computes background as the remainder.

📦 Models

Uses Spleeter pretrained models by Deezer. Automatically downloaded to:

pretrained_models/
2stems/
4stems/
5stems/

No manual download required.

🛠️ Tech Stack

Spleeter – separation engine
Librosa – audio analysis
PyDub – MP3 export & video conversion (requires ffmpeg)
Typer – CLI interface
Rich – terminal formatting
Prompt Toolkit – tab completion
NumPy / SciPy – numerical operations
Psutil – memory checks

📁 Project Structure

vocalxinstrument-separator/
run.py – main launcher
cli.py – CLI commands
interactive.py – interactive menu (Cindy style)
setup.py – environment setup
requirements.txt – Python dependencies
README.md

core/
separator.py
converter.py
processor.py
exporter.py

utils/
logger.py
paths.py
sysinfo.py
progress.py

pretrained_models/ – Spleeter models (auto-download)

🚀 Installation

Automatic setup (recommended)

Run setup.py

Python venv – creates .venv folder
Conda – creates vocalx environment (Python 3.9)

Manual setup (experts)

Create virtual environment: python -m venv .venv
Activate environment: source .venv/bin/activate (Windows: .venv\Scripts\activate)
Install dependencies: pip install -r requirements.txt

🎮 Usage

Interactive menu – run.py

1. Separate Audio
2. System Info
3. Convert Video to Audio
4. Exit

Tab completion works for files and folders.

CLI commands

python run.py separate <input> [--stems 5] [--bitrate 192k] [--output DIR]
python run.py batch <folder> [--stems 5] [--bitrate 192k]
python run.py info

🔄 Video to Audio

Converts mp4, mkv, avi, mov, wmv, flv, webm, m4v
Choose audio format and bitrate
Output file keeps original video name with new extension

🧪 System Requirements

Python 3.8 – 3.10 (3.9 recommended)
RAM – 2 GB minimum (2 stems), 8 GB+ recommended (5 stems)
CPU – any (CPU only)
Disk – ~500 MB for models
ffmpeg – required for audio export & video conversion

🐛 Troubleshooting

CUDA_ERROR_NO_DEVICE – ignored, CPU mode enforced
File not found – remove quotes; tab completion handles spaces
Out of memory – reduce stem count or close other apps
Model downloads every run – ensure pretrained_models/ exists and is writable
ffmpeg errors – install ffmpeg and ensure it’s in PATH

📄 License

MIT License – Spleeter models licensed by Deezer

👻 Acknowledgements

Deezer Research – Spleeter
Rich, Typer, Prompt Toolkit – CLI
Cindy from Scary Movie – immortal inspiration

Go separate some ghosts – I mean audio! 👻🎶


