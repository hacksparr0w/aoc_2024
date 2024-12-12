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


def is_fragmented(ids):
    found_space = False

    for id in ids:
        if id is None:
            found_space = True
        elif found_space:
            return True

    return False


def swap(items, i1, i2):
    items[i1], items[i2] = items[i2], items[i1]


def defragment_step(ids):
    i1 = [i for i in range(len(ids)) if ids[i] is None][0]
    i2 = [i for i in reversed(range(len(ids))) if ids[i] is not None][0]

    swap(ids, i1, i2)


def checksum(ids):
    result = 0

    for i, id in enumerate(ids):
        if id is None:
            continue

        result += i * id

    return result


ids = expand(blocks)

while is_fragmented(ids):
    defragment_step(ids)

print(checksum(ids))
