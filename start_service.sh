#!/bin/bash
echo "$(date) - Attempting to restart service..." >> guardian.log
nohup python3 dummy_server.py > /dev/null 2>&1 &
echo "Service restart command issued."

