#!/bin/python

import os
import sys
import time
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path = sys.path + [BASE_DIR]
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PiMonitor.settings')

import psutil
from datetime import datetime

from monitor.models import MemoryLog, SwapLog, CpuLog

def update_logs():
    memory = psutil.virtual_memory()
    swap = psutil.swap_memory()
    cpu = psutil.cpu_percent(percpu=True)
    boot_time = psutil.boot_time()
    uptime = datetime.now() - datetime.fromtimestamp(boot_time)
    tasks_num = len(psutil.pids())

    MemoryLog.objects.create(
        total=memory.total, available=memory.available,
        percent=memory.percent, uptime=uptime, tasks_num=tasks_num
    )
    SwapLog.objects.create(
        total=swap.total, used=swap.used, free=swap.free, percent=swap.percent
    )
    CpuLog.objects.create(percents=json.dumps(cpu))

if __name__ == '__main__':
    while(True):
        update_logs()
        time.sleep(5)
