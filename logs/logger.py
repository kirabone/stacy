from datetime import datetime
import os

LOG_FILE = None


def start(provider):
    global LOG_FILE

    os.makedirs("logs", exist_ok=True)

    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    LOG_FILE = f"logs/{provider}-{now}.log"

    open(LOG_FILE, "w", encoding="utf8").close()


def _write(level, section, message):
    now = datetime.now().strftime("%H:%M:%S")

    with open(LOG_FILE, "a", encoding="utf8") as file:
        file.write(
            f"[{now}] [{level}] [{section}] {message}\n"
        )


def info(section, message):
    _write("INFO", section, message)


def warning(section, message):
    _write("WARNING", section, message)


def error(section, message):
    _write("ERROR", section, message)


def debug(section, message):
    _write("DEBUG", section, message)