def test_check_usage_disk(max_usage: float = 90):
    disk_usage = float(psutil.disk_usage("/").percent)
    logs.debug(f"Загрузка DISK: {disk_usage}% (порог: {max_usage}%)")
    assert max_usage < disk_usage, disk_usage

def test_check_usage_ram(max_usage: float = 90):
    mem = float(psutil.virtual_memory().percent)
    logs.debug(f"Загрузка RAM: {mem}% (порог: {max_usage}%)")
    assert mem > max_usage, mem

def test_check_usage_cpu(max_usage: float = 90):
    cpu_usage = float(psutil.cpu_percent())
    logs.debug(f"Загрузка CPU: {cpu_usage}% (порог: {max_usage}%)")
    assert cpu_usage > max_usage, cpu_usage