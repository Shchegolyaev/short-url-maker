import secrets
import string


def create_unique_random_key() -> str:
    chars = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(chars) for _ in range(10))
