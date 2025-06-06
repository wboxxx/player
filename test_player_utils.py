import unittest
from unittest.mock import patch, mock_open, MagicMock
from lib_switch import np, librosa, scipy, sf
import os  # For os.path.exists checks in _util_extract_audio_segment tests
import sys
import types

# Provide dummy external modules for player import
sys.modules.setdefault('vlc', MagicMock())
sys.modules.setdefault('matplotlib', types.ModuleType('matplotlib'))
sys.modules.setdefault('matplotlib.pyplot', MagicMock())
sys.modules.setdefault('matplotlib.patches', types.ModuleType('matplotlib.patches'))
sys.modules.setdefault('matplotlib.gridspec', types.ModuleType('matplotlib.gridspec'))
sys.modules.setdefault('matplotlib.animation', types.ModuleType('matplotlib.animation'))
sys.modules.setdefault('pygame', types.ModuleType('pygame'))
sys.modules.setdefault('pygame.mixer', types.ModuleType('pygame.mixer'))
sys.modules.setdefault('pydub', types.ModuleType('pydub'))
sys.modules['pydub'].AudioSegment = MagicMock()

# Assuming player.py is in the same directory or accessible via PYTHONPATH
from player import (
    format_time,
    _util_extract_audio_segment,
    _util_get_tempo_and_beats_librosa,
    extract_keyframes,
    VideoPlayer,
)
import player

class TestFormatTime(unittest.TestCase):
    def test_zero_seconds(self):
        self.assertEqual(format_time(0, include_ms=True, include_tenths=False), "0:00:00.000")
        self.assertEqual(format_time(0, include_ms=False), "0:00:00")
        self.assertEqual(format_time(0, include_ms=True, include_tenths=True), "0:00:00.0")

    def test_integer_seconds(self):
        self.assertEqual(format_time(59, include_ms=False), "0:00:59")
        self.assertEqual(format_time(60, include_ms=False), "0:01:00")
        self.assertEqual(format_time(3600, include_ms=False), "1:00:00")
        self.assertEqual(format_time(3661, include_ms=False), "1:01:01")

    def test_float_seconds(self):
        self.assertEqual(format_time(59.5, include_ms=True, include_tenths=False), "0:00:59.500")
        self.assertEqual(format_time(59.5, include_ms=True, include_tenths=True), "0:00:59.5")
        self.assertEqual(format_time(3661.5, include_ms=True, include_tenths=False), "1:01:01.500")
        self.assertEqual(format_time(3661.567, include_ms=True, include_tenths=False), "1:01:01.567")
        self.assertEqual(format_time(3661.567, include_ms=True, include_tenths=True), "1:01:01.5") # Tenths truncates/rounds based on implementation

    def test_padding(self):
        self.assertEqual(format_time(1, include_ms=False), "0:00:01")
        self.assertEqual(format_time(61, include_ms=False), "0:01:01")

    def test_include_flags(self):
        # Test cases from problem description
        self.assertEqual(format_time(0, include_ms=False, include_tenths=False), "0:00:00") # Corrected from problem, include_tenths is irrelevant if include_ms=False
        self.assertEqual(format_time(3661.5, include_ms=True, include_tenths=True), "1:01:01.5")
        self.assertEqual(format_time(3661.567, include_ms=True, include_tenths=False), "1:01:01.567")
        
        # Additional flag combinations
        self.assertEqual(format_time(12.345, include_ms=True, include_tenths=False), "0:00:12.345")
        self.assertEqual(format_time(12.345, include_ms=True, include_tenths=True), "0:00:12.3")
        self.assertEqual(format_time(12.345, include_ms=False), "0:00:12") # include_tenths is ignored
        self.assertEqual(format_time(12.987, include_ms=True, include_tenths=True), "0:00:12.9")


    def test_none_input(self):
        self.assertEqual(format_time(None, include_ms=True, include_tenths=False), "--:--:--.---")
        self.assertEqual(format_time(None, include_ms=False), "--:--:--")
        self.assertEqual(format_time(None, include_ms=True, include_tenths=True), "--:--:--.-")

    def test_negative_input(self):
        self.assertEqual(format_time(-10, include_ms=True, include_tenths=False), "--:--:--.---")
        self.assertEqual(format_time(-10, include_ms=False), "--:--:--")
        self.assertEqual(format_time(-10, include_ms=True, include_tenths=True), "--:--:--.-")

