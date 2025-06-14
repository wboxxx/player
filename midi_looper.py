import time
import threading
from typing import List, Dict, Union, Tuple, Optional

try:
    import rtmidi
except ImportError:
    rtmidi = None

def midi_note_to_name(note: int) -> str:
    names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    octave = (note // 12) - 1
    name = names[note % 12]
    return f"{name}{octave}"

class MidiLooper:
    def __init__(
        self,
        tempo_bpm: float,
        grid_times: List[float],
        *,
        port_name: str = "PlayerMidiOut",
        note_length_ms: int = 200,
        loop_duration_ms: Optional[int] = None
    ) -> None:
        if rtmidi is None:
            raise RuntimeError("python-rtmidi is required for MidiLooper")

        self.tempo_bpm = tempo_bpm
        self.grid_times = grid_times
        self.port_name = port_name
        self.note_length_ms = note_length_ms
        self.loop_duration_ms = loop_duration_ms or int((grid_times[-1] * 1000) if grid_times else 1000)

        self.midiout: Optional[rtmidi.MidiOut] = None
        self.pattern: List[Tuple[int, int]] = []  # list of (time_ms, midi_note)
        self.active_notes: Dict[int, float] = {}
        self.running = False
        self.thread: Optional[threading.Thread] = None
        self.start_time: Optional[float] = None

    def load_pattern(self, pattern: Dict[Union[int, float], int]) -> None:
        events = []
        for key, note in pattern.items():
            if isinstance(key, int) and key < len(self.grid_times):
                t_ms = int(self.grid_times[key] * 1000)
            else:
                t_ms = int(float(key))
            t_ms = max(0, min(t_ms, self.loop_duration_ms - 1))
            events.append((t_ms, note))
        self.pattern = sorted(events, key=lambda x: x[0])
        print(f"[MIDILOOPER] 🎼 Pattern loaded: {len(self.pattern)} events")

    def _send_note_on(self, note: int, velocity: int = 100) -> None:
        if self.midiout:
            self.midiout.send_message([0x90, note, velocity])
        print(f"[MIDILOOPER] 🎵 NoteOn  → {note} ({midi_note_to_name(note)})")

    def _send_note_off(self, note: int) -> None:
        if self.midiout:
            self.midiout.send_message([0x80, note, 0])
        print(f"[MIDILOOPER] 🔇 NoteOff → {note} ({midi_note_to_name(note)})")

    def _mark_done(self):
        self.running = False
        print("[MIDILOOPER] ✅ Playback finished")


    def go(self) -> None:
        if self.running:
            print("[MIDILOOPER] ⚠️ Already running")
            return

        print("[MIDILOOPER] ▶️ Triggering one-shot MIDI playback")
        self.running = True
        self.start_time = time.time() * 1000  # ms

        self.midiout = rtmidi.MidiOut()
        ports = self.midiout.get_ports()
        for i, name in enumerate(ports):
            if self.port_name.lower() in name.lower():
                self.midiout.open_port(i)
                break
        else:
            try:
                self.midiout.open_virtual_port(self.port_name)
            except Exception as e:
                print(f"[MIDILOOPER] ❌ MIDI port error: {e}")
                self.running = False
                return

        self._play_once()

    def _play_once(self) -> None:
        """Play the pattern once, synchronised in real time."""
        now = time.time() * 1000  # ms
        for t_ms, note in self.pattern:
            delay_sec = max((t_ms - (now - self.start_time)) / 1000.0, 0)
            print(f"[MIDILOOPER] ⏳ Scheduling note {note} in {delay_sec:.3f}s")
            threading.Timer(delay_sec, self._send_note_on, args=[note]).start()
            threading.Timer(delay_sec + self.note_length_ms / 1000.0, self._send_note_off, args=[note]).start()

        # Auto-clean running flag after longest note
        total_duration = max((t for t, _ in self.pattern), default=0) + self.note_length_ms
        threading.Timer(total_duration / 1000.0, self._mark_done).start()

def _mark_done(self):
    self.running = False
    print("[MIDILOOPER] ✅ Playback finished")
    def _loop(self) -> None:
        next_index = 0
        loop_start = self.start_time
        while self.running:
            now = time.time() * 1000  # ms
            loop_pos = (now - loop_start) % self.loop_duration_ms

            while next_index < len(self.pattern) and self.pattern[next_index][0] <= loop_pos:
                t_ms, note = self.pattern[next_index]
                self._send_note_on(note)
                threading.Timer(self.note_length_ms / 1000, self._send_note_off, args=[note]).start()
                next_index += 1

            if next_index >= len(self.pattern):
                next_index = 0
                loop_start = time.time() * 1000
                print("[MIDILOOPER] 🔁 Loop restarted")

            time.sleep(0.01)

    def stop(self) -> None:
        print("[MIDILOOPER] ⏹️ Stopping playback")
        self.running = False
        self.active_notes.clear()
        if self.midiout:
            self.midiout.close_port()
            self.midiout = None
        self.thread = None
        print("[MIDILOOPER] ✅ Stopped cleanly")
