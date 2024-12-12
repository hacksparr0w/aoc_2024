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
convex_corners = [
    (
        ((1, 0), False),
        ((0, -1), False)   
    ),
    (
        ((1, 0), False),
        ((0, 1), False)
    ),
    (
        ((-1, 0), False),
        ((0, -1), False)
    ),
    (
        ((-1, 0), False),
        ((0, 1), False)
    )
]

concave_corners = [
    (
        ((1, 0), True),
        ((0, -1), True),
        ((1, -1), False)
    ),
    (
        ((1, 0), True),
        ((0, 1), True),
        ((1, 1), False)
    ),
    (
        ((-1, 0), True),
        ((0, 1), True),
        ((-1, 1), False)
    ),
    (
        ((-1, 0), True),
        ((0, -1), True),
        ((-1, -1), False)
    )
]

corners = convex_corners + concave_corners


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

    region = set()
    neighbours = set()

    candidates = set([initial_position])

    while candidates:
        candidate = candidates.pop()
        other = level.data.get(candidate)
        row, column = candidate

        if value != other:
            if other is not None:
                neighbours.add(candidate)
            
            continue

        region.add(candidate)

        for direction in directions:
            position = (row + direction[0], column + direction[1])

            if position not in region:
                candidates.add(position)

    return region, neighbours


def calculate_regions(level, initial_position):
    regions = []
    candidates = set([initial_position])

    while candidates:
        candidate = candidates.pop()
        is_visited = False

        for region in regions:
            if candidate in region:
                is_visited = True
                break

        if is_visited:
            continue

        region, neighbours = fill(level, candidate)

        regions.append(region)
        candidates.update(neighbours)

    return regions


def corner_score(region, candidate):
    row, column = candidate
    score = 0

    for criterium in corners:
        is_corner = all([
            ((row + d[0], column + d[1]) in region) == v
            for d, v in criterium
        ])

        if is_corner:
            score += 1

    return score


level = load_input()
initial_position = (0, 0)
regions = calculate_regions(level, initial_position)

total = 0

for region in regions:
    c = sum(map(lambda p: corner_score(region, p), region))
    total += c * len(region)

print(total)
