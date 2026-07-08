from agent.config import PROVIDER, providers

def message(prompt, system):

    response = providers[PROVIDER](prompt, system)
    return response

