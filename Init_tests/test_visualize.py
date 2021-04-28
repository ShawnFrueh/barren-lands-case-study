from os.path import abspath
from PIL import Image
import random

image_name = abspath("grid.png")
img = Image.new("RGB", size=(400, 600), color=(20, 20, 20))


def print_grid(bounds, width=40, height=60):
    rand_color = tuple(random.randint(0, 255) for i in range(3))
    print(rand_color)
    for x in range(width):
        for y in range(height):
            if bounds[0] <= x <= bounds[2] and bounds[1] <= y <= bounds[3]:
                img.putpixel(xy=(x, y), value=rand_color)


data = [[int(j) for j in i.split(" ")] for i in ("0 292 399 307",)]
data = [[int(j) for j in i.split(" ")] for i in ("48 192 351 207", "48 392 351 407", "120 52 135 547", "260 52 275 547")]
print(data)

for d in data:
    print_grid(d, width=400, height=600)

img.show()
