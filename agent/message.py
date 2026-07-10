from agent.config import PROVIDER, providerList, PERSONALITY
from logs import logger


def message(prompt, system):

    logger.enter("MESSAGE", "message")

    logger.state(
        "MESSAGE",
        f'ACTIVE PROVIDER : "{PROVIDER}"'
    )

    logger.output(
        "MESSAGE",
        "SYSTEM PROMPT",
        system
    )

    logger.output(
        "MESSAGE",
        "PERSONALITY PROMPT",
        PERSONALITY
    )

    logger.input(
        "MESSAGE",
        "USER PROMPT",
        prompt
    )

    logger.action(
        "MESSAGE",
        f'SENDING REQUEST TO PROVIDER "{PROVIDER}".'
    )

    try:

        response = providerList[PROVIDER](
            prompt,
            system + PERSONALITY
        )

    except Exception as e:

        logger.exception(
            "MESSAGE",
            e
        )

        logger.exit(
            "MESSAGE",
            "message"
        )

        raise

    logger.output(
        "MESSAGE",
        "RAW PROVIDER RESPONSE",
        response
    )

    if response is None:

        logger.error(
            "MESSAGE",
            "PROVIDER RETURNED NO RESPONSE."
        )

        logger.exit(
            "MESSAGE",
            "message"
        )

        return None

    logger.returning(
        "MESSAGE",
        response
    )

    logger.exit(
        "MESSAGE",
        "message"
    )

    return response