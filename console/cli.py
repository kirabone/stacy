from agent.router import router
from agent.config import providerList, PROVIDER 


while True:

    try :
        prompt = input("> ")
    except KeyboardInterrupt:
        print("bye ")
        break

    response = router(prompt)
    try:
        if response["action"] == "exit":
            print(response["message"])
            break
    except Exception as e:
        pass

    print(response)