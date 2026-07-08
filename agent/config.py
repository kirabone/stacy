from pathlib import Path
import json

CONFIG_PATH = Path(__file__).parent / "config.json"

with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    CONFIG = json.load(f)

with open("agent/system/system.txt", "r", encoding="utf-8") as file:
    SYSTEM = file.read()

with open("agent/system/launch.txt", "r", encoding="utf-8") as file:
    LAUNCH = file.read()

PROVIDER = CONFIG["provider"]
