from dataclasses import dataclass


Position = tuple[int, int]
Direction = tuple[int, int]


@dataclass
class Level:
    rows: int
    columns: int
    obstacles: set[Position]


def add_obstacle(level, position):
    return Level(level.rows, level.columns, level.obstacles | {position})


class CycleDetected(Exception):
    pass


def read_lines(path):
    with open(path, encoding="utf-8") as stream:
        for line in stream:
            content = line.strip()

            if not content:
                continue

            yield content


def load_input():
    lines = list(read_lines("input/06.txt"))

    rows = len(lines)
    columns = len(lines[0])
    obstacles = set()
    initial_position = None
    initial_direction = None

    for row, line in enumerate(lines):
        for column, character in enumerate(line):
            if character == "#":
                obstacles.add((row, column))
            elif character == "^":
                initial_position = (row, column)
                initial_direction = (-1, 0)
            elif character == ">":
                initial_position = (row, column)
                initial_direction = (0, 1)
            elif character == "v":
                initial_position = (row, column)
                initial_direction = (1, 0)
            elif character == "<":
                initial_position = (row, column)
                initial_direction = (0, -1)
    
    level = Level(rows, columns, obstacles)
    initial_state = initial_position, initial_direction

    return level, initial_state


rotations = {
    (0, 1): (1, 0),
    (1, 0): (0, -1),
    (0, -1): (-1, 0),
    (-1, 0): (0, 1)
}


def step(level, state):
    start_position, start_direction = state
    next_position_row = start_position[0] + start_direction[0]
    next_position_column = start_position[1] + start_direction[1]

    if next_position_row < 0 or next_position_row >= level.rows:
        return None

    if next_position_column < 0 or next_position_column >= level.columns:
        return None

    next_position = (next_position_row, next_position_column)

    if next_position in level.obstacles:
        return start_position, rotations[start_direction]

    return next_position, start_direction


def simulate(level, initial_state):
    state = initial_state
    states = set([state])

    while True:
        state = step(level, state)

        if state is None:
            break

        if state in states:
            raise CycleDetected

        states.add(state)

    return states


level, initial_state = load_input()
initial_position = initial_state[0]
states = simulate(level, initial_state)
positions = set(state[0] for state in states)
loop_positions = set()

for position in positions:
    if position == initial_position:
        continue

    updated_level = add_obstacle(level, position)

    try:
        simulate(updated_level, initial_state)
    except CycleDetected:
        loop_positions.add(position)

print(len(positions))
print(len(loop_positions))
