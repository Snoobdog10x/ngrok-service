#!/bin/bash
cd /home/duythanh/projects/bots/ngrok-service
echo '[INFO] git update project'
git restore --staged .
git restore .
git pull
python3 -m venv .venv
source .venv/bin/activate
echo '[INFO] install ngrok'
pip install ngrok --quiet
echo '[INFO] install firebase-admin'
pip install firebase-admin --quiet
python3 update_hosting.py
