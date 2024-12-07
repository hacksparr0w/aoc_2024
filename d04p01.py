def load_input():
    lines = []

    with open("input/04.txt") as stream:
        for line in stream:
            lines.append(line.strip())

    return lines


def find_indices(text, character, start_index):
    indices = []

    for index in range(start_index, len(text)):
        if text[index] == character:
            indices.append(index)

    return indices


def overlap_find(text, keyword, start_index = 0):
    if len(keyword) == 0:
        return []

    if len(keyword) == 1:
        return [[index] for index in find_indices(text, keyword, start_index)]

    head, tail = keyword[0], keyword[1:]
    result = []

    for head_index in find_indices(text, head, start_index):
        for tail_indices in overlap_find(text, tail, head_index + 1):
            result.append([head_index] + tail_indices)

    return result


assert len(overlap_find("abracadabra", "abra")) == 9


def simple_find(text, keyword):
    return [
        index
        for index in range(len(text))
        if text[index:].startswith(keyword)
    ]


def map_matrix_indices(indices, matrix):
    return [matrix[row][column] for row, column in indices]


def map_string_matrix_indices(indices, matrix):
    return "".join(map_matrix_indices(indices, matrix))


def get_matrix_row_indices(rows, columns):
    return [
        [(row, column) for column in range(columns)]
        for row in range(rows)
    ]


def get_matrix_column_indices(rows, columns):
    return [
        [(row, column) for row in range(rows)]
        for column in range(columns)
    ]


def get_matrix_diagonal_indices(rows, columns):
    return [
        [(row, row + column) for row in range(rows) if row + column < columns]
        for column in range(columns)
    ] + [
        [(row + column, row) for row in range(rows) if row + column < rows]
        for column in range(1, rows)
    ] + [
        [(row, column - row) for row in range(rows) if column - row >= 0]
        for column in range(columns)
    ] + [
        [
            (row + column, columns - 1 - row)
            for row in range(rows) if row + column < columns
        ]
        for column in range(1, columns)
    ]


matrix = load_input()
rows = len(matrix)
columns = len(matrix[0])
stripes = [
    *get_matrix_row_indices(rows, columns),
    *[list(reversed(row)) for row in get_matrix_row_indices(rows, columns)],
    *get_matrix_column_indices(rows, columns),
    *[
        list(reversed(column))
        for column in get_matrix_column_indices(rows, columns)
    ],
    *get_matrix_diagonal_indices(rows, columns),
    *[
        list(reversed(diagonal))
        for diagonal in get_matrix_diagonal_indices(rows, columns)
    ]
]

mapped = [map_string_matrix_indices(stripe, matrix) for stripe in stripes]
searched = [len(simple_find(text, "XMAS")) for text in mapped]
result = sum(searched)

print(result)
