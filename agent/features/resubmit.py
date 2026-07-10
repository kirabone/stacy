from agent.config import actionList, RESUBMIT
from agent.message import message


def resubmit(response):

    try:

        interrogation = response["interrogation"]
        context = response["context"]

    except KeyError as e:

        return None

    print(interrogation)

    reply = input("> ")

    request = {
        "context": context,
        "interrogation": interrogation,
        "reply": reply,
        "available action": list(actionList.keys())
    }

    try:

        response = message(request, RESUBMIT)

    except Exception as e:

        return None

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