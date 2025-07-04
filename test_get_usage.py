import logging
import psutil

class UsageExceededError(Exception):
    pass

def test_check_usage_disk(max_usage: float = 90):
    disk_usage = float(psutil.disk_usage("/").percent)
    if disk_usage:
        return max_usage < disk_usage, disk_usage
    assert UsageExceededError 

def test_check_usage_ram(max_usage: float = 90):
    mem = float(psutil.virtual_memory().percent)
    if mem:
        return max_usage < mem, mem
    assert UsageExceededError 

def test_check_usage_cpu(max_usage: float = 90):
    cpu_usage = float(psutil.cpu_percent())
    if cpu_usage:
        return max_usage < cpu_usage, cpu_usage
    assert UsageExceededError 