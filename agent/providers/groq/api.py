import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from logs import logger

load_dotenv()

api_key = os.getenv("GROQ")

with open("agent/providers/groq/model.txt", "r", encoding="utf-8") as file:
    MODEL = file.read().strip()

client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)

def messageGroq(prompt, system):

    logger.enter("GROQ", "messageGroq")

    logger.state(
        "GROQ",
        f'USING MODEL "{MODEL}".'
    )

    logger.output(
        "GROQ",
        "SYSTEM PROMPT",
        system
    )

    logger.output(
        "GROQ",
        "USER PROMPT",
        prompt
    )

    logger.action(
        "GROQ",
        "SENDING REQUEST TO GROQ."
    )

    try:

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": system
                },
                {
                    "role": "user",
                    "content": prompt if isinstance(prompt, str) else json.dumps(prompt)
                }
            ],
            response_format={"type": "json_object"},
            temperature=0
        )

    except Exception as e:

        logger.exception(
            "GROQ",
            e
        )

        logger.exit(
            "GROQ",
            "messageGroq"
        )

        return None

    raw = response.choices[0].message.content

    logger.output(
        "GROQ",
        "RAW RESPONSE",
        raw
    )

    logger.action(
        "GROQ",
        "PARSING JSON RESPONSE."
    )

    try:

        response = json.loads(raw)

    except json.JSONDecodeError:

        logger.error(
            "GROQ",
            "MODEL RETURNED INVALID JSON."
        )

        logger.output(
            "GROQ",
            "INVALID RESPONSE",
            raw
        )

        logger.exit(
            "GROQ",
            "messageGroq"
        )

        return None

    logger.output(
        "GROQ",
        "PARSED RESPONSE",
        response
    )

    if "action" in response:

        logger.action(
            "GROQ",
            "ROUTING RESPONSE TO ROUTER."
        )

    else:

        logger.action(
            "GROQ",
            "RETURNING RESPONSE TO CALLER."
        )

    logger.returning(
        "GROQ",
        response
    )

    logger.exit(
        "GROQ",
        "messageGroq"
    )

    return response