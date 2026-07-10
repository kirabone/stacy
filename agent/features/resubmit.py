from agent.config import actionList, RESUBMIT
from agent.message import message
from logs import logger


def resubmit(response):

    logger.enter("RESUBMIT", "resubmit")

    logger.input(
        "RESUBMIT",
        "REQUEST RECEIVED",
        response
    )

    try:

        interrogation = response["interrogation"]
        context = response["context"]

    except KeyError as e:

        logger.error(
            "RESUBMIT",
            f'MISSING REQUIRED FIELD "{e.args[0]}".'
        )

        logger.exit("RESUBMIT", "resubmit")

        return None

    logger.state(
        "RESUBMIT",
        "EXTRACTED CONTEXT AND INTERROGATION."
    )

    logger.action(
        "RESUBMIT",
        "DISPLAYING INTERROGATION TO USER."
    )

    print(interrogation)

    logger.action(
        "RESUBMIT",
        "WAITING FOR USER INPUT."
    )

    reply = input("> ")

    logger.input(
        "USER",
        "USER REPLY",
        reply
    )

    request = {
        "context": context,
        "interrogation": interrogation,
        "reply": reply,
        "available action": list(actionList.keys())
    }

    logger.output(
        "AI",
        "REQUEST",
        request
    )

    logger.action(
        "AI",
        "REQUESTING NEXT ACTION."
    )

    try:

        response = message(request, RESUBMIT)

    except Exception as e:

        logger.exception(
            "AI",
            e
        )

        logger.exit("RESUBMIT", "resubmit")

        return None

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

        logger.exit("RESUBMIT", "resubmit")

        return None

    if not isinstance(response, dict):

        logger.error(
            "AI",
            "AI RESPONSE WAS NOT A DICTIONARY."
        )

        logger.exit("RESUBMIT", "resubmit")

        return None

    if "action" not in response:

        logger.error(
            "AI",
            'RESPONSE DID NOT CONTAIN "ACTION".'
        )

        logger.exit("RESUBMIT", "resubmit")

        return None

    action = response["action"]

    logger.state(
        "AI",
        f'ACTION RECEIVED: "{action}"'
    )

    logger.lookup(
        "ROUTER",
        f'SEARCHING ACTION TABLE FOR "{action}".'
    )

    if action not in actionList:

        logger.error(
            "ROUTER",
            f'NO FUNCTION MAPPED TO "{action}".'
        )

        logger.exit("RESUBMIT", "resubmit")

        return None

    logger.match(
        "ROUTER",
        f'FOUND HANDLER FOR "{action}".'
    )

    logger.action(
        "ROUTER",
        f'TRANSFERRING CONTROL TO "{action}".'
    )

    try:

        result = actionList[action](response)

    except Exception as e:

        logger.exception(
            "ROUTER",
            e
        )

        logger.exit("RESUBMIT", "resubmit")

        return None

    logger.returning(
        "RESUBMIT",
        result
    )

    logger.exit(
        "RESUBMIT",
        "resubmit"
    )

    return result