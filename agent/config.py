from pathlib import Path
import json
from agent.providers.google.api import messageGoogle
from agent.providers.groq.api import messageGroq

with open("agent/system/system.txt", "r", encoding="utf-8") as file:
    SYSTEM = file.read()

with open("agent/system/launch.txt", "r", encoding="utf-8") as file:
    LAUNCH = file.read()

PROVIDER = "groq"

providers = {
    "google" : messageGoogle,
    "groq" : messageGroq
}
