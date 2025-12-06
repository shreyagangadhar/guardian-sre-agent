
import time
import logging
import yaml
import json
import os
from monitoring import check_http_health, check_disk_usage
from alert_processor import AlertProcessor
from triage import run_diagnostics
from remediation import RemediationExecutor
from history_manager import HistoryManager

# Configure Logging
logging.basicConfig(
    filename='guardian.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("Guardian")

def load_config(path="config.yaml"):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def main():
    logger.info("Guardian SRE Agent Starting...")
    config = load_config()
    alert_processor = AlertProcessor()
    remediation_executor = RemediationExecutor()
    history_manager = HistoryManager()

    monitored_services = config.get('MONITORED_SERVICES', [])
    disk_threshold = config.get('DISK_THRESHOLD', 85)
    
    logger.info(f"Monitoring {len(monitored_services)} services.")

    while True:
        try:
            # 1. Monitoring
            alerts = []
            
            # Check HTTP Services
            for service in monitored_services:
                status, message = check_http_health(service['url'])
                if not status:
                    alerts.append({
                        'type': 'ServiceDown',
                        'details': f"{service['name']} is down. {message}"
                    })
            
            # Check Disk
            disk_status, disk_msg = check_disk_usage(disk_threshold)
            if not disk_status:
                alerts.append({
                    'type': 'DiskFull',
                    'details': disk_msg
                })

            # --- EXPORT STATE ---
            state = {
                "services": [],
                "alerts": alerts,
                "disk_status": {"status": disk_status, "message": disk_msg},
                "last_updated": time.ctime()
            }
            # Add service status to state (re-checking for display or just using the loop)
            # For simplicity, let's just make the services list reflect the config + status we just checked
            for i, service in enumerate(monitored_services):
                 # We need to capture the status from the loop above. 
                 # Let's optimize: reconstruct services list with status
                 s_status, s_msg = check_http_health(service['url']) # Double check or store from above
                 state["services"].append({
                     "name": service['name'],
                     "url": service['url'],
                     "status": "UP" if s_status else "DOWN",
                     "message": s_msg
                 })
            
            with open("status.json", "w") as f:
                json.dump(state, f)
            # --------------------

            # 2. Alert Processing & Triage & Remediation
            for raw_alert in alerts:
                alert = alert_processor.process_alert(raw_alert)
                
                if alert: 
                    # New actionable alert
                    logger.info(f"Triage started for {alert['type']}")
                    history_manager.add_event('alert', alert['details'], 'triggered', alert['type'])
                    
                    # 3. Triage
                    triage_result = run_diagnostics(alert['type'])
                    logger.info(f"Triage result: {triage_result}")

                    # 4. Remediation
                    # In this simple logic, we remediate if Triage confirms issue or unconditionally for the demo
                    if triage_result in ["PortClosed", "DiskSpaceChecked"]:
                         logger.info(f"Attempting remediation for {alert['type']}")
                         success = remediation_executor.execute_remediation(alert['type'])
                         if success:
                             logger.info("Remediation successful.")
                         else:
                             logger.error("Remediation failed.")
                    else:
                        logger.info("Skipping remediation based on triage result.")

            time.sleep(10) # Poll every 10 seconds for demo

        except KeyboardInterrupt:
            logger.info("Guardian Agent stopping...")
            break
        except Exception as e:
            logger.error(f"Main loop error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
