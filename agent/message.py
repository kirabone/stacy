from agent.config import PROVIDER, providerList, PERSONALITY

def message(prompt, system):

    response = providerList[PROVIDER](prompt, system + PERSONALITY)
    return response

