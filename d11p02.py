from functools import lru_cache
from math import log10, floor


def read_lines(path):
    with open(path, "r", encoding="utf-8") as stream:
        for line in stream:
            content = line.strip()

            if content:
                yield content


def freq(items):
    return {item: items.count(item) for item in set(items)}


def load_input():
    line = list(read_lines("input/11.txt"))[0]
    game = freq(list(map(int, line.split(" "))))

    return game


def transform(number):
    if number == 0:
        return [1]

    length = floor(log10(number) + 1)

    if length % 2 == 0:
        middle = length // 2
        a = floor(number / (10 ** middle))
        b = number - a * (10 ** middle)

        return [a, b]

    return [number * 2024]


def step(game):
    result = game.copy()

    for number in game:
        total = game[number]

        if total == 0:
            continue

        result[number] -= total
        transformed = transform(number)

        if len(transformed) == 1:
            a, = transformed

            result[a] = result.get(a, 0) + total
        else:
            a, b = transformed
            result[a] = result.get(a, 0) + total
            result[b] = result.get(b, 0) + total

    return result


game = load_input()

for i in range(75):
    game = step(game)

print(sum(game.values()))
