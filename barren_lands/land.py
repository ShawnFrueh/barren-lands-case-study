from itertools import product, combinations
from collections import defaultdict

from .visualize import display_image


class Field(object):

    def __init__(self, width, height):
        """Field initialization.

        Args:
            width (int): The max width of the Field.
            height (int): The max height of the Field.
        """
        self.width = width
        self.height = height
        self.zone = Zone(Coord(0, 0), Coord(width-1, height-1))
        self.barren_zones = set()
        self.fertile_zones = set()
        self.islands = list()

    def check_coord(self, coord):
        """Checks to see if the Coordinate is within a barren or fertile zone.

        Args:
            coord (Coord): The coordinate to check

        Returns:
            True if fertile else False
        """
        for zone in self.barren_zones:  # type: Zone
            if zone.contains(coord):
                # If any barren land touches this zone, return False.
                return False
        for zone in self.fertile_zones:
            if zone.contains(coord):  # type: Zone
                # We already used this coord, return False.
                return False
        if not self.zone.contains(coord):
            # We are outside the field. Turn that tractor around.
            return False
        # Not used, all good.
        return True

    def add_zone(self, zone, barren=False):
        """Adds a zone to the appropriate zone list.

        Args:
            zone (Zone): The zone to add.
            barren (bool): barren if True else fertile.
        """
        if barren:
            self.barren_zones.add(zone)
        else:
            self.fertile_zones.add(zone)

    def check_zones(self):
        """Runs the final calculation to mark the zones."""
        for x, y in product(range(0, self.width), range(0, self.height)):
            current_coord = Coord(x, y)
            if self.check_coord(current_coord):
                self.mark_zone(current_coord)
        # Partition zones into their respective islands.
        self.gather_islands()

    def mark_zone(self, zone_start):
        """Marks a zone from an input coordinate.

        Args:
            zone_start (Coord): The coordinate of the field to start the zone.

        Returns:
            new_zone (Zone): The new zone generated from a start coord.
        """
        row_end = self.get_end(zone_start)
        zone_end = self.get_rows(zone_start, row_end)
        new_zone = Zone(zone_start, zone_end)
        self.add_zone(new_zone)
        return new_zone

    def gather_islands(self):
        """Handles taking the final zones and grouping them into islands of connected zones.

        Notes:
            https://stackoverflow.com/questions/2254697/how-can-i-group-an-array-of-rectangles-into-islands-of-connected-regions
        """
        neighbours = defaultdict(set)
        self.islands = list()
        visited = set()
        # Get all zone pairs and check to see if they are neighbors.
        for zone in self.fertile_zones:
            for n_zone in self.fertile_zones:
                if zone != n_zone and zone.is_neighbor(n_zone):
                    neighbours[zone.id()].add(n_zone)
        # Re-iterate over the fertile zones
        for zone in self.fertile_zones:
            if zone.id() not in visited:
                island_zones = set()
                zone_que = set()
                zone_que.add(zone)
                while zone_que:
                    z = zone_que.pop()
                    for n in neighbours.get(z.id(), [z]):
                        if n.id() not in visited:
                            # This is a neighbour, add it to our island set.
                            island_zones.add(n)
                            # Mark that we have visited this zone
                            visited.add(n.id())
                            # Add the neighbour to the Que to then check for it's neighbours.
                            zone_que.add(n)
                if island_zones:
                    self.islands.append(island_zones)
        # Sort the island list from largest to smallest
        self.islands.sort(key=lambda i: len(i), reverse=True)
        for island in self.islands:
            print(island)

    def get_end(self, coord):
        """Gets the last unmarked coordinate in the same row.

        Args:
            coord (Coord): The coordinate to start from.

        Returns:
            end (Coord): The last available coordinate.
        """
        end = coord.copy()
        for i in range(coord.x, self.width + 1):
            # If end is still within the field
            if self.check_coord(end.right()):
                end.x += 1
            else:
                break
        return end

    def get_rows(self, start, end):
        """Given a start and end of a single row, finds all available sub rows.

        Args:
            start (Coord): The start coord of the first row.
            end (Coord): The last cord of the row.

        Returns:
            last (Coord): The Opposite bounding coordinate from the start.
        """
        row_ids = range(start.x, end.x + 1)
        last = end.copy()
        for y in range(start.y, self.height):
            # Make sure each coord in the zone is fertile and free
            row_debug = [(i, y) for i in row_ids]
            row_data = [self.check_coord(Coord(i, y)) for i in row_ids]
            if all(row_data):
                last = Coord(end.x, y)
            else:
                break
        return last

    def display(self, test=False):
        """Triggers a render of the resulting Field.

        Args:
            test (bool): If running a pytest, dont display the image.
        """
        display_image(self.islands, self.width, self.height, test=test)


