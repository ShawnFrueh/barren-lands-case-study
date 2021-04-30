import pytest
from barren_lands.utils import format_input


def test_format_input():
    # Make sure the input coords are correctly getting formatted.
    input_coordinates = "0 292 399 307"
    # Run the formatter
    zone = format_input(input=input_coordinates)
    # Re-create the string from the zone object and compare.
    assert f"{zone.start.x} {zone.start.y} {zone.end.x} {zone.end.y}" == input_coordinates
