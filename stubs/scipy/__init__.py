class _Signal:
    def butter(self, *args, **kwargs):
        return []
    def sosfilt(self, sos, y):
        return y
    def find_peaks(self, x, height=None, distance=None):
        return [], {}

signal = _Signal()

from . import signal as signal
