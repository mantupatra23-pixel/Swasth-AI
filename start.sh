#!/usr/bin/env bash
set -e

echo "🔧 Setting up Swasth-AI environment..."

# Ensure pip and uvicorn are installed
python3 -m pip install --upgrade pip
python3 -m pip install "uvicorn[standard]" fastapi python-dotenv

echo "✅ Dependencies installed successfully."
echo "🚀 Launching Swasth-AI server..."

# Start your app using python module (Render safe)
python3 -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
