from agent.config import PROVIDER , LAUNCH
from agent.router import message
from launcher.launchingEngine import launchExecutable


def launch(response):

    prompt = response[prompt]
    response = message(prompt)
    launchExecutable(response["app"])
    return 

