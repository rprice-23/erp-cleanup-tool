#!/bin/bash
PORT=${PORT:-10000}  # Use Render's $PORT, default to 10000 locally
python3 -m uvicorn cleanup_api:app --host 0.0.0.0 --port $PORT