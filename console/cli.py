from agent.router import message
import json

provider = input("provider>")

while True:

    prompt = input(">")
    response = message(provider, prompt)
    print(response["message"])
    