# Player3 - Audio-Visual Practice Tool

This project is an interactive GUI-based audio/video loop player tailored for music practice and analysis.  
It was developed with the help of AI tools (e.g., ChatGPT) and includes original ideas and interface designs by Vincent Boiteau.

## Features

- Loop-based playback with A/B markers
- Tempo synchronization and grid display
- GUI with real-time feedback
- Optional integration of MIDI and audio analysis

## Getting Started

1. Run `./setup_env.sh` to create a virtual environment and install Python
   dependencies listed in `requirements.txt`.
2. Activate the environment:
   `source .venv/bin/activate`
3. Launch the application with `python player.py`.
   You can optionally pass a number to load a recent file by index or a full
   file path to open that media directly.
   The `open_file()` and `open_given_file()` methods also accept a
   `spawn_new_instance` flag. When set to `True` the current player spawns
   `python player.py <path>` in a new process and then exits.

The setup script reminds you to install system packages such as `ffmpeg` and
`python3-tk` which are required for full functionality.

## Stub Libraries for Testing

For ease of testing, this repository ships with lightweight stub versions of
several third-party libraries. You will find files such as `stubs/numpy_stub.py`, the
`stubs/librosa/` and `stubs/scipy/` directories, and `stubs/soundfile.py` in the
`stubs/` directory. These files only implement the minimal functions required by the unit tests.

When Python imports modules with these names, the stubs take precedence over any
installed packages. Running the full application with the real feature set may
therefore require removing or renaming these stub files so that Python can load
the actual libraries from your environment.

To install the real dependencies, activate your virtual environment and run:

```bash
pip install numpy librosa soundfile scipy
```

Additional packages listed in the source (e.g. `matplotlib`, `pygame`, `torch`)
may also be required depending on the features you want to use.

## AI Contribution Notice

The code includes parts generated or assisted by AI. The unique value of the project resides in:

- The interface and feature design
- The integration choices
- The specific user flow and customizations

If you reuse this work, please respect the license and give proper attribution.

## License

MIT — See `LICENSE` file for details.

## loop scroll
🎛️ Zoom and Scroll Logic in the Zoom Window

🟢 Phase 1: Standard Zoom — Centered on the Loop

As long as the zoom level is moderate:
	•	The zoom window stays fixed, centered on the middle of the loop (between A and B).
	•	The visible range (zoom_range) gets progressively smaller as the user zooms in.
	•	This continues until the zoom_range becomes approximately loop_duration / 0.9 — that is, about 111% of the loop duration.
	•	During this phase, the view is stable: no scrolling, no playhead repositioning.

🟡 Phase 2: Scroll Mode — Interpolated View Following the Playhead

Once the zoom goes beyond that threshold, we enter dynamic scroll mode:
	•	The zoom window starts to move horizontally within the loop range.
	•	It is not centered on the playhead.
	•	Instead, the playhead position on the canvas is interpolated:
	•	At the start (when the playhead is at A), it’s shown at 5% of the canvas width.
	•	At the end (when the playhead reaches B), it’s at 95%.
	•	This creates a smooth visual scroll.
	•	The actual zoom window length is fixed or clamped to a minimum duration (e.g., 4 seconds), which is smaller than the loop duration.

🔁 Example: Playhead Scroll Over an 8s Loop
	•	Suppose the loop is 8 seconds long.
	•	When the scroll begins, the playhead is at A, shown at 5% of canvas width.
	•	Over time, as the playhead moves toward B, its x-position increases gradually to 95%.
	•	Visually:
	•	The playhead traverses 8 seconds,
	•	But only moves across 90% of the canvas.
	•	→ Its visual speed is reduced by ~50%.

🧠 Visual Synchronization of Layers

While this interpolated scroll is happening:
	•	All time-synced visual layers — waveform (RMS power), rhythmic grid, etc. — must:
	•	Scroll accordingly, so they stay aligned with the playhead’s real-time position.
	•	Update dynamically to maintain visual accuracy and rhythmic alignment.

