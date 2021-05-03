width = 5
height = 5
matrix = [
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
]


def contains(cx, cy, sx, sy, ex, ey):
    within_x = sx <= cx <= ex
    within_y = sy <= cy <= ey
    return within_x and within_y


def set_barron(sx, sy, ex, ey):
    for i in range(sy, ey + 1):
        for j in range(sx, ex + 1):
            matrix[i][j] = 0


set_barron(1, 0, 4, 2)

for r in matrix:
    print(r)

coord = [2, 2]
print(contains(coord[0], coord[1], 1, 0, 4, 2))


def get_rows(sx, sy, ex, ey):
    row_ids = range(sx, ex + 1)
    last = [0, 0]
    for r in range(sy, height):
        # Make sure each coord in the zone is fertile and free
        if all(contains(r, i, 1, 0, 4, 2) for i in row_ids):
            for x in row_ids:
                last = (x, r)
        else:
            break
    return last