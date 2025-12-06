#!/bin/bash
# Install dependencies
pip install -r requirements.txt

# Start the dummy service in the background (simulating the 'app')
nohup python3 dummy_server.py > dummy.log 2>&1 &

# Start the guardian agent in the background
nohup python3 agent_main.py > guardian.log 2>&1 &
