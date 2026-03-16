<div align="center">

# 🎤 VocalxInstrument Separator 🎸

**The AI-powered audio exorcist.**

Surgically separate vocals, instruments, and background elements from any song — or rip audio straight from video — all on your CPU. Featuring Cindy-style narrative logs and a high-end hacker terminal aesthetic.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)
[![Powered by Spleeter](https://img.shields.io/badge/Engine-Spleeter-purple?style=flat-square)](https://github.com/deezer/spleeter)
[![FFmpeg](https://img.shields.io/badge/Media-FFmpeg-green?style=flat-square&logo=ffmpeg)](https://ffmpeg.org)

</div>

---

## 📖 Table of Contents

- [Features](#-features)
- [What Is a Stem?](#-what-is-a-stem)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Usage](#-usage)
- [Video to Audio](#-video-to-audio)
- [License](#-license)
- [Acknowledgements](#-acknowledgements)

---

## ✨ Features

| Feature | Description |
| :--- | :--- |
| 🎵 **Source Separation** | Extract `vocals`, `instruments`, and `background` from `.mp3`, `.wav`, `.flac`, and `.ogg` |
| 🥁 **Variable Stem Counts** | Choose between 2, 4, or 5 stems for surgical precision |
| 💾 **Automatic Model Caching** | Pretrained models download automatically to `pretrained_models/` |
| 🎬 **Video-to-Audio** | Convert `.mp4`, `.mkv`, `.avi`, and more to high-quality audio |
| 🧠 **Smart RAM Guard** | Recommends the optimal stem count based on available hardware |
| 🖥️ **Tab Completion** | Full filesystem autocomplete for all file and folder prompts |
| 🌈 **Rich Terminal UI** | Narrative logs, progress bars, and spinners powered by `Rich` |

---

## 🧩 What Is a Stem?

In audio engineering, a **stem** is an isolated component of a mix. This tool offers three levels of separation:

| Mode | Output Tracks |
| :---: | :--- |
| **2 Stems** | Vocals · Accompaniment |
| **4 Stems** | Vocals · Drums · Bass · Other |
| **5 Stems** | Vocals · Drums · Bass · Piano · Other |

> [!NOTE]
> Non-vocal stems are automatically combined into a master **Instruments** track. The **Background** noise floor is calculated by subtracting vocals and instruments from the original source.

---

## 📦 Tech Stack

| Layer | Libraries |
| :--- | :--- |
| **Separation Engine** | [Spleeter](https://github.com/deezer/spleeter) by Deezer |
| **Audio Processing** | [Librosa](https://librosa.org/), [PyDub](https://github.com/jiaaro/pydub), [NumPy](https://numpy.org/), [SciPy](https://scipy.org/) |
| **Terminal Interface** | [Typer](https://typer.tiangolo.com/), [Rich](https://rich.readthedocs.io/), [Prompt Toolkit](https://python-prompt-toolkit.readthedocs.io/) |
| **System Utilities** | [Psutil](https://psutil.readthedocs.io/) |
| **Media Conversion** | [FFmpeg](https://ffmpeg.org/) |

---

## 📁 Project Structure

```
vocalxinstrument-separator/
├── run.py              # Main launcher — auto-activates environment
├── cli.py              # Typer CLI command definitions
├── interactive.py      # Interactive Cindy-style menu
├── setup.py            # Environment setup (venv / Conda)
├── requirements.txt    # Dependency list
├── core/
│   ├── separator.py    # Spleeter separation logic
│   └── converter.py    # Video → Audio conversion
└── utils/
    ├── logger.py       # "Cindy" themed logging
    └── sysinfo.py      # Hardware monitoring
```

---

## 🚀 Installation

### Prerequisites

- Python 3.8+
- [FFmpeg](https://ffmpeg.org/download.html) installed and available on your `PATH`

### Option 1 — Automatic Setup (Recommended)

The setup script handles virtual environment creation and checks for FFmpeg automatically:

```bash
python setup.py
```

You'll be prompted to choose between:
- **Python venv** — creates a local `.venv` folder
- **Conda** — creates a `vocalx` environment (Miniconda installer included for Linux/macOS)

### Option 2 — Manual Installation

```bash
# 1. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate       # macOS / Linux
# .venv\Scripts\activate        # Windows

# 2. Install dependencies
pip install -r requirements.txt
```

---

## 🎮 Usage

### Interactive Mode

Launch the full guided menu with tab-completion:

```bash
python run.py
```

### CLI Mode

Run separations directly from the terminal:

```bash
# Separate a file into 5 stems
python cli.py separate "path/to/song.mp3" --stems 5

# Separate into 2 stems (fastest)
python cli.py separate "path/to/song.wav" --stems 2
```

**Available stem options:** `2`, `4`, `5`

---

## 🎬 Video to Audio

Convert video files to audio directly from the interactive menu or CLI.

**Supported input formats:** `.mp4` · `.mkv` · `.avi` · `.mov` · `.wmv` · `.flv` · `.webm` · `.m4v`

**Supported output formats:** `.mp3` · `.wav` · `.flac`

You can choose your preferred output format and bitrate from the interactive menu.

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

> Spleeter models are provided by Deezer under their respective license.

---

## 👻 Acknowledgements

- **[Deezer Research](https://github.com/deezer/spleeter)** — for the Spleeter separation engine
- **[FFmpeg](https://ffmpeg.org/)** — for the heavy lifting in media conversion
- **The *Scary Movie* franchise** — for Cindy's legendary one-liners

---

<div align="center">
  <sub>Built with 👻 and way too much caffeine</sub>
</div>

