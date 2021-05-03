import random
from pathlib import Path
from PIL import Image, ImageDraw


def display_image(islands, width=40, height=60, base=(20, 20, 20), test=False):
    """Renders and image with random colors for each zone in bounds.

    Args:
        islands (list[set]): list of grouped zones.
        width (int): Width of the image.
        height (int): Height of the image.
        base (tuple): The color to initially fill in the image with.
        test (bool): Used to disable show if running pytest.
    """
    img = Image.new("RGBA", size=(width, height), color=base)
    drawer = ImageDraw.Draw(img)
    img_out = Path(__file__).parent.parent.joinpath("grid.png")

    for i, island in enumerate(islands):
        for zone in island:
            # Get a random color
            rand_color = list(random.randint(0, 255) for i in range(3))
            rand_color.append(10 if i else 255)
            # Draw the zone.
            drawer.rectangle(zone.rectangle(), fill=tuple(rand_color))

    # Display the image
    vis = img.show() if not test else None
    # Save it out.
    img.save(img_out, format="png")
