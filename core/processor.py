"""
Audio processing utilities: resampling, normalization, etc.
"""

import numpy as np
import librosa

def resample_if_needed(waveform: np.ndarray, orig_sr: int, target_sr: int) -> np.ndarray:
    """
    Resample audio waveform to target sample rate.
    Handles both mono and stereo.
    """
    if orig_sr == target_sr:
        return waveform

    # librosa.resample expects shape (channels, samples) or (samples,)
    # Spleeter returns (samples, channels) typically.
    # We'll transpose if needed.
    if waveform.ndim == 2:
        # Assume (samples, channels) -> convert to (channels, samples)
        waveform = waveform.T

    resampled = librosa.resample(waveform, orig_sr=orig_sr, target_sr=target_sr, axis=-1)

    # Convert back to (samples, channels)
    if resampled.ndim == 2:
        resampled = resampled.T
    return resampled