from itertools import product

matrix = [
    [1, 0, 0, 0, 0],
    [1, 0, 1, 0, 0],
    [1, 1, 1, 1, 1],
    [0, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
]

width = len(matrix[0])
height = len(matrix)

used_zones = list()


class Coord(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def check(self):
        # Sample the matrix at this coordinate.
        return matrix[self.y][self.x]

    def accounted(self):
        used_zones.append((self.x, self.y))

    def right(self):
        """

        Returns:
            Coord
        """
        if self.x < width - 1:
            return Coord(self.x + 1, self.y)

    def __eq__(self, other):
        pass

    def __repr__(self):
        return f"X:{self.x} Y:{self.y}"


class zone(object):

    def __init__(self, start, end):
        self.start = start
        self.end = end


def check(coord):
    if coord:
        return matrix[coord.y][coord.x]
    return False


def get_end(coord):
    """

    Args:
        coord (Coord):

    Returns:

    """
    end = Coord(coord.x, coord.y)
    for i in range(coord.x, width):
        if check(end.right()):
            end = end.right()
            # used_zones.append((cord.x, i))
        else:
            break
    return end


def get_rows(start, end):
    row_ids = list(range(start.x, end.x + 1))
    last = end
    for r in range(start.y, height):
        # If all items in row are 1
        if all(matrix[r][x] for x in row_ids):
            for x in row_ids:
                used_zones.append((x, r))
                last = Coord(x, r)
        else:
            break
    return last


def find_zone(x, y):
    start = Coord(x, y)
    end = get_end(start)
    end = get_rows(start, end)

    print(start, end)


for y, x in product(range(height), range(width)):
    cord = Coord(x, y)
    if (x, y) not in used_zones and check(cord):
        find_zone(x, y)

print(used_zones)
# find_zone(0, 0)
# find_zone(1, 2)

# print(get_row(Coord(0, 0)))
# print(get_row(Coord(0, 2)))
