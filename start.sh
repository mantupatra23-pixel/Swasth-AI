#!/usr/bin/env python3
import os
import subprocess

print("🚀 Swasth-AI server starting (Render Fix)...")

# Ensure dependencies
subprocess.run(["pip", "install", "--upgrade", "pip", "setuptools", "wheel", "uvicorn", "fastapi", "python-dotenv"], check=True)

print("✅ All dependencies installed successfully!")

# Launch Uvicorn manually
os.execvp("python3", ["python3", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", os.getenv("PORT", "10000")])
