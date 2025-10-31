#!/usr/bin/env bash
# Custom build script for Render Python
set -o errexit

# Upgrade pip, wheel, setuptools before installing
pip install --upgrade pip setuptools wheel

# Then install your app dependencies
pip install -r requirements.txt
