import pytest
from os.path import isfile
from barren_lands.utils import format_input, format_raw_input, get_icon, get_css


def test_format_input():
    # Make sure the input coords are correctly getting formatted.
    input_coordinates = "0 292 399 307"
    # Run the formatter
    zone = format_input(input_coordinates)
    # Re-create the string from the zone object and compare.
    assert f"{zone.start.x} {zone.start.y} {zone.end.x} {zone.end.y}" == input_coordinates


def test_format_raw_input():
    # Make sure input from the GUI is formatted correctly.
    raw_input = "\"48 192 351 207\", “48 392 351 407”"

    parsed_input = format_raw_input(raw_input)

    assert parsed_input == [[48, 192, 351, 207], [48, 392, 351, 407]]


def test_get_icon():
    # Make sure we are getting a file back.
    icon_path = get_icon()

    assert isfile(icon_path)


def test_get_css():
    # Make sure we are getting a file back.
    css_data = get_css()

    assert "QPushButton" in css_data