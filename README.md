# 🎤 VocalxInstrument Separator 🎸

**AI-powered audio exorcist** – separate vocals, instruments, and background from any song, and convert videos to audio, all on CPU. Built with spooky Cindy-style logs and hacker-terminal vibes.



## ✨ Features

- 🎵 **Source separation** – extract `vocals`, `instruments`, `background` from `.mp3`, `.wav`, `.flac`, `.ogg`
- 🥁 **Choose stem count** – 2, 4, or 5 stems (more stems = finer separation)
- 💾 **Automatic model caching** – downloads pretrained models into `pretrained_models/`
- 🎬 **Video to audio converter** – convert `.mp4`, `.mkv`, `.avi` … to `.mp3`, `.wav`, `.flac`
- 🧠 **Smart memory check** – recommends best stem count based on free RAM
- 🖥️ **Tab completion** – for all file/folder prompts
- 🌈 **Rich terminal UI** – progress bars, spinners, and Cindy’s narration
- 🌍 **Cross-platform** – Linux, macOS, Windows (CPU only)
- ⚡ **Two interfaces** – interactive menu or CLI commands



## 🧩 What is a Stem?

In audio processing, a **stem** is an isolated component of a mix.

- 🎤 **2 stems** – vocals + accompaniment
- 🥁 **4 stems** – vocals + drums + bass + other
- 🎹 **5 stems** – adds piano to the 4‑stem set

The tool combines all non‑vocal stems into one **instruments** track and computes the **background** as the original minus vocals minus instruments.



## 📦 Models

We use **Spleeter** pretrained models by Deezer. The models are downloaded automatically on first use and stored in:
pretrained_models/
├── 2stems/
├── 4stems/
└── 5stems/

No manual download required – the tool handles everything.



## 🛠️ Tech Stack

- **[Spleeter](https://github.com/deezer/spleeter)** – separation engine
- **[Librosa](https://librosa.org/)** – audio analysis
- **[PyDub](https://github.com/jiaaro/pydub)** – MP3 export & video conversion (requires ffmpeg)
- **[Typer](https://typer.tiangolo.com/)** – CLI interface
- **[Rich](https://rich.readthedocs.io/)** – beautiful terminal formatting
- **[Prompt Toolkit](https://python-prompt-toolkit.readthedocs.io/)** – tab completion
- **[NumPy](https://numpy.org/)** / **[SciPy](https://scipy.org/)** – numerical heavy lifting
- **[Psutil](https://psutil.readthedocs.io/)** – memory checks



## 📁 Project Structure
vocalxinstrument-separator/
│
├── run.py # main launcher (auto‑activates env)
├── cli.py # Typer CLI commands
├── interactive.py # interactive menu (Cindy style)
├── setup.py # environment setup (venv / conda)
├── requirements.txt # Python dependencies
├── README.md # this file
│
├── core/ # core modules
│ ├── separator.py # separation logic
│ ├── converter.py # video → audio
│ ├── processor.py # audio resampling
│ └── exporter.py # MP3 export
│
├── utils/ # helper modules
│ ├── logger.py # Cindy logs
│ ├── paths.py # cross‑platform desktop path
│ ├── sysinfo.py # system info display
│ └── progress.py # progress bar utilities
│
├── pretrained_models/ # downloaded Spleeter models (created automatically)


## 🚀 Installation

### Option 1: Automatic setup (recommended)

Run the setup script and choose your preferred environment manager:


python setup.py
    1) Python venv – creates a local .venv folder

    2) Conda – creates a vocalx environment with Python 3.9

If you choose Conda and it’s not installed, the script offers to download and install Miniconda automatically (Linux/macOS). After installation, it creates the environment and installs all dependencies.

The script also checks for ffmpeg (required for MP3 export & video conversion) and gives installation hints if missing.
Option 2: Manual installation (experts)

Create a virtual environment and install dependencies:
# using venv
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -r requirements.txt

# using conda
conda create -n vocalx python=3.9
conda activate vocalx
pip install -r requirements.txt
🎮 Usage
Interactive Menu

Just run:
python run.py
1) Separate Audio
2) System Info
3) Convert Video to Audio
4) Exit
Follow the prompts – tab completion works everywhere you enter a file/folder path.
🔄 Video to Audio Conversion

Option 3 in the interactive menu converts any common video format to audio.
You can choose output format and bitrate (for MP3).
The output file keeps the original video name with the new extension.

Supported video inputs: .mp4, .mkv, .avi, .mov, .wmv, .flv, .webm, .m4v

📄 License

This project is licensed under the MIT License.
Spleeter models are provided by Deezer under their own license.
👻 Acknowledgements

    Deezer Research for the amazing Spleeter library

    Rich, Typer, and Prompt Toolkit for making the CLI so pleasant

    The Scary Movie franchise for Cindy’s immortal lines