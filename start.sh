#!/bin/bash
# Activate Render’s Python virtual environment if it exists
if [ -f "./.venv/bin/activate" ]; then
    source .venv/bin/activate
fi

# Use python3 explicitly
python3 -m uvicorn cleanup_api:app --host 0.0.0.0 --port $PORT