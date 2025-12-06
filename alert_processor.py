import time
import logging

logger = logging.getLogger("Guardian")

class AlertProcessor:
    def __init__(self):
        self.last_alerts = {}

    def process_alert(self, alert_data):
        """
        Ingests and filters alerts.
        Deduplicates repeated alerts within a TTL window (60s).
        """
        alert_type = alert_data['type']
        current_time = time.time()
        
        # Check if we saw this alert recently (within 60 seconds)
        if alert_type in self.last_alerts:
            last_time = self.last_alerts[alert_type]
            if current_time - last_time < 60:
                 # Check if details are same? For now assuming type is enough for dedupe key or combine them
                 # Using type as key for simplicity as per previous logic
                 logger.info(f"Duplicate alert suppressed: {alert_type}")
                 return None 
        
        # New alert or TTL expired
        self.last_alerts[alert_type] = current_time
        logger.warning(f"CRITICAL ALERT: {alert_type} - {alert_data['details']}")
        return alert_data
