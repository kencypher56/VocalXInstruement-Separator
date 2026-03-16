"""
Export audio to MP3 files using pydub.
"""

import numpy as np
from pathlib import Path
from pydub import AudioSegment
import soundfile as sf
import tempfile
import os

class Exporter:
    def __init__(self, bitrate: str = "192k"):
        self.bitrate = bitrate

    def export_audio(self, waveform: np.ndarray, sample_rate: int, output_path: Path):
        """
        Export numpy waveform to MP3 file.
        """
        # Ensure waveform is in float range [-1, 1]
        if waveform.dtype != np.float32:
            waveform = waveform.astype(np.float32)

        # Write temporary WAV file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp_wav = tmp.name

        try:
            # Write WAV (soundfile expects (samples, channels))
            sf.write(tmp_wav, waveform, sample_rate)

            # Convert to MP3 with pydub
            audio = AudioSegment.from_wav(tmp_wav)
            audio.export(output_path, format="mp3", bitrate=self.bitrate)
        finally:
            os.unlink(tmp_wav)