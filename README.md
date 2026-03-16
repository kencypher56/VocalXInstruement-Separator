# 🎤 VocalxInstrument Separator 🎸

**The AI-powered audio exorcist.** Separate vocals, instruments, and background elements from any song, or convert video to audio—all on your CPU. Featuring spooky "Cindy-style" logs and a high-end hacker terminal aesthetic.

---

## ✨ Features

* 🎵 **Source Separation** – Extract `vocals`, `instruments`, and `background` from `.mp3`, `.wav`, `.flac`, and `.ogg`.
* 🥁 **Variable Stem Counts** – Choose between 2, 4, or 5 stems for surgical precision.
* 💾 **Automatic Model Caching** – Pretrained models download automatically to `pretrained_models/`.
* 🎬 **Video-to-Audio** – Convert `.mp4`, `.mkv`, `.avi`, and more to high-quality audio.
* 🧠 **Smart RAM Guard** – Automatically recommends the best stem count based on your available hardware.
* 🖥️ **Tab Completion** – Full filesystem autocomplete for all file and folder prompts.
* 🌈 **Rich Terminal UI** – Narrative logs, progress bars, and spinners powered by `Rich`.

---

## 🧩 What is a Stem?

In audio engineering, a **stem** is an isolated component of a mix. This tool offers three levels of "exorcism":

| Mode | Output Components |
| :--- | :--- |
| **2 Stems** | Vocals + Accompaniment |
| **4 Stems** | Vocals + Drums + Bass + Other |
| **5 Stems** | Vocals + Drums + Bass + Piano + Other |

> [!NOTE]
> The tool intelligently combines non-vocal stems into a master **Instruments** track and calculates the **Background** noise floor by subtracting vocals and instruments from the original source.

---

## 📦 Tech Stack

* **Engine:** [Spleeter](https://github.com/deezer/spleeter) (by Deezer)
* **Audio Processing:** [Librosa](https://librosa.org/), [PyDub](https://github.com/jiaaro/pydub), [NumPy](https://numpy.org/), [SciPy](https://scipy.org/)
* **Interface:** [Typer](https://typer.tiangolo.com/), [Rich](https://rich.readthedocs.io/), [Prompt Toolkit](https://python-prompt-toolkit.readthedocs.io/)
* **System:** [Psutil](https://psutil.readthedocs.io/)

---

## 📁 Project Structure

vocalxinstrument-separator/
├── run.py              # Main launcher (auto-activates environment)
├── cli.py              # Typer CLI command definitions
├── interactive.py      # Interactive Cindy-style menu
├── setup.py            # Env setup (Venv / Conda)
├── requirements.txt    # Dependency list
├── core/               # Separation & conversion logic
│   ├── separator.py    # Spleeter implementation
│   └── converter.py    # Video → Audio logic
└── utils/              # UI & System helpers
    ├── logger.py       # "Cindy" themed logging
    └── sysinfo.py      # Hardware monitoring

🚀 Installation
Option 1: Automatic Setup (Recommended)

The setup script handles environment creation and checks for ffmpeg.


python setup.py

You will be prompted to choose:

    Python venv: Creates a local .venv folder.

    Conda: Creates a vocalx environment (Miniconda installer included for Linux/macOS).

Option 2: Manual Installation


# Create environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

🎮 Usage
Interactive Mode

Launch the main menu for a guided experience with full tab-completion:
Bash

python run.py

CLI Mode

Perform quick actions directly from your terminal:
Bash

# Example command 
python cli.py separate "path/to/song.mp3" --stems 5

🎬 Video to Audio

Supported inputs: .mp4, .mkv, .avi, .mov, .wmv, .flv, .webm, .m4v.
Choose your output format (.mp3, .wav, or .flac) and bitrate directly from the menu.
📄 License

This project is licensed under the MIT License.
Spleeter models are provided by Deezer under their respective license.
👻 Acknowledgements

    Deezer Research for the Spleeter library.

    The Scary Movie Franchise for Cindy’s legendary lines.

    FFmpeg for the heavy lifting in media conversion.