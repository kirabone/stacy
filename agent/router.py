from launcher.launchingEngine import launchExecutable
from agent.providers.google.api import messageGoogle
from agent.providers.groq.api import messageGroq

with open("agent/shared/system.txt", "r", encoding="utf-8") as file:
    SYSTEM = file.read()


def search(response=None):
    return {"message": "Search not implemented."}


def launch(response):
    executable = response["executable"]
    app_id = launchExecutable(executable)
    return {
        "message": f"Launched {app_id}"
    }


def greet(response):
    greetings = response["greetings"]
    return {
        "message": greetings
    }


def infoNeeded(provider, response):
    interogation = response["interogation"]
    context = response["context"]

    print(interogation)
    info = input("> ")

    prompt = {
        "context": context,
        "info": info
    }

    return message(provider, prompt)


providers = {
    "google": messageGoogle,
    "groq": messageGroq
}


features = {
    "search": search,
    "launch": launch,
    "greet": greet,
}


def message(provider, prompt):

    response = providers[provider](prompt, SYSTEM)

    action = response["action"]

    if action == "continue":
        return infoNeeded(provider, response)

    return features[action](response)