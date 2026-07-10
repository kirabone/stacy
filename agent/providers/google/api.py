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

def messageGoogle(prompt , system):
    try:
        response = client.models.generate_content(
            model=MODEL,
            config=types.GenerateContentConfig(
                system_instruction=system,
                response_mime_type="application/json", 
            ),
            contents=prompt,
        )

        logger.info(f"RESPONSE RECEIVED FROM GOOGLE AI. : {response}")

    except ResourceExhausted:
        logger.error("GOOGLE AI QUOTA OR RATE LIMIT EXCEEDED.")
        return None

    except NotFound:
        logger.error(f'MODEL "{MODEL}" WAS NOT FOUND.')
        return None

    except InvalidArgument as e:
        logger.error(f"INVALID REQUEST: {e}")
        return None

    except DeadlineExceeded:
        logger.error("GOOGLE AI REQUEST TIMED OUT.")
        return None

    except PermissionDenied:
        logger.error("PERMISSION DENIED. API KEY HAS NO ACCESS TO THIS MODEL.")
        return None

    except Unauthenticated:
        logger.error("AUTHENTICATION FAILED. INVALID OR MISSING API KEY.")
        return None

    except ServiceUnavailable:
        logger.error("GOOGLE AI SERVICE IS TEMPORARILY UNAVAILABLE.")
        return None

    except Exception as e:
        logger.exception(f"UNEXPECTED GOOGLE AI ERROR: {e}")
        return None

    logger.debug("PARSING JSON RESPONSE...")

    try:
        response = json.loads(response.text)
        logger.info("JSON PARSED SUCCESSFULLY.")

    except json.JSONDecodeError:
        logger.error("MODEL RETURNED INVALID JSON.")
        logger.debug(f"RAW RESPONSE:\n{response.text}")
        return None
     
    logger.debug("GOOGLE AI API", f"RESPONSE : {response}")
    if "action" in response:
        logger.info("GOOGLE AI API", f"DATA TRANSFERRED TO THE ROUTER : {response}")
    else:
        logger.info("GOOGLE AI API", f"DATA TRANSFERRED TO THE MESSAGES : {response}")
    return response




