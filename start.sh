#!/bin/bash
pip install --upgrade pip
pip install uvicorn
exec python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
