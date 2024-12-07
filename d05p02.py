from functools import cmp_to_key


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
                a, b = list(map(int, content.split("|")))
                dependencies[(a, b)] = -1
                dependencies[(b, a)] = 1
            else:
                updates.append(list(map(int, content.split(","))))

    return dependencies, updates


def build_compare(dependencies):
    return lambda a, b: dependencies[(a, b)] if (a, b) in dependencies else 0


depependencies, updates = load_input()
compare = build_compare(depependencies)
unordered = [
    update for update in updates
    if sorted(update, key=cmp_to_key(compare)) != update
]

ordered = [
    sorted(update, key=cmp_to_key(compare)) for update in unordered
]

numbers = map(lambda update: update[len(update) // 2], ordered)
result = sum(numbers)

print(result)
