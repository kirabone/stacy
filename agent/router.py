from agent.config import PROVIDER , SYSTEM, providerList, actionList, PERSONALITY
from logs import logger

def message(prompt):

    response = providerList[PROVIDER](prompt, SYSTEM + PERSONALITY)
    if response is None:
        logger.error("NO VALID RESPONSE RECEIVED FROM GOOGLE PROVIDER.")
        return None
    try :
        action = response["action"]
    except TypeError:
        logger.error("ROUTER RECEIVED AN INVALID RESPONSE. EXPECTED A DICTIONARY.")
        return None

    except KeyError:
        logger.error('ROUTER RECEIVED A DICTIONARY WITHOUT THE "ACTION" FIELD.')
        return None
    
    try:
        return actionList[action](response)

    except TypeError:
        logger.error("ACTION MAPPING RECEIVED AN INVALID ARGUMENT.")
        return None

    except KeyError:
        logger.error(f'NO FUNCTION MAPPED FOR ACTION "{action}".')
        return None

    except Exception as e:
        logger.exception(f"UNEXPECTED ROUTER ERROR: {e}")
        return None
        
