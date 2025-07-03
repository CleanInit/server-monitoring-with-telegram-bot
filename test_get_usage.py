import logging
import psutil

def test_check_usage_disk(max_usage: float = 90):
    disk_usage = float(psutil.disk_usage("/").percent)
    assert max_usage < disk_usage, disk_usage

def test_check_usage_ram(max_usage: float = 90):
    mem = float(psutil.virtual_memory().percent)
    assert mem > max_usage, mem

def test_check_usage_cpu(max_usage: float = 90):
    cpu_usage = float(psutil.cpu_percent())
    assert cpu_usage > max_usage, cpu_usage