class TestUtilExtractAudio(unittest.TestCase):

    @patch('player.subprocess.run')
    @patch('player.os.path.exists')
    @patch('player.os.path.getsize')
    @patch('player.tempfile.NamedTemporaryFile')
    def test_ffmpeg_command_construction_defaults(self, mock_tempfile, mock_getsize, mock_exists, mock_run):
        # Mock for temp file creation
        mock_temp_file_obj = MagicMock()
        mock_temp_file_obj.name = "dummy_temp.wav"
        mock_tempfile.return_value.__enter__.return_value = mock_temp_file_obj
        
        mock_exists.return_value = True
        mock_getsize.return_value = 1024 # Non-empty file
        mock_run.return_value = MagicMock(stdout=b'', stderr=b'', returncode=0)

        result_path = _util_extract_audio_segment("input.mp4")
        mock_run.assert_called_once()
        args, _ = mock_run.call_args
        expected_cmd = ['ffmpeg', '-y', '-i', 'input.mp4', '-vn', '-acodec', 'pcm_s16le', '-ar', '44100', '-ac', '1', 'dummy_temp.wav']
        self.assertEqual(args[0], expected_cmd)
        self.assertEqual(result_path, "dummy_temp.wav")

    @patch('player.subprocess.run')
    @patch('player.os.path.exists')
    @patch('player.os.path.getsize')
    def test_ffmpeg_command_all_params(self, mock_getsize, mock_exists, mock_run):
        mock_exists.return_value = True
        mock_getsize.return_value = 1024
        mock_run.return_value = MagicMock(stdout=b'', stderr=b'', returncode=0)

        result_path = _util_extract_audio_segment(
            "input.mp4", "output.aac", start_sec=10.5, duration_sec=5.2,
            audio_codec="aac", sample_rate=48000, channels=2, 
            overwrite=False, use_temp_file=False
        )
        mock_run.assert_called_once()
        args, _ = mock_run.call_args
        # Note: '-y' (overwrite) should be absent
        expected_cmd = ['ffmpeg', '-ss', '10.5', '-t', '5.2', '-i', 'input.mp4', '-vn', '-acodec', 'aac', '-ar', '48000', '-ac', '2', 'output.aac']
        self.assertEqual(args[0], expected_cmd)
        self.assertEqual(result_path, "output.aac")

    @patch('player.subprocess.run')
    @patch('player.os.path.exists')
    @patch('player.os.path.getsize')
    def test_no_overwrite(self, mock_getsize, mock_exists, mock_run):
        mock_exists.return_value = True
        mock_getsize.return_value = 1024
        mock_run.return_value = MagicMock(stdout=b'', stderr=b'', returncode=0)

        _util_extract_audio_segment("input.mp4", "output.wav", overwrite=False, use_temp_file=False)
        args, _ = mock_run.call_args
        self.assertNotIn('-y', args[0])

    @patch('player.subprocess.run')
    def test_extraction_failure_ffmpeg(self, mock_run):
        mock_run.side_effect = subprocess.CalledProcessError(1, "ffmpeg", stderr=b"ffmpeg error")
        result = _util_extract_audio_segment("input.mp4", "output.wav", use_temp_file=False)
        self.assertIsNone(result)

    @patch('player.subprocess.run')
    @patch('player.os.path.exists')
    def test_extraction_failure_file_not_created(self, mock_exists, mock_run):
        mock_run.return_value = MagicMock(stdout=b'', stderr=b'', returncode=0)
        mock_exists.return_value = False # Simulate file not being created
        result = _util_extract_audio_segment("input.mp4", "output.wav", use_temp_file=False)
        self.assertIsNone(result)

    @patch('player.subprocess.run')
    @patch('player.os.path.exists')
    @patch('player.os.path.getsize')
    def test_extraction_failure_empty_file(self, mock_getsize, mock_exists, mock_run):
        mock_run.return_value = MagicMock(stdout=b'', stderr=b'', returncode=0)
        mock_exists.return_value = True
        mock_getsize.return_value = 0 # Simulate empty file
        result = _util_extract_audio_segment("input.mp4", "output.wav", use_temp_file=False)
        self.assertIsNone(result)

