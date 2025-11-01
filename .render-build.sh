#!/usr/bin/env bash
# Render Build Script Fix for Python 3.13 + Numpy
set -o errexit

echo "---- Upgrading pip and setup tools ----"
pip install --upgrade pip setuptools wheel build

echo "---- Installing core dependencies ----"
pip install "numpy>=2.1.2"

echo "---- Installing from requirements.txt ----"
pip install -r requirements.txt
