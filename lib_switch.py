import os
import sys

USE_REAL_LIBS = os.environ.get('PLAYER_USE_REAL_LIBS') == '1'

if USE_REAL_LIBS:
    import numpy as np
    import librosa
    import scipy
    import soundfile as sf
else:
    from stubs import numpy_stub as np
    from stubs import librosa
    from stubs import scipy
    from stubs import soundfile as sf

# Expose modules via sys.modules so regular imports work
sys.modules.setdefault('numpy', np)
sys.modules.setdefault('librosa', librosa)
sys.modules.setdefault('scipy', scipy)
sys.modules.setdefault('scipy.signal', scipy.signal)
sys.modules.setdefault('soundfile', sf)

# Convenience alias remains 'sf'

# numpy compatibility
if not hasattr(np, 'complex'):
    np.complex = complex
