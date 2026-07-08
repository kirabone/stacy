from agent.features.launch import launch
from agent.features.greet import greet
from agent.config import PROVIDER , SYSTEM
from agent.config import providers

actions = {
    "launch" : launch,
    "greet" : greet,
}

def message(prompt):

    response = providers[PROVIDER](prompt, SYSTEM)
    action = response["action"]
    actions[action](response)


