#!/bin/bash
python3 -m uvicorn cleanup_api:app --host 0.0.0.0 --port $PORT