from launcher.launchingEngine import launchExecutable
from agent.providers.google.api import messageGoogle
from agent.providers.groq.api import messageGroq


with open("agent/shared/system.txt", "r", encoding="utf-8") as file:
    SYSTEM = file.read()

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

providers = {
    "google" : messageGoogle,
    "groq" : messageGroq
}

def message(provider, prompt):

    global SYSTEM
    response = providers[provider](prompt, SYSTEM)

    action = response["action"]

    return features[action](response)  

    


