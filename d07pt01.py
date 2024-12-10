def load_input():
    values = []

    with open("input/07.txt") as stream:
        for line in stream:
            content = line.strip()

            if not content:
                continue

            value, rest = content.split(":")
            value = int(value)
            rest = rest.strip()

            factors = list(map(int, rest.split(" ")))

            values.append((value, factors))

    return values


operations = set(["+", "*"])


def variations(items, k):
    if k == 0:
        yield []
        return

    for item in items:
        for rest in variations(items, k - 1):
            yield [item] + rest


def interpret(factors, operations):
    result = factors[0]

    for index, operation in enumerate(operations):
        if operation == "+":
            result += factors[index + 1]
        elif operation == "*":
            result *= factors[index + 1]

    return result


class FactorizationError(Exception):
    pass


def factorize(value, factors):
    for factorization in variations(operations, len(factors) - 1):
        result = interpret(factors, factorization)

        if result == value:
            return factorization

    raise FactorizationError


values = load_input()
total = 0

for value, factors in values:
    try:
        factorization = factorize(value, factors)
        total += value
    except FactorizationError:
        continue

print(total)
