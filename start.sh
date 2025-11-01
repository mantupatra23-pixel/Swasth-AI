#!/usr/bin/env bash
set -e

echo "🚀 Starting Swasth-AI backend..."

# Install dependencies explicitly at runtime
pip install --upgrade pip
pip install uvicorn fastapi python-dotenv

echo "✅ Dependencies installed successfully."
echo "🔁 Running Uvicorn server..."
python3 -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
