from agent.googleapi import message
import json

while True:

    prompt = input(">")
    response = message(prompt)
    print(response["message"])
    