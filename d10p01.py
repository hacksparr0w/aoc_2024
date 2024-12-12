from __future__ import annotations

from dataclasses import dataclass
from pprint import pprint


def read_lines(path):
    with open(path, "r", encoding="utf-8") as stream:
        for line in stream:
            content = line.strip()

            if content:
                yield content


Position = tuple[int, int]


@dataclass
class Level:
    rows: int
    columns: int
    zs: dict[Position, int]


def load_input():
    lines = list(read_lines("input/10.txt"))
    rows = len(lines)
    columns = len(lines[0])

    zs = {}

    for row in range(rows):
        for column in range(columns):
            zs[(row, column)] = int(lines[row][column])

    return Level(rows, columns, zs)


@dataclass
class Node:
    position: Position
    z: int
    children: list[Node]

    def __hash__(self):
        return hash(self.position)


def build_graph_roots(level):
    roots = []

    for row in range(level.rows):
        for column in range(level.columns):
            position = (row, column)
            z = level.zs[position]

            if z == 0:
                roots.append(Node(position, z, []))

    return roots


def add_graph_nodes(level, roots):
    if not roots:
        return []

    nodes = []

    for root in roots:
        row, column = root.position
        z1 = root.z

        positions = [
            (row - 1, column),
            (row + 1, column),
            (row, column - 1),
            (row, column + 1)
        ]

        for position in positions:
            z2 = level.zs.get(position)

            if z2 is None or z2 != z1 + 1:
                continue

            node = Node(position, z2, [])
            nodes.append(node)
            root.children.append(node)

    return nodes


def build_graph(level):
    roots = build_graph_roots(level)
    nodes = roots

    while nodes:
        nodes = add_graph_nodes(level, nodes)

    return roots


def last_nodes(root):
    if not root.children:
        return [root]

    result = []

    for child in root.children:
        result.extend(last_nodes(child))

    return result


level = load_input()
graph = build_graph(level)

total = 0

for root in graph:
    nodes = last_nodes(root)
    targets = set(filter(lambda n: n.z == 9, nodes))
    total += len(targets)

print(total)
