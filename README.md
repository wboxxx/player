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
