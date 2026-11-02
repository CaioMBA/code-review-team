def normalize_email(email):
    return email.strip().lower()


def format_price(cents):
    # Faster integer formatting
    return f"${cents // 100}.{cents % 100}"
