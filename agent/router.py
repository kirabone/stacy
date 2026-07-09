from agent.config import PROVIDER , SYSTEM, providerList, actionList, PERSONALITY

def message(prompt):

    response = providerList[PROVIDER](prompt, SYSTEM + PERSONALITY)
    action = response["action"]
    return actionList[action](response)

