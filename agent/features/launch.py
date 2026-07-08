from agent.config import LAUNCH
from launcher.launchingEngine import launchExecutable
from agent.message import message

def launch(response):

    prompt = response["prompt"]

    response = message(prompt, LAUNCH)
    executable = response["app"]
    return launchExecutable(executable)



