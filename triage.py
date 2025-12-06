
import subprocess
import logging

logger = logging.getLogger("Guardian")

def run_diagnostics(alert_type):
    """
    Executes diagnostic steps based on alert type.
    """
    if alert_type == "ServiceDown":
        logger.info("Running diagnostics for ServiceDown...")
        try:
            # Check for listening ports
            result = subprocess.run(['netstat', '-tuln'], capture_output=True, text=True)
            logger.info("Diagnostic Output (netstat):\n" + result.stdout)
            
            # Simple check for port 8080 (hardcoded for the scenario)
            if ":8080" not in result.stdout:
                logger.info("Diagnostic Result: Port 8080 is NOT listening.")
                return "PortClosed"
            else:
                logger.info("Diagnostic Result: Port 8080 IS listening.")
                return "PortOpen"
        except Exception as e:
            logger.error(f"Diagnostics failed: {e}")
            return "DiagnosticsFailed"
            
    elif alert_type == "DiskFull":
        logger.info("Running diagnostics for DiskFull...")
        try:
             # run df -h
            result = subprocess.run(['df', '-h'], capture_output=True, text=True)
            logger.info("Diagnostic Output (df -h):\n" + result.stdout)
            return "DiskSpaceChecked"
        except Exception as e:
             logger.error(f"Diagnostics failed: {e}")
             return "DiagnosticsFailed"

    return "NoDiagnostics"
