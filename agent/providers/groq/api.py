import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ")

with open("agent/providers/groq/model.txt", "r", encoding="utf-8") as file:
    MODEL = file.read().strip()

client = Groq(api_key=api_key)

def messageGroq(prompt, system):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": system
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        response_format={"type": "json_object"},
        temperature=0
    )

    return json.loads(response.choices[0].message.content)