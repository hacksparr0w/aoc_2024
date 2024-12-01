def freq(items):
    return {item: items.count(item) for item in set(items)}


def load_input():
    xs = []
    ys = []

    with open("01.txt", encoding="utf-8") as stream:
        for line in stream:
            x, y = line.strip().split("   ")

            xs.append(int(x))
            ys.append(int(y))

    return xs, ys


xs, ys = load_input()
f = freq(ys)
r = sum(x * f.get(x, 0) for x in xs)

print(r)

assert r == 27732508
