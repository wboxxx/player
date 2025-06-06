import os
import subprocess
import tempfile
from typing import Optional, Tuple

from lib_switch import np, librosa, scipy, sf


def _util_extract_audio_segment(
    input_path: str,
    output_path: Optional[str] = None,
    *,
    start_sec: Optional[float] = None,
    duration_sec: Optional[float] = None,
    audio_codec: str = "pcm_s16le",
    sample_rate: int = 44100,
    channels: int = 1,
    overwrite: bool = True,
    use_temp_file: bool = True,
) -> Optional[str]:
    """Extract an audio segment via ffmpeg."""
    if output_path is None:
        if use_temp_file:
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                output_path = tmp.name
        else:
            raise ValueError("output_path required if use_temp_file=False")

    cmd = ["ffmpeg"]
    if overwrite:
        cmd.append("-y")
    if start_sec is not None:
        cmd += ["-ss", str(start_sec)]
    if duration_sec is not None:
        cmd += ["-t", str(duration_sec)]
    cmd += ["-i", input_path, "-vn", "-acodec", audio_codec, "-ar", str(sample_rate), "-ac", str(channels), output_path]

    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception:
        return None

    if not os.path.exists(output_path) or os.path.getsize(output_path) == 0:
        return None

    return output_path


def _util_get_tempo_and_beats_librosa(y: np.ndarray, sr: int) -> Tuple[float, np.ndarray]:
    """Return tempo and beat frames from audio using librosa."""
    if y is None or len(y) == 0:
        return 0.0, np.array([])
    try:
        tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
        return float(tempo), beats
    except Exception:
        return 0.0, np.array([])
