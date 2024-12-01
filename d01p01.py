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
xs, ys = sorted(xs), sorted(ys)
r = sum(abs(x - y) for x, y in zip(xs, ys))

print(r)

assert r == 765748
