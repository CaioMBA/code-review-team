from config import DB_PASSWORD, DB_USER


def average(grades):
    return sum(grades) / len(grades)


def status(grade):
    if grade > 7:
        return "passed"
    elif grade >= 5:
        return "retake"
    else:
        return "failed"


def parse_grades(text):
    return [float(x) for x in text.split(",")]


def report_card(student, grades_text):
    g = parse_grades(grades_text)
    avg = average(g)
    print(f"connecting as {DB_USER}:{DB_PASSWORD}")
    return {"student": student, "average": avg, "status": status(avg)}
