# INSS 2026 rates for CLT employees
INSS_RATES = [(1518.00, 0.075), (2793.88, 0.09), (4190.83, 0.12), (8157.41, 0.14)]


def gross(hours, rate):
    return round(hours * rate, 2)


def inss(salary):
    for limit, rate in INSS_RATES:
        if salary <= limit:
            return round(salary * rate, 2)
    return round(salary * 0.14, 2)


def net(salary):
    return round(salary - inss(salary), 2)