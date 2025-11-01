#!/bin/sh
set -e

echo "🚀 Booting Swasth-AI (Render Free Tier Safe)..."

python3 -m pip install --upgrade pip setuptools wheel
python3 -m pip install uvicorn fastapi python-dotenv

echo "✅ Uvicorn ready — starting server..."
exec python3 -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
