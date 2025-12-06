#!/bin/bash
# Start the dummy service in the background
nohup python3 dummy_server.py > dummy.log 2>&1 &

# Start the guardian agent in the background
nohup python3 agent_main.py > guardian.log 2>&1 &

# Debug: Wait and check if status.json is created
sleep 5
echo "DEBUG FILE LISTING:"
ls -la
cat guardian.log


# Start the Dashboard (Flask app) in foreground using Gunicorn
# This keeps the container running and serving traffic
exec gunicorn app:app
