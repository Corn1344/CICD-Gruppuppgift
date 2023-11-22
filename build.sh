#!/bin/bash

python3 -m venv backend/.venv
. backend/.venv/bin/activate
pip install -r backend/requirements.txt