class TestUtilGetTempoLibrosa(unittest.TestCase):
    @patch('player.librosa.beat.beat_track')
    def test_normal_case(self, mock_beat_track):
        mock_beat_track.return_value = (120.0, np.array([10, 20, 30]))
        y_fake = np.random.rand(22050 * 2)  # 2 seconds of fake audio
        sr_fake = 22050
        
        tempo, beats = _util_get_tempo_and_beats_librosa(y_fake, sr_fake)
        
        mock_beat_track.assert_called_once_with(y=y_fake, sr=sr_fake)
        self.assertEqual(tempo, 120.0)
        np.testing.assert_array_equal(beats, np.array([10, 20, 30]))

    def test_empty_audio_data(self):
        y_empty = np.array([])
        sr_fake = 22050
        tempo, beats = _util_get_tempo_and_beats_librosa(y_empty, sr_fake)
        self.assertEqual(tempo, 0.0)
        np.testing.assert_array_equal(beats, np.array([]))

    def test_none_audio_data(self):
        y_none = None
        sr_fake = 22050
        tempo, beats = _util_get_tempo_and_beats_librosa(y_none, sr_fake)
        self.assertEqual(tempo, 0.0)
        np.testing.assert_array_equal(beats, np.array([]))

    @patch('player.librosa.beat.beat_track')
    def test_librosa_exception(self, mock_beat_track):
        mock_beat_track.side_effect = Exception("Librosa fake error")
        y_fake = np.random.rand(1000)
        sr_fake = 22050
        tempo, beats = _util_get_tempo_and_beats_librosa(y_fake, sr_fake)
        self.assertEqual(tempo, 0.0)
        np.testing.assert_array_equal(beats, np.array([]))

class TestExtractKeyframes(unittest.TestCase):
    @patch('player.subprocess.check_output')
    def test_full_extraction_normal(self, mock_check_output):
        # Note: ffprobe output for pkt_pts_time,pict_type with csv=p=0
        ffprobe_output = b"1.000000,I\n2.500000,P\n3.000000,I\n5.000000,I\n"
        mock_check_output.return_value = ffprobe_output
        
        keyframes = extract_keyframes("dummy.mp4")
        self.assertEqual(keyframes, [1.0, 3.0, 5.0])
        mock_check_output.assert_called_with([
            "ffprobe", "-v", "error", "-select_streams", "v:0",
            "-show_entries", "frame=pkt_pts_time,pict_type",
            "-of", "csv=p=0", "dummy.mp4"
        ], stderr=subprocess.PIPE)

    @patch('player.subprocess.check_output')
    def test_full_extraction_no_keyframes(self, mock_check_output):
        ffprobe_output = b"1.000000,P\n2.500000,B\n3.000000,P\n"
        mock_check_output.return_value = ffprobe_output
        
        keyframes = extract_keyframes("dummy.mp4")
        self.assertEqual(keyframes, [])

    @patch('player.subprocess.check_output')
    def test_windowed_extraction_start_and_duration(self, mock_check_output):
        ffprobe_output = b"0.5,I\n1.0,I\n1.5,I\n2.0,I\n2.5,I\n3.0,I\n3.5,I\n4.0,I\n"
        mock_check_output.return_value = ffprobe_output
        
        # Window: [1.0, 1.0 + 2.0) = [1.0, 3.0)
        keyframes = extract_keyframes("dummy.mp4", start_time_sec=1.0, duration_sec=2.0)
        self.assertEqual(keyframes, [1.0, 1.5, 2.0, 2.5])

    @patch('player.subprocess.check_output')
    def test_windowed_extraction_start_and_end_time(self, mock_check_output):
        ffprobe_output = b"0.5,I\n1.0,I\n1.5,I\n2.0,I\n2.5,I\n3.0,I\n3.5,I\n4.0,I\n"
        mock_check_output.return_value = ffprobe_output
        
        # Window: [1.2, 3.2)
        keyframes = extract_keyframes("dummy.mp4", start_time_sec=1.2, end_time_sec=3.2)
        self.assertEqual(keyframes, [1.5, 2.0, 2.5, 3.0])
        
    @patch('player.subprocess.check_output')
    def test_windowed_extraction_only_start_time(self, mock_check_output):
        ffprobe_output = b"0.5,I\n1.0,I\n1.5,I\n2.0,I\n2.5,I\n"
        mock_check_output.return_value = ffprobe_output
        
        # Window: [1.5, infinity)
        keyframes = extract_keyframes("dummy.mp4", start_time_sec=1.5)
        self.assertEqual(keyframes, [1.5, 2.0, 2.5])

    @patch('player.subprocess.check_output')
    def test_windowed_no_match(self, mock_check_output):
        ffprobe_output = b"1.0,I\n2.0,I\n3.0,I\n"
        mock_check_output.return_value = ffprobe_output
        
        keyframes = extract_keyframes("dummy.mp4", start_time_sec=4.0, duration_sec=1.0)
        self.assertEqual(keyframes, [])

    @patch('player.subprocess.check_output')
    def test_ffprobe_error(self, mock_check_output):
        mock_check_output.side_effect = subprocess.CalledProcessError(1, "ffprobe", stderr=b"ffprobe error")
        keyframes = extract_keyframes("dummy.mp4")
        self.assertEqual(keyframes, [])
        
    @patch('player.subprocess.check_output')
    def test_malformed_ffprobe_output(self, mock_check_output):
        ffprobe_output = b"1.0,I\nthis_is_not_a_time,I\n3.0,I\n"
        mock_check_output.return_value = ffprobe_output
        keyframes = extract_keyframes("dummy.mp4")
        self.assertEqual(keyframes, [1.0, 3.0]) # Should skip the malformed line


