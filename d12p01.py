import time

from dataclasses import dataclass


def read_lines(path):
    with open(path, "r", encoding="utf-8") as stream:
        for line in stream:
            content = line.strip()

            if content:
                yield content


Row = int
Column = int
Position = tuple[Row, Column]


@dataclass
class Level:
    rows: int
    columns: int
    data: dict[Position, str]


directions = set([(1, 0), (0, 1), (-1, 0), (0, -1)])


def load_input():
    lines = list(read_lines("input/12.txt"))
    rows = len(lines)
    columns = len(lines[0])

    data = {}

    for row, line in enumerate(lines):
        for column, character in enumerate(line):
            data[(row, column)] = character

    return Level(rows, columns, data)


def fill(level, initial_position):
    value = level.data[initial_position]

    boundary_positions = set()
    area = set()
    neighbours = set()

    candidates = set([initial_position])

    while candidates:
        candidate = candidates.pop()
        other = level.data.get(candidate)
        row, column = candidate

        if value != other:
            boundary_positions.add(candidate)

            if other is not None:
                neighbours.add(candidate)
            
            continue

        area.add(candidate)

        for direction in directions:
            position = (row + direction[0], column + direction[1])

            if position not in area:
                candidates.add(position)

    boundaries = dict()

    for candidate in boundary_positions:
        row, column = candidate
        edges = 0

        for direction in directions:
            position = (row + direction[0], column + direction[1])

            if position in area:
                edges += 1

        boundaries[candidate] = edges

    return boundaries, area, neighbours


def calculate_regions(level, initial_position):
    regions = []
    candidates = set([initial_position])

    while candidates:
        candidate = candidates.pop()
        is_visited = False

        for _, area in regions:
            if candidate in area:
                is_visited = True
                break

        if is_visited:
            continue

        boundaries, area, neighbours = fill(level, candidate)

        regions.append((boundaries, area))
        candidates.update(neighbours)

    return regions


level = load_input()
initial_position = (0, 0)
regions = calculate_regions(level, initial_position)

total = 0

for boundaries, area in regions:
    total += len(area) * sum(boundaries.values())

print(total)
