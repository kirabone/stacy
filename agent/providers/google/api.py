import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv
from logs import logger
from agent.config import actionList
from google.api_core.exceptions import (
    ResourceExhausted,
    NotFound,
    InvalidArgument,
    DeadlineExceeded,
    PermissionDenied,
    Unauthenticated,
    ServiceUnavailable,
)

load_dotenv()

api_key = os.getenv("GOOGLE")

with open("agent/providers/google/model.txt", "r", encoding="utf-8") as file:
    MODEL = file.read().strip()

client = genai.Client(api_key=api_key)

def messageGoogle(prompt, system):

    logger.enter("GOOGLE", "messageGoogle")

    logger.state(
        "GOOGLE",
        f'USING MODEL "{MODEL}".'
    )

    logger.output(
        "GOOGLE",
        "SYSTEM PROMPT",
        system
    )

    logger.output(
        "GOOGLE",
        "USER PROMPT",
        prompt
    )

    logger.action(
        "GOOGLE",
        "SENDING REQUEST TO GOOGLE AI."
    )

    try:

        response = client.models.generate_content(
            model=MODEL,
            config=types.GenerateContentConfig(
                system_instruction=system,
                response_mime_type="application/json",
            ),
            contents=prompt,
        )

    except ResourceExhausted:

        logger.error(
            "GOOGLE",
            "GOOGLE AI QUOTA OR RATE LIMIT EXCEEDED."
        )

        logger.exit("GOOGLE", "messageGoogle")

        return None

    except NotFound:

        logger.error(
            "GOOGLE",
            f'MODEL "{MODEL}" WAS NOT FOUND.'
        )

        logger.exit("GOOGLE", "messageGoogle")

        return None

    except InvalidArgument as e:

        logger.exception(
            "GOOGLE",
            e
        )

        logger.exit("GOOGLE", "messageGoogle")

        return None

    except DeadlineExceeded:

        logger.error(
            "GOOGLE",
            "REQUEST TIMED OUT."
        )

        logger.exit("GOOGLE", "messageGoogle")

        return None

    except PermissionDenied:

        logger.error(
            "GOOGLE",
            "PERMISSION DENIED."
        )

        logger.exit("GOOGLE", "messageGoogle")

        return None

    except Unauthenticated:

        logger.error(
            "GOOGLE",
            "AUTHENTICATION FAILED."
        )

        logger.exit("GOOGLE", "messageGoogle")

        return None

    except ServiceUnavailable:

        logger.error(
            "GOOGLE",
            "SERVICE UNAVAILABLE."
        )

        logger.exit("GOOGLE", "messageGoogle")

        return None

    except Exception as e:

        logger.exception(
            "GOOGLE",
            e
        )

        logger.exit("GOOGLE", "messageGoogle")

        return None

    logger.output(
        "GOOGLE",
        "RAW RESPONSE",
        response.text
    )

    logger.action(
        "GOOGLE",
        "PARSING JSON RESPONSE."
    )

    try:

        response = json.loads(response.text)

    except json.JSONDecodeError:

        logger.error(
            "GOOGLE",
            "MODEL RETURNED INVALID JSON."
        )

        logger.output(
            "GOOGLE",
            "INVALID RESPONSE",
            response.text
        )

        logger.exit("GOOGLE", "messageGoogle")

        return None

    logger.output(
        "GOOGLE",
        "PARSED RESPONSE",
        response
    )

    if "action" in response:

        logger.action(
            "GOOGLE",
            "ROUTING RESPONSE TO ROUTER."
        )

    else:

        logger.action(
            "GOOGLE",
            "RETURNING RESPONSE TO CALLER."
        )

    logger.returning(
        "GOOGLE",
        response
    )

    logger.exit(
        "GOOGLE",
        "messageGoogle"
    )

    return response



