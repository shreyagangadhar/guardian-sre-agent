# SRE Agent "Guardian"

Guardian is a modular, Python-based SRE agent designed for autonomous monitoring, triage, and remediation of infrastructure issues.

## Features
- **Monitoring**: Checks HTTP endpoints and disk usage.
- **Alert Processing**: Deduplicates alerts to reduce noise.
- **Triage**: Runs diagnostic commands (`netstat`, `df`, etc.) to investigate alerts.
- **Remediation**: Automatically executes scripts to fix known issues (e.g., restarting a service).
- **Logging**: Detailed audit trail of all actions in `guardian.log`.

## Setup
1.  **Prerequisites**: Python 3.9+
2.  **Installation**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install requests psutil pyyaml
    ```
3.  **Configuration**: Edit `config.yaml` to define monitored services and remediation scripts.

## Usage
Start the agent:
```bash
source venv/bin/activate
python3 agent_main.py
```

## Testing
A dummy server and chaos script are included for verification.
1.  Start the dummy server: `python3 dummy_server.py`
2.  Start the agent: `python3 agent_main.py`
3.  Kill the server: `pkill -f dummy_server.py`
4.  Watch `guardian.log` or the server output to see the agent restart it automatically.

## Project Structure
- `agent_main.py`: Main entry point and orchestration loop.
- `monitoring.py`, `alert_processor.py`, `triage.py`, `remediation.py`: Core modules.
- `config.yaml`: Configuration file.
- `start_service.sh`: Example remediation script.
- `dummy_server.py`: Test service.
