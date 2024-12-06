def load_input():
    reports = []

    with open("input/02.txt", "r") as file:
        for line in file:
            levels = [
                int(level) for level in
                line.strip().split(" ")
            ]

            reports.append(levels)

    return reports


def pairs(items):
    for i in range(len(items) - 1):
        yield items[i], items[i + 1]


def are_increasing(numbers):
    return all(a < b for a, b in pairs(numbers))


def are_decerasing(numbers):
    return all(a > b for a, b in pairs(numbers))


def are_at_most_3_different(numbers):
    return all(abs(b - a) <= 3 for a, b in pairs(numbers))


def is_safe_report(levels):
    if not are_increasing(levels) and not are_decerasing(levels):
        return False

    if not are_at_most_3_different(levels):
        return False

    return True


reports = load_input()
safe_reports = list(filter(is_safe_report, reports))

print(len(safe_reports))
