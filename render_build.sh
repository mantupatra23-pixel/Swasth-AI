#!/usr/bin/env bash
# Render Safe Python Build Script (Final Fix)
set -o errexit

# Ensure local venv build path
export PIP_NO_BUILD_ISOLATION=false

# Force reinstall build tools first
python3 -m pip install --upgrade pip setuptools wheel build

# Then install requirements
pip install -r requirements.txt
