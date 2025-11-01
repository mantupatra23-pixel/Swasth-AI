#!/bin/bash
set -e

echo "🔧 Installing uvicorn manually..."
pip install --upgrade pip
pip install uvicorn[standard]

echo "🚀 Launching Swasth-AI..."
python3 -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
