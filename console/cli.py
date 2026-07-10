from agent.router import router
from datetime import datetime
from logs import logger

logger.start("google")


while True:

    logger.divider()

    logger.info(
        "TRANSCRIPT",
        f"NEW CONVERSATION TURN | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    try :
        prompt = input("> ")
    except KeyboardInterrupt:
        print("bye ")
        break

    logger.input(
        "USER",
        "PROMPT",
        prompt
    )

    logger.enter(
        "ROUTER",
        "message"
    )

    response = router(prompt)
    try:
        if response["action"] == "exit":
            print(response["message"])
            break
    except Exception as e:
        pass

    logger.exit(
        "ROUTER",
        "message"
    )

    logger.output(
        "ASSISTANT",
        "FINAL RESPONSE",
        response
    )

    print(response)

    logger.returning(
        "TRANSCRIPT",
        "TURN COMPLETE"
    )
    