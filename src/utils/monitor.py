import psutil
import platform
from datetime import datetime

def get_system_info():
    return {
        "cpu_usage": psutil.cpu_percent(interval=1),
        "memory_usage": psutil.virtual_memory().percent,
        "os": platform.system(),
        "last_sync": datetime.now().strftime("%H:%M:%S")
    }