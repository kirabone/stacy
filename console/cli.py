from agent.api import message
import json

while True:

    prompt = input(">")
    response = message(prompt)
    print(response["message"])
    