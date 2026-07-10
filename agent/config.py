from pathlib import Path
import json
import importlib

with open("agent/system/system.txt", "r", encoding="utf-8") as file:
    SYSTEM = file.read()

with open("agent/system/launch.txt", "r", encoding="utf-8") as file:
    LAUNCH = file.read()

with open("agent/system/resubmit.txt", "r", encoding="utf-8") as file:
    RESUBMIT = file.read()

with open("agent/system/personality.txt", "r", encoding="utf-8") as file:
    PERSONALITY = file.read()

PROVIDER = "groq"

def providers(module_name, function_name):
    def wrapper(*args, **kwargs):
        module = importlib.import_module(
            f"agent.providers.{module_name}.api"
        )
        function = getattr(module, function_name)
        return function(*args, **kwargs)

    return wrapper


providerList = {
    "google": providers("google", "messageGoogle"),
    "groq": providers("groq", "messageGroq"),
}


def actions(name):
    def wrapper(*args, **kwargs):
        module = importlib.import_module(
            f"agent.features.{name}"
        )
        function = getattr(module, name)
        return function(*args, **kwargs)

    return wrapper


actionList = {
    "greet": actions("greet"),
    "launch": actions("launch"),
    "resubmit" : actions("resubmit"),
    "exit" : actions("exit")
}