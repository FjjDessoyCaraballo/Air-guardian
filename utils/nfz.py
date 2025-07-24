import os

def authenticate(secret: str):
    if not secret or secret != os.environ["X-SECRET"]:
        return False
    return True