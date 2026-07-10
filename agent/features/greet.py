def greet(response):

    if response is None:
        return None

    if not isinstance(response, dict):
        return None

    if "message" not in response:
        return None

    return response["message"]