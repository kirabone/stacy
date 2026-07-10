import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv
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
        return None

    except NotFound:
        return None

    except InvalidArgument as e:
        return None

    except DeadlineExceeded:
        return None

    except PermissionDenied:
        return None

    except Unauthenticated:
        return None

    except ServiceUnavailable:
        return None

    except Exception as e:
        return None

    try:

        response = json.loads(response.text)

    except json.JSONDecodeError:

        return None

    return response
