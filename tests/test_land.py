import pytest
import os
from pathlib import Path
from barren_lands.land import Field, Zone, Coord


class TestField:
    new_field = Field(6, 6)
    field_vis = [
        [1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 1, 1],
        [1, 1, 1, 0, 1, 1],
        [1, 0, 1, 0, 1, 1],
    ]

    def test_add_zone(self):
        new_zone = Zone(Coord(0, 0), Coord(0, 5))
        self.new_field.add_zone(new_zone, barren=False)
        # Make sure the new zone is added correctly.
        assert new_zone in self.new_field.fertile_zones

    def test_add_zone_barren(self):
        first_barren_zone = Zone(Coord(0, 3), Coord(3, 3))
        self.new_field.add_zone(first_barren_zone, barren=True)
        second_barren_zone = Zone(Coord(3, 3), Coord(3, 5))
        self.new_field.add_zone(second_barren_zone, barren=True)
        third_barren_zone = Zone(Coord(1, 5), Coord(1, 5))
        self.new_field.add_zone(third_barren_zone, barren=True)
        # Make sure the new barren zone is added correctly.
        assert first_barren_zone in self.new_field.barren_zones
        assert second_barren_zone in self.new_field.barren_zones
        assert third_barren_zone in self.new_field.barren_zones

    def test_check_coord(self):
        coord_to_check = Coord(1, 4)
        assert self.new_field.check_coord(coord_to_check)

    def test_check_coord_barren(self):
        coord_to_check = Coord(1, 5)
        assert not self.new_field.check_coord(coord_to_check)

    def test_check_coord_fertile(self):
        coord_to_check = Coord(0, 0)
        assert not self.new_field.check_coord(coord_to_check)

    def test_check_coord_outside_bounds(self):
        coord_to_check = Coord(0, 6)
        assert not self.new_field.check_coord(coord_to_check)

    def test_get_end(self):
        start_coord = Coord(2, 2)
        end_coord = self.new_field.get_end(start_coord)

        assert end_coord.x == 5
        assert end_coord.y == 2

    def test_get_rows(self):
        self.new_field.fertile_zones = set()
        start_coord = Coord(0, 0)
        end_coord = Coord(5, 0)
        last_coord = self.new_field.get_rows(start_coord, end_coord)

        assert last_coord == Coord(5, 2)

    def test_mark_zone(self):

        start_coord = Coord(0, 0)
        new_zone = self.new_field.mark_zone(start_coord)

        assert new_zone.start == Coord(0, 0)
        assert new_zone.end == Coord(5, 2)

    def test_check_zones(self):
        # Clear out the zones from prior tests
        self.new_field.fertile_zones = set()

        self.new_field.check_zones()
        print(self.new_field.fertile_zones)
        assert len(self.new_field.fertile_zones) == 5

    def test_display(self):

        image = Path(__file__).parent.parent.joinpath("grid.png")
        print(image)
        # Remove the image in preparation for it to be replaced.
        if image.exists():
            os.remove(image)

        self.new_field.display(test=True)

        assert image.exists()

    def test_gather_islands(self):
        self.new_field.gather_islands()
        assert len(self.new_field.islands) == 2


class TestCoord:

    def test_coord_init(self):
        new_coord = Coord(1, 2)

        assert new_coord.x == 1
        assert new_coord.y == 2

    def test_coord_copy(self):
        new_coord = Coord(1, 2)
        copy_coord = new_coord.copy()
        copy_coord.x = 2

        assert new_coord != copy_coord

    def test_coord_right(self):
        new_coord = Coord(1, 2)
        right_coord = new_coord.right()

        assert right_coord.x == (new_coord.x + 1)

    def test_coord_print(self):
        new_coord = Coord(1, 2)

        assert repr(new_coord) == "X:1 Y:2"


class TestZone:

    start = Coord(0, 0)
    end = Coord(4, 1)
    new_zone = Zone(start, end)

    def test_zone_width(self):
        assert self.new_zone.width() == 5

    def test_zone_height(self):
        assert self.new_zone.height() == 2

    def test_zone_get_size(self):
        assert self.new_zone.get_size() == 10

    def test_zone_rectangle(self):
        assert self.new_zone.rectangle() == [(0, 0), (4, 1)]

    def test_zone_contains(self):
        new_coord = Coord(0, 1)
        assert self.new_zone.contains(new_coord)

    def test_zone_not_contains(self):
        new_coord = Coord(0, 2)
        assert not self.new_zone.contains(new_coord)

    def test_zone_add(self):
        zone_a = Zone(Coord(0, 0), Coord(1, 4))  # size = 10
        zone_b = Zone(Coord(2, 3), Coord(3, 4))  # size = 4

        assert zone_a+zone_b == 14
        assert zone_a+4 == 14
