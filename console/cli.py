from agent.router import message

while True:

    prompt = input(">")
    response = message(prompt)
    
    