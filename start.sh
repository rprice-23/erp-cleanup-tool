#!/bin/bash

export PATH="/opt/render/project/.venv/bin:$PATH"

python3 -m uvicorn cleanup_api:app --host 0.0.0.0 --port $PORT