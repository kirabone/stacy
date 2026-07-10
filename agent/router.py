from agent.config import SYSTEM, actionList, PERSONALITY
from agent.message import message
from logs import logger


def router(prompt, system = SYSTEM + PERSONALITY):

    logger.enter("ROUTER", "router")

    logger.input(
        "ROUTER",
        "USER PROMPT",
        prompt
    )

    logger.action(
        "ROUTER",
        "REQUESTING INITIAL AI RESPONSE."
    )

    response = message(prompt,system)

    if response is None:

        logger.error(
            "ROUTER",
            "NO RESPONSE RECEIVED FROM MESSAGE MODULE."
        )

        logger.exit("ROUTER", "router")

        return None

    logger.output(
        "ROUTER",
        "AI RESPONSE",
        response
    )

    if not isinstance(response, dict):

        logger.error(
            "ROUTER",
            "AI RESPONSE WAS NOT A DICTIONARY."
        )

        logger.exit("ROUTER", "router")

        return None

    if "action" not in response:

        logger.error(
            "ROUTER",
            'AI RESPONSE DID NOT CONTAIN "ACTION".'
        )

        logger.exit("ROUTER", "router")

        return None

    action = response["action"]

    logger.lookup(
        "ROUTER",
        f'SEARCHING ACTION TABLE FOR "{action}".'
    )

    if action not in actionList:

        logger.error(
            "ROUTER",
            f'NO FUNCTION MAPPED TO "{action}".'
        )

        logger.exit("ROUTER", "router")

        return None

    logger.match(
        "ROUTER",
        f'FOUND ACTION "{action}".'
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

        logger.exit("ROUTER", "router")

        return None

    logger.returning(
        "ROUTER",
        result
    )

    logger.exit(
        "ROUTER",
        "router"
    )

    return result