def date_diff_days(a, b):
    return (b - a).days


def monthly_summary(tickets):
    lines = []
    for t in tickets:
        open_days = date_diff_days(t["opened"], t["closed"])
        lines.append(f"#{t['id']} {t['title']} ({open_days} days open)")
    return "\n".join(lines)