class TestBuildRhythmGrid(unittest.TestCase):
    class Dummy(VideoPlayer):
        def __init__(self):
            self.loop_start = 1
            self.loop_end = 1001
            self.tempo_bpm = 60
            self.subdivision_mode = "binary8"
            self.grid_times = []
            self.grid_labels = []
            self.grid_subdivs = []
            self.seq = None

        def get_current_syllable_sequence(self):
            return self.seq if self.seq is not None else ["1", "&", "2", "&", "3", "&", "4", "&"]

        def hms(self, ms):
            return str(ms)

    def test_label_from_sequence_index(self):
        d = self.Dummy()
        d.seq = ["1", "&", "2", "&", "3", "&", "4", "&"]
        VideoPlayer.build_rhythm_grid(d)
        self.assertEqual(d.grid_labels[-1], "2")
        self.assertEqual(len(d.grid_labels), 3)

    def test_no_duplicate_at_loop_end(self):
        d = self.Dummy()
        d.seq = ["da", "da"]
        VideoPlayer.build_rhythm_grid(d)
        self.assertEqual(d.grid_labels, ["da", "da"])
        self.assertEqual(len(d.grid_times), 2)


class TestDegreeFromChordMapping(unittest.TestCase):
    class Dummy(VideoPlayer):
        def __init__(self):
            pass

    def test_all_major_keys_present(self):
        vp = self.Dummy()
        keys = ["C", "C#", "Db", "D", "D#", "Eb", "E", "F", "F#", "Gb", "G", "G#", "Ab", "A", "A#", "Bb", "B"]
        for k in keys:
            self.assertNotEqual(vp.degree_from_chord(k, k), "?")


class TestZoomScroll(unittest.TestCase):
    class Dummy(VideoPlayer):
        def __init__(self):
            self.loop_start = 0
            self.loop_end = 10000
            self.loop_zoom_ratio = 2.0
            self.playhead_time = 0.0
            self.player = MagicMock()
            self.player.get_length.return_value = 10000
            self.zoom_context = {
                "zoom_start": 0,
                "zoom_end": 5000,
                "zoom_range": 5000,
            }

    def test_scroll_reaches_B(self):
        d = self.Dummy()
        d.playhead_time = 10.0
        ctx = d.get_zoom_context()
        self.assertEqual(ctx["zoom_end"], d.loop_end)

    def test_midway_scroll(self):
        d = self.Dummy()
        d.playhead_time = 5.0
        ctx = d.get_zoom_context()
        self.assertEqual(ctx["zoom_start"], 2500)
        self.assertEqual(ctx["zoom_end"], 7500)


