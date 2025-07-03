import json
import asyncio
import os
import logging
import requests
import psutil

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename="server-monitoring.log",
                    filemode="a",
                    )

logs = logging.getLogger(__name__)

def _get_settings(path: str = "settings.json"):
    logs.info(f"Пытаюсь открыть настройки по пути {path}")
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as file:
            logs.info(f"Открыл настройки по пути {path}")
            try:
                result = json.load(file)
                logs.info(f"Настройки успешно загружены: {result}")
                return result
            except json.decoder.JSONDecodeError:
                logs.error(f"Настройки по пути {path} не правильно форматированы.")
    else:
        logs.error(f"По пути {path} не найдено настроек!")
        exit(1)

def _check_usage_disk(max_usage: float = 90):
    disk_usage = float(psutil.disk_usage("/").percent)
    logs.debug(f"Загрузка DISK: {disk_usage}% (порог: {max_usage}%)")
    return max_usage < disk_usage, disk_usage

def _check_usage_ram(max_usage: float = 90):
    mem = float(psutil.virtual_memory().percent)
    logs.debug(f"Загрузка RAM: {mem}% (порог: {max_usage}%)")
    return mem > max_usage, mem

def _check_usage_cpu(max_usage: float = 90):
    cpu_usage = float(psutil.cpu_percent())
    logs.debug(f"Загрузка CPU: {cpu_usage}% (порог: {max_usage}%)")
    return cpu_usage > max_usage, cpu_usage

def do_request(CHAT_ID: int = 0, BOT_TOKEN: str = "", message: str = "test"):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    logs.info(f"Отправка уведомления, сообщение: {message}")
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        logs.info(f"Уведомление успешно отправлено.")
    except requests.exceptions.RequestException as e:
        logs.warning(f"[Ошибка Telegram]: {e}")

async def main():
    settings = _get_settings()

    BOT_TOKEN = settings.get("BOT_TOKEN")
    CHAT_ID = settings.get("CHAT_ID")

    WARNING_USAGE_CPU = settings.get("WARNING_USAGE_CPU")
    WARNING_USAGE_RAM = settings.get("WARNING_USAGE_RAM")
    WARNING_USAGE_DISK = settings.get("WARNING_USAGE_DISK")
    msg_lines = []
    cpu_alert, cpu_value = _check_usage_cpu(max_usage=WARNING_USAGE_CPU)
    disk_alert, disk_value = _check_usage_disk(max_usage=WARNING_USAGE_RAM)
    ram_alert, ram_value = _check_usage_ram(max_usage=WARNING_USAGE_DISK)

    if cpu_alert:
        msg_lines.append(f"⚠️ *CPU* загружен на {cpu_value:.2f}%")

    if disk_alert:
        msg_lines.append(f"⚠️ *DISK* загружен на {disk_value:.2f}%")

    if ram_alert:
        msg_lines.append(f"⚠️ *RAM* загружена на {ram_value:.2f}%")

    if msg_lines:
        full_message = "🚨 *Server Alert!*\n\n" + "\n".join(msg_lines)
        do_request(CHAT_ID=CHAT_ID, BOT_TOKEN=BOT_TOKEN, message=full_message)

if __name__ == "__main__":
    asyncio.run(main())