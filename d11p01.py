def read_lines(path):
    with open(path, "r", encoding="utf-8") as stream:
        for line in stream:
            content = line.strip()

            if content:
                yield content


def load_input():
    line = list(read_lines("input/11.txt"))[0]
    game = list(map(int, line.split(" ")))

    return game


def transform(number):
    if number == 0:
        return [1]

    text = str(number)

    if len(text) % 2 == 0:
        middle = len(text) // 2
        return [int(text[:middle]), int(text[middle:])]

    return [number * 2024]


def flatten(items):
    for outer in items:
        for inner in outer:
            yield inner


def step(game):
    return list(flatten(map(transform, game)))


game = load_input()

for i in range(25):
    game = step(game)
    #print(game)

print(len(game))
