from agent.config import PROVIDER, providerList, PERSONALITY


def message(prompt, system):

    try:

        response = providerList[PROVIDER](
            prompt,
            system + PERSONALITY
        )

    except Exception as e:

        raise

    if response is None:
        return None

    return response