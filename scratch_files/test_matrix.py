from itertools import product

nil = None
cnt = 0
ids = ["A", "B", "C"]
matrix = [
    [1, 0, 0, 0, 0],
    [1, 0, 0, 0, 0],
    [1, 1, 1, 1, 1],
    [1, 1, 0, 1, 1],
    [1, 1, 1, 1, 1],
]
result = [
    [0.0, nil, nil, nil, nil],
    [0.1, nil, nil, nil, nil],
    [0.2, 1.2, 2.2, 3.2, 4.2],
    [0.3, 1.3, nil, 3.3, 4.3],
    [0.4, 1.4, 2.4, 3.4, 4.4],
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


class Zone(object):

    def __init__(self, start, end):
        """

        Args:
            start (Coord):
            end (Coord):
        """
        self.start = start
        self.end = end

    def get_all(self):
        return [(i, j) for i, j in product(range(self.start.x, self.end.x+1),
                                           range(self.start.y, self.end.y+1))]

    def get_size(self):
        return self.width() * self.height()

    def width(self):
        # Add 1 since we are starting with 0
        return self.end.x - self.start.x + 1

    def height(self):
        # Add 1 since we are starting with 0
        return self.end.y - self.start.y + 1

    def contains(self, coord):
        """Checks to see if a coord is within this zone.

        Args:
            coord (Coord):

        Returns:
            True if in zone else False.
        """
        # https://stackoverflow.com/questions/18295825/determine-if-point-is-within-bounding-box
        if self.start.x <= coord.x <= self.end.x and self.start.y <= coord.y <= self.end.y:
            return True
        else:
            return False

    def __repr__(self):
        return f"start:{self.start.x}-{self.start.y} end:{self.end.x}-{self.end.y}"


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
                if (x, r) in used_zones:
                    # we dont need you.
                    break
                else:
                    used_zones.append((x, r))
                    last = Coord(x, r)
        else:
            break
    return last


def find_zone(x, y):
    start = Coord(x, y)
    end = get_end(start)
    end = get_rows(start, end)
    return Zone(start, end)


zone_list = []
for y, x in product(range(height), range(width)):
    cord = Coord(x, y)
    if (x, y) not in used_zones and check(cord):
        zone_list.append(find_zone(x, y))
        cnt += 1

# print(used_zones)
# find_zone(0, 0)
# find_zone(1, 2)

# print(get_row(Coord(0, 0)))
# print(get_row(Coord(0, 2)))

for zone in zone_list:
    print(zone.get_all())
    print(zone.get_size())
