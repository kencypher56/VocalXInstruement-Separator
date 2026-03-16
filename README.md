---

# 🎤 VocalxInstrument Separator 🎸

**AI-powered audio exorcist** – separate vocals, instruments, and background from any song, and convert videos to audio, all on CPU.
Built with fun **Cindy-style logs** and a hacker-terminal vibe.

---

## ✨ Features

* 🎵 **Source separation** – extract `vocals`, `instruments`, `background` from `.mp3`, `.wav`, `.flac`, `.ogg`
* 🥁 **Choose stem count** – 2, 4, or 5 stems (more stems = finer separation)
* 💾 **Automatic model caching** – downloads pretrained models into `pretrained_models/`
* 🎬 **Video to audio converter** – convert `.mp4`, `.mkv`, `.avi` to `.mp3`, `.wav`, `.flac`
* 🧠 **Smart memory check** – recommends best stem count based on free RAM
* 🖥️ **Tab completion** – for all file/folder prompts
* 🌈 **Rich terminal UI** – progress bars, spinners, and Cindy’s narration
* 🌍 **Cross-platform** – Linux, macOS, Windows (CPU only)
* ⚡ **Two interfaces** – interactive menu or CLI commands

---

## 🧩 What is a Stem?

* 🎤 **2 stems** – vocals + accompaniment
* 🥁 **4 stems** – vocals + drums + bass + other
* 🎹 **5 stems** – adds piano to the 4-stem set

The tool combines all non-vocal stems into **instruments** and computes **background** as the remainder.

---

## 📦 Models

Uses **Spleeter** pretrained models by Deezer. Automatically downloaded to:

```
pretrained_models/
├── 2stems/
├── 4stems/
└── 5stems/
```

No manual download required.

---

## 🛠️ Tech Stack

* 🔹 **Spleeter** – separation engine
* 🔹 **Librosa** – audio analysis
* 🔹 **PyDub** – MP3 export & video conversion (requires ffmpeg)
* 🔹 **Typer** – CLI interface
* 🔹 **Rich** – terminal formatting
* 🔹 **Prompt Toolkit** – tab completion
* 🔹 **NumPy / SciPy** – numerical operations
* 🔹 **Psutil** – memory checks

---

## 📁 Project Structure

```
vocalxinstrument-separator/
│
├── run.py             # main launcher
├── cli.py             # CLI commands
├── interactive.py     # interactive menu (Cindy style)
├── setup.py           # environment setup
├── requirements.txt   # Python dependencies
├── README.md
│
├── core/
│   ├── separator.py
│   ├── converter.py
│   ├── processor.py
│   └── exporter.py
│
├── utils/
│   ├── logger.py
│   ├── paths.py
│   ├── sysinfo.py
│   └── progress.py
│
└── pretrained_models/ # Spleeter models (auto-download)
```

---

## 🚀 Installation

### 🔹 Automatic Setup (Recommended)


python setup.py
```

* 1️⃣ Python venv – creates `.venv` folder
* 2️⃣ Conda – creates `vocalx` environment (Python 3.9)

Installs dependencies and checks **ffmpeg** (required for MP3 export & video conversion).

### 🔹 Manual Setup (Experts)


# venv
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# conda
conda create -n vocalx python=3.9
conda activate vocalx
pip install -r requirements.txt
```

---

## 🎮 Usage

### 🖱 Interactive Menu


python run.py


1) Separate Audio
2) System Info
3) Convert Video to Audio
4) Exit
```

* **Tab completion** works everywhere for files/folders

### 💻 CLI Commands


python run.py separate <input> [--stems 5] [--bitrate 192k] [--output DIR]
python run.py batch <folder> [--stems 5] [--bitrate 192k]
python run.py info


* `separate` – single file
* `batch` – all audio files in folder
* `info` – system info

---

## 🔄 Video to Audio

* Converts `.mp4`, `.mkv`, `.avi`, `.mov`, `.wmv`, `.flv`, `.webm`, `.m4v`
* Choose **audio format** and **bitrate**
* Output file keeps the original video name with new extension

---

## 🧪 System Requirements

* 🐍 Python 3.8 – 3.10 (3.9 recommended)
* 🧠 RAM – 2 GB min (2 stems), 8 GB+ recommended (5 stems)
* 💻 CPU – any (CPU only)
* 💾 Disk – ~500 MB for models
* 🎛 ffmpeg – required for audio export & video conversion

---

## 🐛 Troubleshooting

| Problem                   | Solution                                                   |
| ------------------------- | ---------------------------------------------------------- |
| `CUDA_ERROR_NO_DEVICE`    | Ignored – CPU mode enforced. Use `CUDA_VISIBLE_DEVICES=-1` |
| File not found            | Remove quotes; tab completion handles spaces               |
| Out of memory             | Reduce stem count or close other apps                      |
| Model downloads every run | Ensure `pretrained_models/` exists and writable            |
| ffmpeg errors             | Install ffmpeg and ensure it’s in PATH                     |

---

## 📄 License

MIT License – Spleeter models licensed by Deezer

---

## 👻 Acknowledgements

* Deezer Research – Spleeter
* Rich, Typer, Prompt Toolkit – CLI
* Cindy from Scary Movie – immortal inspiration

---

**Go separate some ghosts – I mean audio!** 👻🎶

---

