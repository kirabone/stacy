from agent.config import LAUNCH
from agent.message import message

import subprocess
import json


def launch(response):

    ps = r"""
    Get-StartApps |
        Select-Object Name, AppID |
        ConvertTo-Json -Depth 3
    """

    result = subprocess.run(
        ["powershell", "-NoProfile", "-Command", ps],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return "FAILED TO RETRIEVE INSTALLED APPLICATIONS."

    try:

        executables = json.loads(result.stdout)

    except json.JSONDecodeError:

        return "FAILED TO PARSE APPLICATION LIST."

    prompt = {
        "prompt": response["prompt"],
        "applications": executables
    }

    try:

        response = message(prompt, LAUNCH)

    except Exception as e:

        return "AI REQUEST FAILED."

    if response is None:
        return "NO RESPONSE FROM AI."

    if not isinstance(response, dict):
        return "INVALID AI RESPONSE."

    if "command" not in response:
        return response.get("message", "NO COMMAND RETURNED.")

    command = response["command"]

    if not command:
        return response.get("message", "EMPTY COMMAND.")

    valid = {app["AppID"] for app in executables}

    if command not in valid:
        return response.get("message", "APPLICATION NOT FOUND.")

    result = subprocess.run(
        [
            "explorer.exe",
            f"shell:AppsFolder\\{command}"
        ],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return response.get(
            "message",
            "FAILED TO LAUNCH APPLICATION."
        )

    return response.get("message", "DONE.")