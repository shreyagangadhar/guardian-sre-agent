from flask import Flask, render_template, jsonify
import signal
import sys
import time
import random
from collections import deque
import json
import os
import subprocess
from history_manager import HistoryManager

app = Flask(__name__)
STATUS_FILE = "status.json"
LOG_FILE = "guardian.log"
history_manager = HistoryManager()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/status')
def get_status():
    if os.path.exists(STATUS_FILE):
        try:
            with open(STATUS_FILE, 'r') as f:
                data = json.load(f)
                return jsonify(data)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "No status file found. Agent might not be running."}), 404

@app.route('/api/logs')
def get_logs():
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, 'r') as f:
                # Read last 50 lines
                lines = f.readlines()[-50:]
                return jsonify({"logs": lines})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"logs": ["Log file not found."]}), 200

@app.route('/api/history')
def get_history():
    data = history_manager.load_history()
    # Sort by timestamp desc
    data.sort(key=lambda x: x['timestamp'], reverse=True)
    return jsonify(data)

# --- Metrics Simulation ---
cpu_history = deque(maxlen=60)
memory_history = deque(maxlen=60)
latency_history = deque(maxlen=60)

def generate_metrics():
    # Simulate CPU: Sine wave + noise
    t = time.time()
    base_cpu = 30 + (20 *  (1 +  math.sin(t / 10))) 
    cpu = base_cpu + random.uniform(-5, 5)
    cpu = max(0, min(100, cpu))

    # Simulate Memory: Random walk
    last_mem = memory_history[-1] if memory_history else 512
    mem = last_mem + random.uniform(-20, 20)
    mem = max(200, min(2048, mem))

    # Simulate Latency: Spikey
    latency = random.paretovariate(3) * 20 + 10 # Long tail distribution

    return round(cpu, 1), int(mem), int(latency)

@app.route('/api/metrics')
def get_metrics():
    # Generate a new point each time called (or could be background thread)
    # For simplicity, we'll generate on request but claim it's "live"
    # To make it look like a history, we'll populate if empty
    import math # importing here to avoid restart issues if helpful, or move up
    
    if not cpu_history:
        for i in range(60):
            cpu_history.append(random.uniform(10, 50))
            memory_history.append(random.uniform(400, 600))
            latency_history.append(random.uniform(10, 50))

    # Add new point
    import math 
    t = time.time()
    cpu = 30 + (10 * math.sin(t/5)) + random.uniform(0, 10)
    mem = 512 + (50 * math.cos(t/10)) + random.uniform(-10, 10)
    lat = random.randint(10, 100)
    if random.random() > 0.9: lat += 200 # Spike

    cpu_history.append(round(cpu, 1))
    memory_history.append(int(mem))
    latency_history.append(int(lat))

    return jsonify({
        "labels": [i for i in range(60)], # Simple index for x-axis
        "cpu": list(cpu_history),
        "memory": list(memory_history),
        "latency": list(latency_history)
    })

@app.route('/api/chaos/kill', methods=['POST'])
def kill_service():
    try:
        subprocess.run(['pkill', '-f', 'dummy_server.py'], check=False)
        return jsonify({"status": "killed"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/chaos/start', methods=['POST'])
def start_service():
    try:
        subprocess.Popen(['python3', 'dummy_server.py'])
        return jsonify({"status": "started"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5001, debug=True)