class TestTogglePauseLoopTiming(unittest.TestCase):
    def _create_player(self):
        vp = VideoPlayer.__new__(VideoPlayer)
        vp.root = MagicMock()
        vp.root.after_cancel = MagicMock()
        vp.console = MagicMock()
        vp.player = MagicMock()
        vp.player.get_time.return_value = 2000
        vp.player.pause = MagicMock()
        vp.player.play = MagicMock()
        vp.after_id = "id"
        vp.playhead_time = None
        vp.loop_start = 0
        vp.loop_end = 4000
        vp.loop_duration_s = 4.0
        vp.last_loop_jump_time = 50.0
        vp.update_loop = MagicMock()
        return vp

    @patch('player.time.perf_counter', side_effect=[100.0, 110.0])
    @patch.object(VideoPlayer, 'safe_jump_to_time')
    def test_pause_resume_adjusts_last_loop_jump(self, mock_jump, mock_perf):
        vp = self._create_player()
        vp.toggle_pause()
        self.assertTrue(vp.is_paused)
        self.assertEqual(vp.pause_start_time, 100.0)

        vp.toggle_pause()
        self.assertFalse(vp.is_paused)
        self.assertAlmostEqual(vp.last_loop_jump_time, 60.0)
        mock_jump.assert_called_once_with(int(vp.playhead_time * 1000), source="toggle_pause")
        vp.player.play.assert_called_once()
        vp.update_loop.assert_called_once()


class TestGridZoomScaling(unittest.TestCase):
    class Dummy(VideoPlayer):
        def __init__(self):
            self.loop_start = 0
            self.loop_end = 8000
            self.tempo_bpm = 60
            self.subdivision_mode = "binary4"
            self.grid_canvas = MagicMock()
            self.grid_canvas.winfo_width.return_value = 1000
            self.player = MagicMock()
            self.player.get_length.return_value = 8000
            self.loop_zoom_ratio = 2.0
            self.zoom_context = {"zoom_start": 0, "zoom_end": 4000, "zoom_range": 4000}
            self.subdivision_state = {}

    def test_subdivision_positions_scaled_with_zoom(self):
        d = self.Dummy()
        VideoPlayer.build_rhythm_grid(d)
        infos = d.compute_rhythm_grid_infos()
        self.assertAlmostEqual(infos[0]["x"], 200)
        self.assertAlmostEqual(infos[1]["x"], 350)


class TestSpawnNewInstance(unittest.TestCase):
    @patch('player.subprocess.Popen')
    @patch('player.sys.exit')
    def test_open_given_file_spawns(self, mock_exit, mock_popen):
        vp = VideoPlayer.__new__(VideoPlayer)
        vp.root = MagicMock()
        VideoPlayer.open_given_file(vp, 'sample.mp4', spawn_new_instance=True)
        expected = [sys.executable, os.path.abspath(player.__file__), 'sample.mp4']
        mock_popen.assert_called_once_with(expected)
        vp.root.destroy.assert_called_once()
        mock_exit.assert_called_once_with(0)


class TestOpenFileAfterCancel(unittest.TestCase):
    def _create_player(self):
        vp = VideoPlayer.__new__(VideoPlayer)
        vp.root = MagicMock()
        vp.root.after_cancel = MagicMock()
        vp.root.after = MagicMock()
        vp.refresh_static_timeline_elements = MagicMock()
        vp.canvas = MagicMock()
        vp.canvas.winfo_id.return_value = 1
        vp.console = MagicMock()
        vp.instance = MagicMock()
        vp.instance.media_new.return_value = MagicMock()
        vp.player = MagicMock()
        vp.load_saved_loops = MagicMock()
        vp.apply_crop = MagicMock()
        vp.safe_update_playhead = MagicMock()
        vp.update_loop = MagicMock()
        vp._compute_audio_power_data = MagicMock()
        vp.after_id = None
        return vp

    @patch('player.filedialog.askopenfilename', side_effect=['f1.mp4', 'f2.mp4'])
    @patch('player.subprocess.Popen')
    @patch('player.sys.exit')
    @patch('threading.Thread')
    def test_cancel_previous_after(self, mock_thread, mock_exit, mock_popen, mock_dialog):
        vp = self._create_player()
        vp.root.destroy = MagicMock()
        VideoPlayer.open_file(vp, spawn_new_instance=True)
        vp.after_id = 'cb1'
        VideoPlayer.open_file(vp, spawn_new_instance=True)
        vp.root.after_cancel.assert_called_once_with('cb1')
        self.assertIsNone(vp.after_id)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
