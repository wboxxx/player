class _Signal:
    def butter(self, *args, **kwargs):
        return []
    def sosfilt(self, sos, y):
        return y

signal = _Signal()

from . import signal as signal
