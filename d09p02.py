with open("input/09.txt") as stream:
    blocks = stream.readlines()[0].strip()

def expand(blocks):
    id = 0
    ids = []

    for i, block in enumerate(blocks):
        if i % 2 == 0:
            ids.extend([id] * int(block))
            id += 1
        else:
            ids.extend([None] * int(block))

    return ids


def swap(items, i1, i2):
    items[i1], items[i2] = items[i2], items[i1]


def multiswap(items, i1, i2, length):
    for offset in range(length):
        swap(items, i1 + offset, i2 + offset)


def find_continuous_space(ids, length, maximum_index):
    spaces = 0

    for index in range(maximum_index):
        id = ids[index]

        if id is None:
            spaces += 1

            if spaces == length:
                return index - length + 1
        else:
            spaces = 0

    return None


def find_continuous_block(ids, initial_index):
    current_id = None
    start_index = None
    stop_index = None

    for index in reversed(range(initial_index)):
        id = ids[index]

        if current_id is None:
            if id is not None:
                current_id = id
                stop_index = index + 1
        else:
            if id != current_id:
                start_index = index + 1
                break

    if start_index is None:
        return None

    return (start_index, stop_index)


def defragment_step(ids, initial_index):
    bounds = find_continuous_block(ids, initial_index)

    if bounds is None:
        return None

    length = bounds[1] - bounds[0]
    space_index = find_continuous_space(ids, length, bounds[0])

    if space_index is not None:
        multiswap(ids, bounds[0], space_index, length)

    return bounds[0]


def checksum(ids):
    result = 0

    for i, id in enumerate(ids):
        if id is None:
            continue

        result += i * id

    return result


ids = expand(blocks)
index = len(ids)

while index is not None:
    index = defragment_step(ids, index)

print(checksum(ids))
