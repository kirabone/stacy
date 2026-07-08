import os
import json
from google import genai
from google.genai import types
from launcher.launchingEngine import launchExecutable
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_AI_STUDIO")

# Load the system instruction from your text file
with open("agent/system.txt", "r", encoding="utf-8") as file:
    SYSTEM = file.read()

# Disconnected model.txt — Hardcoded directly for Google Gemini API
MODEL = "gemini-2.5-flash"

def search(response=None): # Added parameter to match the function signature call
    return {"message": "Search not implemented."}

def launch(response):
    executable = response["executable"]
    app_id = launchExecutable(executable)
    return {
        "message": f"Launched {app_id}"
    }

def greet(response):
    greetings = response["greetings"]
    return {"message": greetings}

features = {
    "search": search,
    "launch": launch,
    "greet": greet
}

client = genai.Client(api_key=api_key)

def message(prompt):
    response = client.models.generate_content(
        model=MODEL,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM,
            # Forces Gemini to return valid, raw JSON directly
            response_mime_type="application/json", 
        ),
        contents=prompt,
    )

    print("Model response:", response.text)


    response_json = json.loads(response.text)

    action = response_json.get("action")

    if action not in features:
        raise ValueError(f"Unknown action: {action}")

    return features[action](response_json)