
import requests
import psutil
import logging

logger = logging.getLogger("Guardian")

def check_http_health(url):
    """Checks the health of a given URL."""
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return True, f"Service at {url} is HEALTHY (200 OK)"
        else:
            return False, f"Service at {url} failed with status {response.status_code}"
    except Exception as e:
        return False, f"Service at {url} UNREACHABLE: {str(e)}"

def check_disk_usage(threshold=85):
    """Checks if disk usage exceeds the threshold."""
    # Assuming checking root partition for now
    usage = psutil.disk_usage('/')
    if usage.percent > threshold:
        return False, f"Disk usage CRITICAL: {usage.percent}% > {threshold}%"
    return True, f"Disk usage OK: {usage.percent}%"
