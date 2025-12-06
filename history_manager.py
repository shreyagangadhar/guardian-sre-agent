import json
import os
import uuid
import time
import logging

logger = logging.getLogger("Guardian")

class HistoryManager:
    def __init__(self, storage_file="incidents.json"):
        self.storage_file = storage_file
        self.ensure_storage_exists()

    def ensure_storage_exists(self):
        if not os.path.exists(self.storage_file):
            with open(self.storage_file, 'w') as f:
                json.dump([], f)

    def load_history(self):
        try:
            with open(self.storage_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load history: {e}")
            return []

    def verify_event_structure(self, event):
        """Ensure event has required keys"""
        required_keys = ['id', 'timestamp', 'type', 'details', 'status']
        for key in required_keys:
            if key not in event:
                event[key] = "N/A"
        return event

    def add_event(self, event_type, details, status="triggered", alert_type=None):
        entry = {
            "id": str(uuid.uuid4()),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "type": event_type, # 'alert' or 'remediation'
            "details": details,
            "status": status,
            "alert_type": alert_type if alert_type else "N/A"
        }
        
        try:
            history = self.load_history()
            history.append(entry)
            
            # Keep only last 1000 events to prevent indefinite growth
            if len(history) > 1000:
                history = history[-1000:]
                
            with open(self.storage_file, 'w') as f:
                json.dump(history, f, indent=2)
            
            return entry
        except Exception as e:
            logger.error(f"Failed to save event: {e}")
            return None
