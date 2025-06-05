#!/usr/bin/env bash
# Setup script for Player3
# Creates a Python virtual environment and installs dependencies
set -e

python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Upgrade pip and install dependencies
python -m pip install --upgrade pip
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
fi

echo "Reminder: system packages like 'ffmpeg' and 'python3-tk' may be required."
