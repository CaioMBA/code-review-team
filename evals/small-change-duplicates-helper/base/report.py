def monthly_summary(tickets):
    lines = []
    for t in tickets:
        lines.append(f"#{t['id']} {t['title']}")
    return "\n".join(lines)