class Coord(object):
    """Representation of one unit within a Zone"""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def copy(self):
        # Returns a new coord with this coords coordinates.
        return Coord(self.x, self.y)

    def right(self):
        """Gets the coord immediately to the right of this coord."""
        return Coord(self.x + 1, self.y)

    def __eq__(self, other):
        """Coordinate comparison
        Args:
            other (Coord): Other coordinate to check.
        """
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        """Hashing capabilities to allow for use in sets.

        Returns:
            (hash): Hashed value using (x, y)
        """
        return hash((self.x, self.y))

    def __repr__(self):
        """Used for debugging with print ;)

        Returns:
            (str): Formatted results of this Coord.
        """
        return f"X:{self.x} Y:{self.y}"


class Zone(object):
    """Class to handle storing zone information from within the Field."""

    def __init__(self, start, end):
        """Representation of a zone within a Field.

        Notes:
            Contains just the bounding box coordinates that make up the zone.

        Args:
            start (Coord): The first bounding box coordinate.
            end (Coord): The last bounding box coordinate.
        """
        self.start = start
        self.end = end

    def width(self):
        """Calculates the width of the zone using its coordinates.

        Returns:
            (int): The calculated with of this zone
        """
        # Add 1 since we are starting with 0
        return self.end.x - self.start.x + 1

    def height(self):
        """Calculates the height of the zone using its coordinates.

        Returns:
            (int): The calculated height of this zone
        """
        # Add 1 since we are starting with 0
        return self.end.y - self.start.y + 1

    def get_size(self):
        """Calculates the 2D volume of this zone.

        Returns:
            (int): The volume of this zone in units.
        """
        return self.width() * self.height()

    def rectangle(self):
        """Returns a formatted version of this Zone for use with PIL.

        Returns:
            (list[tuple]): Formatted tuple for PIL.
        """
        return [(self.start.x, self.start.y), (self.end.x, self.end.y)]

    def contains(self, coord):
        """Checks to see if the incoming coord is within this zone.

        Notes:
            https://stackoverflow.com/questions/18295825/determine-if-point-is-within-bounding-box

        Args:
            coord (Coord):

        Returns:
            True if in zone else False.
        """
        within_x = self.start.x <= coord.x <= self.end.x
        within_y = self.start.y <= coord.y <= self.end.y
        return within_x and within_y

    def is_neighbor(self, zone):
        """Checks to see if another zone is considered a neighbour.

        Args:
            zone (Zone): Zone to check if is neighbour.

        Returns:
            (bool): True if neighbour else False
        """
        for edge in zone.boundary():
            # Extend by 1 to have border zones intersect.
            within_x = (self.start.x - 1) <= edge.x <= (self.end.x + 1)
            within_y = (self.start.y - 1) <= edge.y <= (self.end.y + 1)
            if within_x and within_y:
                return True
        return False

    def boundary(self):
        """Find the outer perimeter of the zone and return all coordinates.

        Returns:
            boundary (set): The boundary coordinates to a zone.
        """
        boundary = set()
        top = [boundary.add(Coord(x, self.start.y)) for x in range(self.start.x, self.end.x + 1)]
        bottom = [boundary.add(Coord(x, self.end.y)) for x in range(self.start.x, self.end.x + 1)]
        left = [boundary.add(Coord(self.end.x, y)) for y in range(self.start.y, self.end.y + 1)]
        right = [boundary.add(Coord(self.start.x, y)) for y in range(self.start.y, self.end.y + 1)]

        return boundary

    def id(self):
        return f"{self.start.x}-{self.start.y}-{self.end.x}-{self.end.y}"

    def __repr__(self):
        """Used for debugging with print ;)

        Returns:
            (str): Formatted results of this zone
        """
        return f"start:{self.start.x}-{self.start.y} end:{self.end.x}-{self.end.y}"
