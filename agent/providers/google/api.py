import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE")

with open("agent/providers/google/model.txt", "r", encoding="utf-8") as file:
    MODEL = file.read().strip()

client = genai.Client(api_key=api_key)

def messageGoogle(prompt , system):
    response = client.models.generate_content(
        model=MODEL,
        config=types.GenerateContentConfig(
            system_instruction=system,
            response_mime_type="application/json", 
        ),
        contents=prompt,
    )

    return json.loads(response.text)




