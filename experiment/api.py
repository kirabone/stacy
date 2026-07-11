import os
import json

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ")


MODEL = "llama-3.3-70b-versatile"

client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)


def messageGroq(history, system):

    messages = [
        {
            "role": "system",
            "content": system
        }
    ]

    # history should already be a list of {"role":..., "content":...}
    messages.extend(history)

    try:

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            response_format={"type": "json_object"},
            temperature=0
        )

    except Exception as e:

        print(e)
        return None

    try:

        return json.loads(response.choices[0].message.content)

    except json.JSONDecodeError:

        print("Model returned invalid JSON.")
        return None