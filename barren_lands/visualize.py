from os.path import dirname, join
from PIL import Image, ImageDraw
import random


def display_image(zones, width=40, height=60, base=(20, 20, 20), test=False):
    """Renders and image with random colors for each zone in bounds.

    Args:
        zones (set[Zone]): List of zones to draw.
        width (int): Width of the image.
        height (int): Height of the image.
        base (tuple): The color to initially fill in the image with.
        test (bool): Used to disable show if running pytest.
    """
    img = Image.new("RGB", size=(width, height), color=base)
    drawer = ImageDraw.Draw(img)
    img_out = join(dirname(dirname(__file__)), "grid.png")

    for zone in zones:
        # Get a random color
        rand_color = tuple(random.randint(0, 255) for i in range(3))
        # Draw the zone.
        drawer.rectangle(zone.rectangle(), fill=rand_color)

    # Display the image
    vis = img.show() if not test else None
    # Save it out.
    img.save(img_out, format="png")
