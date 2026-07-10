from agent.config import actionList, RESUBMIT
from agent.message import message
import json

def resubmit(response):
    response = response
    print(response["interrogation"])
    reply = input(">")
    request = {
        "context" : response["context"],
        "interrogation" : response["interrogation"],
        "reply" : reply,
        "available action" : list(actionList.keys())
    }
    
    response = message(request, RESUBMIT)
    return actionList[action](response)