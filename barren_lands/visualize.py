from os.path import abspath, dirname
from itertools import product
from PIL import Image
import random


def display_image(bounds, width=40, height=60):

    img = Image.new("RGB", size=(width, height), color=(20, 20, 20))

    for bound in bounds:
        rand_color = tuple(random.randint(0, 255) for i in range(3))
        for x, y in product(range(width), range(height)):
            if bound.start.x <= x <= bound.end.x and bound.start.y <= y <= bound.end.y:
                img.putpixel(xy=(x, y), value=rand_color)

    img.show()
