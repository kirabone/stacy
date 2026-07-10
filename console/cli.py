from agent.router import message
from datetime import datetime 
from logs import logger

logger.start(f"google-{datetime.now()}")

while True:

    prompt = input(">")
    print(message(prompt))

    
    
    