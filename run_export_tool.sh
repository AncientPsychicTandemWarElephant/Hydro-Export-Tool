#!/bin/bash
# Launcher script for Hydrophone Export Tool

cd "$(dirname "$0")"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run the application
python3 main.py