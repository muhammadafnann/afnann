import subprocess
import os
import sys
import time
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.db.database import log_event

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("Healer")

# Global dict to store running process instances
processes = {}

def start_process(process_name, command):
    logger.info(f"Starting process: {process_name}")
    try:
        proc = subprocess.Popen(
            command,
            shell=True,
            cwd=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        )
        processes[process_name] = proc
        log_event(process_name, "start", f"Process started with PID {proc.pid}")
        return proc
    except Exception as e:
        logger.error(f"Failed to start {process_name}: {e}")
        log_event(process_name, "error", f"Failed to start: {e}")
        return None

def check_and_heal(process_name, command):
    proc = processes.get(process_name)
    if proc is None:
        logger.warning(f"Process {process_name} is not running. Healing (starting)...")
        start_process(process_name, command)
    else:
        # Check if process has terminated
        retcode = proc.poll()
        if retcode is not None:
            logger.error(f"Process {process_name} died with return code {retcode}. Healing (restarting)...")
            log_event(process_name, "crash", f"Process died with return code {retcode}. Restarting.")
            start_process(process_name, command)
            
def get_process(process_name):
    return processes.get(process_name)

if __name__ == '__main__':
    # Test block
    start_process('sensor_daemon', 'python src/mock_services/sensor_daemon.py')
    time.sleep(10)
    check_and_heal('sensor_daemon', 'python src/mock_services/sensor_daemon.py')
