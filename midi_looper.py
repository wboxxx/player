import time
from typing import Dict, List, Tuple, Union, Optional

try:
    import rtmidi
except ImportError:  # pragma: no cover - rtmidi may not be installed during tests
    rtmidi = None


class MidiLooper:
    """Real-time MIDI playback synced to an A/B loop.

    The class exposes a small API to load a pattern of notes and to call
    :py:meth:`update_playhead` as the media playhead advances.  Notes are sent
    through a virtual ``rtmidi`` output port which can then be routed in Carla
    or any other MIDI host.
    """

    def __init__(
        self,
        tempo_bpm: float,
        loop_start_ms: int,
        loop_end_ms: int,
        grid_times: List[float],
        *,
        port_name: str = "PlayerMidiOut",
        note_length_ms: int = 200,
    ) -> None:
        if rtmidi is None:
            raise RuntimeError("python-rtmidi is required for MidiLooper")

        self.tempo_bpm = tempo_bpm
        self.loop_start_ms = loop_start_ms
        self.loop_end_ms = loop_end_ms
        self.loop_duration_ms = max(loop_end_ms - loop_start_ms, 1)
        self.grid_times = grid_times
        self.port_name = port_name
        self.note_length_ms = note_length_ms

        self.midiout: Optional[rtmidi.MidiOut] = None
        self.pattern: List[Tuple[int, int]] = []  # list of (time_ms, midi_note)
        self.active_notes: Dict[int, float] = {}
        self.pending_off_events: List[Tuple[float, int]] = []
        self.last_loop_pos: Optional[int] = None
        self.running = False

    def load_pattern(self, pattern: Dict[Union[int, float], int]) -> None:
        """Load a note pattern mapping timestamps or grid indices to MIDI notes."""
        events: List[Tuple[int, int]] = []
        for key, note in pattern.items():
            if isinstance(key, int) and key < len(self.grid_times):
                t_ms = int(self.grid_times[key] * 1000)
            else:
                t_ms = int(float(key))
            t_ms = max(0, min(t_ms, self.loop_duration_ms - 1))
            events.append((t_ms, note))
        self.pattern = sorted(events, key=lambda x: x[0])

    def start_loop(self) -> None:
        if self.running:
            return
        self.midiout = rtmidi.MidiOut()
        self.midiout.open_virtual_port(self.port_name)
        self.last_loop_pos = None
        self.running = True

    def stop_loop(self) -> None:
        if not self.running:
            return
        for note in list(self.active_notes):
            self._send_note_off(note)
        self.active_notes.clear()
        self.pending_off_events.clear()
        self.running = False
        if self.midiout:
            self.midiout.close_port()
            self.midiout = None

    # --- Internal helpers -------------------------------------------------
    def _send_note_on(self, note: int, velocity: int = 100) -> None:
        if self.midiout:
            self.midiout.send_message([0x90, note, velocity])
        print(
            f"[MIDI] NoteOn  note={note} vel={velocity} system_ms={int(time.time()*1000)}"
        )

    def _send_note_off(self, note: int) -> None:
        if self.midiout:
            self.midiout.send_message([0x80, note, 0])
        print(
            f"[MIDI] NoteOff note={note} system_ms={int(time.time()*1000)}"
        )

    # --- Main update ------------------------------------------------------
    def update_playhead(self, playhead_ms: int) -> None:
        """Update loop state given the current playhead position.

        Parameters
        ----------
        playhead_ms : int
            Current playhead timestamp in milliseconds relative to the start of
            the media file.
        """
        if not self.running or not self.pattern:
            return
        loop_pos = (playhead_ms - self.loop_start_ms) % self.loop_duration_ms
        if self.last_loop_pos is None:
            self.last_loop_pos = loop_pos
            return

        # Determine notes that fall between last position and current
        if loop_pos >= self.last_loop_pos:
            todo = [ev for ev in self.pattern if self.last_loop_pos < ev[0] <= loop_pos]
        else:  # wrapped around
            todo = [ev for ev in self.pattern if ev[0] > self.last_loop_pos or ev[0] <= loop_pos]

        self.last_loop_pos = loop_pos

        if todo:
            print(
                f"[MIDI] Trigger {len(todo)} note(s) at playhead_ms={playhead_ms} loop_pos={loop_pos}"
            )

        now_ms = time.time() * 1000.0
        for off_time, note in list(self.pending_off_events):
            if now_ms >= off_time:
                self._send_note_off(note)
                self.pending_off_events.remove((off_time, note))
                self.active_notes.pop(note, None)

        for t_ms, note in todo:
            if note in self.active_notes:
                self._send_note_off(note)
                self.active_notes.pop(note, None)
            self._send_note_on(note)
            off = now_ms + self.note_length_ms
            self.pending_off_events.append((off, note))
            self.active_notes[note] = off

