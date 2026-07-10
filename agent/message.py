from agent.config import PROVIDER, providerList, PERSONALITY
from logs import logger

def message(prompt, system):
    logger.info("MESSAGE", f"AGENT'S PROMPT : {prompt}")
    try:
        response = providerList[PROVIDER](prompt, system + PERSONALITY)
    except Exception as e:
        logger.error("MESSAGE", f"CANNOT GET THE RESPONSE FROM THE MODEL : {e}")
        raise
    logger.debug("MESSAGE", response)
    return response

