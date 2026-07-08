from ollama import chat
import json
from launcher.launchingEngine import launchExecutable

with open("agent/system.txt", "r", encoding="utf-8") as file:
    SYSTEM = file.read()

with open("agent/model.txt", "r", encoding="utf-8") as file:
    MODEL = file.read()

def search():
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

def message(prompt):

    response = chat(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": SYSTEM,
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    
    response = json.loads(response["message"]["content"])

    print(response)
    action = response.get("action")

    if action not in features:
        raise ValueError(f"Unknown action: {action}")

    return features[action](response)