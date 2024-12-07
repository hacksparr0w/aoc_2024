def load_input():
    dependencies = {}
    updates = []

    with open("input/05.txt") as stream:
        reading_updates = False

        for line in stream:
            content = line.strip()

            if not content:
                reading_updates = True
                continue

            if not reading_updates:
                dependency, dependant = list(map(int, content.split("|")))
                dependencies.setdefault(dependant, []).append(dependency)
            else:
                updates.append(list(map(int, content.split(","))))

    return dependencies, updates


def check_dependencies(update, needed, satisfied):
    for dependency in needed:
        if dependency in update and dependency not in satisfied:
            return False

    return True


def check_order(dependencies, update):
    pages = []

    for page in update:
        if not check_dependencies(update, dependencies.get(page, []), pages):
            return False

        pages.append(page)

    return True

dependencies, updates = load_input()
ordered = filter(
    lambda update: check_order(dependencies, update),
    updates
)

numbers = map(
    lambda update: update[len(update) // 2],
    ordered
)

result = sum(numbers)

print(result)
