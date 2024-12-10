from dataclasses import dataclass
from math import sqrt


Position = tuple[int, int]


@dataclass
class Antenna:
    type: str
    position: Position

    def __hash__(self):
        return hash(self.type) ^ hash(self.position)


@dataclass
class Level:
    dimensions: tuple[int, int]
    antennas: set[Antenna]


def read_lines(path):
    with open(path, "r", encoding="utf-8") as stream:
        for line in stream:
            content = line.strip()

            if content:
                yield content


def load_input():
    lines = list(read_lines("input/08.txt"))
    dimensions = len(lines), len(lines[0])
    antennas = set()

    for row, line in enumerate(lines):
        for column, character in enumerate(line):
            if character == ".":
                continue

            position = (row, column)
            antennas.add(Antenna(character, position))

    return Level(dimensions, antennas)


def cross_product(xs, ys):
    for x in xs:
        for y in ys:
            yield x, y


def pair_antennas(antennas):
    for a, b in cross_product(antennas, antennas):
        if a.type != b.type:
            continue

        if a.position == b.position:
            continue

        yield a, b


def l1_dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def trace_line(level, a, b):
    dx = b[1] - a[1]
    dy = b[0] - a[0]

    x = a[1]
    y = a[0]

    while True:
        yield y, x

        x += dx
        y += dy

        if x < 0 or x >= level.dimensions[1] or \
            y < 0 or y >= level.dimensions[0]:
            
            break

    x = a[1]
    y = a[0]

    while True:
        x -= dx
        y -= dy

        if x < 0 or x >= level.dimensions[1] or \
            y < 0 or y >= level.dimensions[0]:

            break

        yield y, x


def flatten(xs):
    for x in xs:
        yield from x


def find_antinodes(level, a, b):
    points = list(trace_line(level, a.position, b.position))

    for point in points:
        if l1_dist(point, a.position) == 2 * l1_dist(point, b.position) or \
            l1_dist(point, b.position) == 2 * l1_dist(point, a.position):

            yield point


level = load_input()
pairs = pair_antennas(level.antennas)
antinodes = flatten(map(lambda pair: find_antinodes(level, *pair), pairs))
result = set(antinodes)

print(len(result))
