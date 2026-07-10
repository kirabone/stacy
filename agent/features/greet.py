from logs import logger


def greet(response):

    logger.enter("GREET", "greet")

    logger.input(
        "GREET",
        "REQUEST RECEIVED",
        response
    )

    if response is None:

        logger.error(
            "GREET",
            "RESPONSE WAS NONE."
        )

        logger.exit("GREET", "greet")

        return None

    if not isinstance(response, dict):

        logger.error(
            "GREET",
            "RESPONSE WAS NOT A DICTIONARY."
        )

        logger.exit("GREET", "greet")

        return None

    if "message" not in response:

        logger.error(
            "GREET",
            'RESPONSE DID NOT CONTAIN "MESSAGE".'
        )

        logger.exit("GREET", "greet")

        return None

    logger.state(
        "GREET",
        "MESSAGE FIELD VERIFIED."
    )

    logger.returning(
        "GREET",
        response["message"]
    )

    logger.exit(
        "GREET",
        "greet"
    )

    return response["message"]