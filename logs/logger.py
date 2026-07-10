from datetime import datetime
from pathlib import Path
import json
import traceback

LOG_FILE = None
_DEPTH = 0


def start(name: str):
    global LOG_FILE

    Path("logs").mkdir(exist_ok=True)

    name = "".join(
        c if c not in '<>:"/\\|?*' else "_"
        for c in name
    )

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    LOG_FILE = Path("logs") / f"{name}-{timestamp}.log"
    LOG_FILE.touch()


def _timestamp():
    return datetime.now().strftime("%H:%M:%S")


def _indent():
    return "│   " * _DEPTH


def _write(level, section, message):

    if LOG_FILE is None:
        raise RuntimeError("LOGGER HAS NOT BEEN STARTED.")

    if not isinstance(message, str):
        try:
            message = json.dumps(message, indent=4, ensure_ascii=False)
        except Exception:
            message = repr(message)

    prefix = f"[{_timestamp()}] [{level}] [{section}] "

    with LOG_FILE.open("a", encoding="utf8") as file:

        if "\n" not in message:
            file.write(prefix + _indent() + message + "\n")
            return

        file.write(prefix + "\n")

        for line in message.splitlines():
            file.write(_indent() + line + "\n")

        file.write("\n")


# ---------- NORMAL LOGS ----------

def info(section, message):
    _write("INFO", section, message)


def warning(section, message):
    _write("WARNING", section, message)


def error(section, message):
    _write("ERROR", section, message)


def debug(section, message):
    _write("DEBUG", section, message)


# ---------- TRACE ----------

def enter(section, function):

    global _DEPTH

    _write("ENTER", section, f"{function}()")

    _DEPTH += 1


def exit(section, function):

    global _DEPTH

    _DEPTH = max(0, _DEPTH - 1)

    _write("EXIT", section, f"{function}()")


# ---------- SPECIAL ----------

def action(section, message):
    _write("ACTION", section, message)


def state(section, message):
    _write("STATE", section, message)


def input(section, title, data):
    _write("INPUT", section, f"{title}\n{data}")


def output(section, title, data):
    _write("OUTPUT", section, f"{title}\n{data}")


def lookup(section, message):
    _write("LOOKUP", section, message)


def match(section, message):
    _write("MATCH", section, message)


def returning(section, value):
    _write("RETURN", section, value)


def exception(section, exc):
    _write(
        "EXCEPTION",
        section,
        traceback.format_exc() if exc is None else str(exc)
    )


def divider():
    _write(
        "-----",
        "LOGGER",
        "=" * 80
    )