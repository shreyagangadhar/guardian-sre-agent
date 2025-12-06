
import subprocess
import logging
import yaml
import os
from history_manager import HistoryManager

logger = logging.getLogger("Guardian")

class RemediationExecutor:
    def __init__(self, config_path="config.yaml"):
        self.config = self._load_config(config_path)
        self.history = HistoryManager()

    def _load_config(self, path):
        try:
            with open(path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            return {}

    def execute_remediation(self, alert_type):
        """
        Executes the remediation script for the given alert type.
        """
        scripts = self.config.get('REMEDIATION_SCRIPTS', {})
        script_path = scripts.get(alert_type)

        if not script_path:
            logger.warning(f"No remediation script found for alert type: {alert_type}")
            return False

        logger.info(f"Executing remediation for {alert_type}: {script_path}")
        
        try:
            # Check if script is executable
            if not os.access(script_path, os.X_OK):
                 # Try to make it executable or run with sh
                 pass

            # using subproccess.run for security
            result = subprocess.run([script_path], capture_output=True, text=True, shell=False)
            
            if result.returncode == 0:
                logger.info(f"Remediation script executed successfully.\nOutput: {result.stdout}")
                self.history.add_event('remediation', f"Executed {script_path}", 'success', alert_type)
                return True
            else:
                logger.error(f"Remediation script failed (Exit Code {result.returncode}).\nError: {result.stderr}")
                self.history.add_event('remediation', f"Failed execution of {script_path}: {result.stderr}", 'failed', alert_type)
                return False

        except Exception as e:
            logger.error(f"Remediation execution error: {e}")
            return False
