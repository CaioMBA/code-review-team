def normalize_email(email):
    return email.strip().lower()


def format_price(cents):
    return f"${cents / 100:.2f}"
