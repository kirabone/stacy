from agent.config import LAUNCH
from agent.message import message
from logs import logger

import subprocess
import json


def launch(response):

    logger.enter("LAUNCH", "launch")

    logger.input(
        "LAUNCH",
        "REQUEST RECEIVED",
        response
    )

    ps = r"""
    Get-StartApps |
        Select-Object Name, AppID |
        ConvertTo-Json -Depth 3
    """

    logger.action(
        "POWERSHELL",
        "REQUESTING INSTALLED APPLICATIONS."
    )

    result = subprocess.run(
        ["powershell", "-NoProfile", "-Command", ps],
        capture_output=True,
        text=True
    )

    logger.output(
        "POWERSHELL",
        "RAW RESULT",
        {
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }
    )

    if result.returncode != 0:
        logger.error(
            "POWERSHELL",
            "FAILED TO EXECUTE POWERSHELL COMMAND."
        )

        logger.returning(
            "LAUNCH",
            "FAILED TO RETRIEVE APPLICATIONS."
        )

        logger.exit("LAUNCH", "launch")
        return "FAILED TO RETRIEVE INSTALLED APPLICATIONS."

    logger.action(
        "POWERSHELL",
        "PARSING JSON OUTPUT."
    )

    try:

        executables = json.loads(result.stdout)

    except json.JSONDecodeError:

        logger.error(
            "POWERSHELL",
            "POWERSHELL OUTPUT WAS NOT VALID JSON."
        )

        logger.output(
            "POWERSHELL",
            "INVALID OUTPUT",
            result.stdout
        )

        logger.exit("LAUNCH", "launch")

        return "FAILED TO PARSE APPLICATION LIST."

    logger.state(
        "LAUNCH",
        f"RETRIEVED {len(executables)} APPLICATIONS."
    )

    prompt = {
        "prompt": response["prompt"],
        "applications": executables
    }

    logger.output(
        "AI",
        "REQUEST",
        prompt
    )

    logger.action(
        "AI",
        "REQUESTING APPLICATION MATCH."
    )

    try:

        response = message(prompt, LAUNCH)

    except Exception as e:

        logger.exception(
            "AI",
            e
        )

        logger.exit("LAUNCH", "launch")

        return "AI REQUEST FAILED."

    logger.output(
        "AI",
        "RESPONSE",
        response
    )

    if response is None:

        logger.error(
            "AI",
            "AI RETURNED NO RESPONSE."
        )

        logger.exit("LAUNCH", "launch")

        return "NO RESPONSE FROM AI."

    if not isinstance(response, dict):

        logger.error(
            "AI",
            "AI RESPONSE WAS NOT A DICTIONARY."
        )

        logger.exit("LAUNCH", "launch")

        return "INVALID AI RESPONSE."

    if "message" not in response:

        logger.warning(
            "AI",
            'RESPONSE DID NOT CONTAIN "MESSAGE".'
        )

    if "command" not in response:

        logger.error(
            "AI",
            'RESPONSE DID NOT CONTAIN "COMMAND".'
        )

        logger.exit("LAUNCH", "launch")

        return response.get("message", "NO COMMAND RETURNED.")

    command = response["command"]

    logger.state(
        "AI",
        f'COMMAND RECEIVED: "{command}"'
    )

    if not command:

        logger.error(
            "AI",
            "COMMAND WAS EMPTY."
        )

        logger.exit("LAUNCH", "launch")

        return response.get("message", "EMPTY COMMAND.")

    logger.lookup(
        "LAUNCH",
        "VERIFYING APP ID EXISTS."
    )

    valid = {app["AppID"] for app in executables}

    if command not in valid:

        logger.error(
            "LAUNCH",
            f'UNKNOWN APP ID "{command}".'
        )

        logger.returning(
            "LAUNCH",
            "APPLICATION NOT FOUND."
        )

        logger.exit("LAUNCH", "launch")

        return response.get("message", "APPLICATION NOT FOUND.")

    logger.match(
        "LAUNCH",
        f'VALID APP ID "{command}" FOUND.'
    )

    logger.action(
        "LAUNCH",
        f'EXECUTING APP "{command}".'
    )

    result = subprocess.run(
        [
            "explorer.exe",
            f"shell:AppsFolder\\{command}"
        ],
        capture_output=True,
        text=True
    )

    logger.output(
        "LAUNCH",
        "WINDOWS RESPONSE",
        {
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }
    )

    if result.returncode != 0:

        logger.error(
            "LAUNCH",
            f'FAILED TO EXECUTE "{command}".'
        )

        logger.exit("LAUNCH", "launch")

        return response.get(
            "message",
            "FAILED TO LAUNCH APPLICATION."
        )

    logger.returning(
        "LAUNCH",
        response.get("message", "DONE.")
    )

    logger.exit(
        "LAUNCH",
        "launch"
    )

    return response.get("message", "DONE.")