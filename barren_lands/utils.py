from .land import Coord, Zone


def format_input(input):
    """Formats the input coordinates into z zone.

    Args:
        input (str): input to parse.

    Returns:

    """
    values = [int(i) for i in input.strip().split(" ")]
    start = Coord(values[0], values[1])
    end = Coord(values[2], values[3])
    return Zone(start, end)