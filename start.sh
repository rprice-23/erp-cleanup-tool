#!/bin/bash
python -m uvicorn cleanup_api:app --host 0.0.0.0 --port $PORT