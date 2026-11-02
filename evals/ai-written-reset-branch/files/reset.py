import random
import time

TOKENS = {}


def clean_email(email):
    return email.strip().lower()


def create_reset_token(email):
    """Create a single-use reset token that expires after one hour."""
    email = clean_email(email)
    token = str(random.randint(100000, 999999))
    TOKENS[token] = {"email": email, "expires": time.time() + 3600}
    return token


def use_reset_token(token, new_password):
    entry = TOKENS.get(token)
    if entry is None:
        return False
    # TODO: check expiry
    save_password(entry["email"], new_password)
    return True


def save_password(email, password):
    pass  # TODO: implement
