from itertools import product
from .visualize import display_image


class Field(object):

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.barren_zones = set()
        self.fertile_zones = set()

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
        for y, x in product(range(0, self.height), range(0, self.width)):
            current_coord = Coord(x, y)
            if self.check_coord(current_coord):
                self.mark_zone(current_coord)

    def mark_zone(self, zone_start):
        row_end = self.get_end(zone_start)
        zone_end = self.get_rows(zone_start, row_end)
        new_zone = Zone(zone_start, zone_end)
        self.add_zone(new_zone)

    def get_end(self, coord):
        end = coord.copy()
        for i in range(coord.x, self.width+1):
            # If end is still within the field
            if self.check_coord(end.right()):
                end.x += 1
            else:
                break
        return end

    def get_rows(self, start, end):
        row_ids = range(start.x, end.x + 1)
        last = end
        for r in range(start.y, self.height):
            # Make sure each coord in the zone is fertile and free
            row_debug = [(i, r) for i in row_ids]
            row_data = [self.check_coord(Coord(i, r)) for i in row_ids]
            if all(row_data):
                last = Coord(end.x, r)
            else:
                break
        return last

    def display(self):
        display_image(self.fertile_zones, self.width, self.height)


class Coord(object):
    """Representation of one unit within a Zone"""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def copy(self):
        return Coord(self.x, self.y)

    def right(self):
        return Coord(self.x+1, self.y)

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

    def __repr__(self):
        """Used for debugging with print ;)

        Returns:
            (str): Formatted results of this zone
        """
        return f"start:{self.start.x}-{self.start.y} end:{self.end.x}-{self.end.y}"

