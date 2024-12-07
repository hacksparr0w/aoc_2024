def load_input():
    lines = []

    with open("input/04.txt") as stream:
        for line in stream:
            lines.append(line.strip())

    return lines


def find_matrix_element(matrix, element):
    for row in range(len(matrix)):
        for column in range(len(matrix[row])):
            if matrix[row][column] == element:
                yield (row, column)


def get_matrix_element(matrix, position):
    row, column = position

    return matrix[row][column]


def check_x_mas_pattern(matrix, position):
    rows = len(matrix)
    columns = len(matrix[0])

    row, column = position

    if row - 1 < 0 or row + 1 >= rows:
        return False

    if column - 1 < 0 or column + 1 >= columns:
        return False

    tlbr = (
        get_matrix_element(matrix, (row - 1, column - 1)),
        get_matrix_element(matrix, (row + 1, column + 1))
    )

    if tlbr != ("M", "S") and tlbr != ("S", "M"):
        return False

    trbl = (
        get_matrix_element(matrix, (row - 1, column + 1)),
        get_matrix_element(matrix, (row + 1, column - 1))
    )

    if trbl != ("M", "S") and trbl != ("S", "M"):
        return False

    return True


matrix = load_input()
centers = find_matrix_element(matrix, "A")
checked = map(
    lambda position: check_x_mas_pattern(matrix, position),
    centers
)

result = sum(map(int, checked))

print(result)
