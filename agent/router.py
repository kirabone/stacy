from agent.config import SYSTEM, actionList, PERSONALITY
from agent.message import message


def router(prompt, system = SYSTEM + PERSONALITY):

    response = message(prompt,system)

    if response is None:
        return None

    if not isinstance(response, dict):
        return None

    if "action" not in response:
        return None

    action = response["action"]

    if action not in actionList:
        return None

    try:

        result = actionList[action](response)

    except Exception as e:

        return None

    return result