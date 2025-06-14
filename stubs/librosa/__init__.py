import sys
import types


class _Beat:
    def beat_track(self, y=None, sr=22050):
        return 0.0, []

beat = _Beat()


def load(*args, sr=None, dtype=None, mono=True, offset=0.0, duration=None):
    return [], sr or 22050


def frames_to_time(frames, sr=22050, hop_length=512):
    return [f * hop_length / sr for f in frames]

class _Feature:
    def rms(self, y=None, frame_length=2048, hop_length=512):
        length = len(y) // hop_length if y else 0
        return [[0.0] * length]

feature = _Feature()

class _Onset:
    def onset_strength(self, y=None, sr=22050, hop_length=512):
        length = len(y) // hop_length if y else 0
        return [0.0] * length

onset = _Onset()


display = types.ModuleType(__name__ + '.display')

def specshow(*args, **kwargs):
    return None


display.specshow = specshow
sys.modules[__name__ + '.display'] = display
sys.modules.setdefault('librosa.display', display)


def stft(y, n_fft=2048, hop_length=512):
    length = len(y) // hop_length if y else 0
    return [[0.0] * length]

def fft_frequencies(sr=22050, n_fft=2048):
    return [sr / n_fft * i for i in range(n_fft // 2 + 1)]

def times_like(arr, sr=22050, hop_length=512):
    return [i * hop_length / sr for i in range(len(arr))]

def yin(y, fmin=80, fmax=1000, sr=22050, frame_length=2048, hop_length=512):
    length = len(y) // hop_length if y else 0
    return [0.0] * length
