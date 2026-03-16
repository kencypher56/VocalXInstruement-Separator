"""
Core separation logic using Spleeter.
Handles separation, stem combination, and residual calculation.
Includes memory check, CUDA fallback, and automatic model caching in pretrained_models/.
"""

import os
import logging
import warnings
import psutil
from pathlib import Path
import numpy as np
from spleeter.separator import Separator as SpleeterSeparator
from spleeter.audio.adapter import AudioAdapter
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

from core.processor import resample_if_needed
from core.exporter import Exporter
from utils.logger import get_logger, cindy_log

# ---------- CUDA / CPU configuration (already set in run.py, but repeat for safety) ----------
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
logging.getLogger("tensorflow").setLevel(logging.ERROR)
logging.getLogger("spleeter").setLevel(logging.ERROR)

# Filter out any remaining CUDA warnings
warnings.filterwarnings("ignore", message=".*CUDA_ERROR_NO_DEVICE.*")
warnings.filterwarnings("ignore", message=".*failed call to cuInit.*")

logger = get_logger(__name__)

# Approximate memory requirements for each stem model (in GB)
STEM_MEMORY_REQUIREMENTS = {
    2: 2.0,
    4: 4.0,
    5: 8.0
}

def check_memory(stems: int) -> bool:
    """Check if available memory is sufficient for the chosen stem count."""
    available_gb = psutil.virtual_memory().available / (1024**3)
    required_gb = STEM_MEMORY_REQUIREMENTS.get(stems, 8.0)
    if available_gb < required_gb:
        cindy_log(f"Uh‑oh! This system only has {available_gb:.1f} GB RAM free, "
                  f"but the {stems}‑stem model needs about {required_gb} GB.")
        return False
    return True

class Separator:
    def __init__(self, stems: int = 5, bitrate: str = "192k"):
        self.stems = stems
        # Normalize bitrate
        if bitrate.isdigit():
            bitrate = bitrate + "k"
        self.bitrate = bitrate

        # Check memory before loading model
        if not check_memory(stems):
            raise MemoryError(f"Insufficient memory for {stems}‑stem separation.")

        # Set model directory to 'pretrained_models' in project root
        project_root = Path(__file__).parent.parent
        self.model_dir = project_root / "pretrained_models"
        self.model_dir.mkdir(exist_ok=True)
        os.environ['SPLEETER_CACHE'] = str(self.model_dir)

        self.model = f"spleeter:{stems}stems"
        self.audio_adapter = AudioAdapter.default()

        # Cindy logs for model loading
        cindy_log("Checking for pre‑trained model... 🧟")
        if self._model_exists_locally():
            cindy_log("Model found locally! Loading it now... 🔮")
        else:
            cindy_log("No local model found. Downloading... this may take a few minutes. ☠️")

        # Load separator (downloads if needed)
        self.separator = SpleeterSeparator(self.model, multiprocess=False)  # CPU only

        cindy_log("Model loaded successfully! The AI is ready to exorcise audio. 👻")
        self.exporter = Exporter(bitrate)

    def _model_exists_locally(self) -> bool:
        """Check if the required stem model already exists in pretrained_models/."""
        model_subdir = self.model_dir / f"{self.stems}stems"
        return model_subdir.exists() and any(model_subdir.iterdir())

    def process_file(self, input_path: Path, output_dir: Path):
        """
        Separate a single audio file and export results to output_dir.
        """
        cindy_log(f"Loading {input_path.name}... I hope it's not haunted. 🎃")

        try:
            waveform, sample_rate = self.audio_adapter.load(str(input_path), sample_rate=44100)
        except Exception as e:
            cindy_log("The audio file is cursed! Can't load it.")
            logger.error(f"Failed to load {input_path}: {e}")
            raise

        if sample_rate != 44100:
            cindy_log("Wait... the sample rate is weird. Let me fix that...")
            waveform = resample_if_needed(waveform, sample_rate, 44100)
            sample_rate = 44100

        cindy_log("Analyzing audio... it's like looking for ghosts in the waveforms. 👀")

        # Perform separation with progress and interrupt handling
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            transient=True,
        ) as progress:
            task = progress.add_task("Separating stems...", total=1)
            try:
                prediction = self.separator.separate(waveform)
            except KeyboardInterrupt:
                cindy_log("Yikes! You stopped the spell! Returning to menu...")
                raise  # Re-raise to be caught in interactive.py
            except Exception as e:
                cindy_log("The separation spell failed! Maybe too many ghosts?")
                logger.error(f"Separation failed: {e}")
                raise
            progress.update(task, completed=1)

        cindy_log("Whoa! It separated the vocals! The singer's ghost is free! 🎤👻")

        # Prepare output files
        output_dir.mkdir(parents=True, exist_ok=True)

        # Build stems list
        vocal_stem = 'vocals'
        if vocal_stem not in prediction:
            vocal_stem = [k for k in prediction if 'vocals' in k][0]

        # Sum non-vocal stems
        non_vocal = [prediction[k] for k in prediction if k != vocal_stem]
        if non_vocal:
            instruments = np.sum(non_vocal, axis=0)
        else:
            instruments = np.zeros_like(prediction[vocal_stem])

        cindy_log("The instruments are running away into another file! 🎸💨")

        background = waveform - prediction[vocal_stem] - instruments

        # Export stems
        cindy_log("OH MY GOD it worked... exporting files now... 📀")
        try:
            self.exporter.export_audio(prediction[vocal_stem], sample_rate, output_dir / "vocals.mp3")
            self.exporter.export_audio(instruments, sample_rate, output_dir / "instruments.mp3")
            self.exporter.export_audio(background, sample_rate, output_dir / "background.mp3")
        except KeyboardInterrupt:
            cindy_log("Interrupted during export! Partial files may remain.")
            raise

        logger.info(f"Exported to {output_dir}")
        cindy_log(f"Done! Files saved in: {output_dir} Go haunt your neighbors! 🧛")