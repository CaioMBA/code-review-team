from datetime import date


def days_between(start: date, end: date) -> int:
    """Whole days from start to end (negative if end is before start)."""
    return (end - start).days
