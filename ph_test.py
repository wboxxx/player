import importlib, sys, os
import time

# Chargement des stubs manuellement
from stubs import numpy_stub as np
from stubs import librosa
from stubs import scipy
from stubs import soundfile as sf
import types

sys.modules['numpy'] = np
sys.modules['numpy.linalg'] = np.linalg
sys.modules['librosa'] = librosa
sys.modules['librosa.display'] = types.ModuleType('librosa.display')
sys.modules['scipy'] = scipy
scipy_signal = types.ModuleType('scipy.signal')
scipy_signal.find_peaks = lambda *a, **k: ([], {})
scipy_signal.butter = lambda *a, **k: []
scipy_signal.sosfilt = lambda sos, y: y
sys.modules['scipy.signal'] = scipy_signal
sys.modules['soundfile'] = sf

mpl = types.ModuleType('matplotlib')
pyplot = types.ModuleType('matplotlib.pyplot')
pyplot.plot = lambda *a, **k: None
pyplot.subplots = lambda *a, **k: (None, None)
sys.modules['matplotlib'] = mpl
sys.modules['matplotlib.pyplot'] = pyplot
sys.modules['matplotlib.patches'] = types.ModuleType('matplotlib.patches')
sys.modules['matplotlib.gridspec'] = types.ModuleType('matplotlib.gridspec')
sys.modules['matplotlib.animation'] = types.ModuleType('matplotlib.animation')
sys.modules['pygame'] = types.ModuleType('pygame')
pygame_mixer = types.ModuleType('pygame.mixer')
pygame_mixer.get_init = lambda: False
pygame_mixer.quit = lambda: None
pygame_mixer.music = type('music', (), {'stop': lambda: None, 'load': lambda x: None})()
sys.modules['pygame.mixer'] = pygame_mixer
sys.modules['pydub'] = types.ModuleType('pydub')
sys.modules['pydub'].AudioSegment = type('AudioSegment', (), {'from_file': lambda *a, **k: None})

# Désactive forçage des vraies libs
os.environ['PLAYER_USE_REAL_LIBS'] = '0'

# Import du player
import player

# Active uniquement le debug playhead
player.DEBUG_FLAGS["PH"] = True
player.DEBUG_FLAGS["BRINT"] = False

# Canvas factice pour test de dessin
class DummyCanvas:
    def winfo_width(self): return 300
    def delete(self, *args, **kwargs): pass
    def create_line(self, *args, **kwargs):
        print("🎯 create_line", args)
        return 1
    def coords(self, *args): pass
    def tag_raise(self, *args): pass

# Root factice pour gestion du .after
class DummyRoot:
    def after(self, delay, callback):
        print(f"⏱ after({delay}) (non exécuté)")

# DummyPlayer avec uniquement les attributs nécessaires
class DummyPlayer(player.VideoPlayer):
    def __init__(self):
        self.timeline = DummyCanvas()
        self.root = DummyRoot()
        self.player = type("P", (), {
            "get_length": lambda self: 10000,
            "is_playing": lambda self: True,
            "get_time": lambda self: 0,
        })()
        self.duration = 10000  # 10 secondes
        self.cached_width = 300
        self.last_width_update = time.time()
        self.loop_start = 0
        self.loop_end = 10000
        self.loop_zoom_ratio = 1.0
        self._last_playhead_x = None
        self._draw_count_same_x = 0
        self.playhead_id = None
        self.needs_refresh = False
        self.playhead_anim_id = None
        self.draw_count = 0
        self.update_count = 0
        self.last_stat_time = time.time()
        self.GlobApos = 0
        self.time_sec_to_canvas_x = lambda t: int(t / 10)  # simple mapping
        self.scroll_zoom_with_playhead = lambda ms: None
        self.get_zoom_context = lambda: {"zoom_start": 0, "zoom_range": 10}
        self._update_ph_canvas = lambda x: None
        self.refresh_static_timeline_elements = lambda: None

# Exécution du test
vp = DummyPlayer()
for ms in range(0, 1000, 100):
    vp.update_playhead_by_time(ms)