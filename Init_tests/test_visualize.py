from os.path import abspath
from PIL import Image
import random

image_name = abspath("grid.png")
img = Image.new("RGB", size=(400, 600), color=(0, 200, 0))


def print_grid(bounds, width=40, height=60):
    rand_color = tuple(random.randint(0, 255) for i in range(3))
    print(rand_color)
    for x in range(width):
        for y in range(height):
            if bounds[2] <= x <= bounds[0]:
                color = rand_color
                img.putpixel(xy=(y, y), value=color)
            elif bounds[1] <= y <= bounds[3]:
                color = rand_color
                img.putpixel(xy=(x, y), value=color)
            else:
                color = (209, 123, 193)


data = [[int(j) for j in i.split(" ")] for i in ("0 292 399 307",)]
data = [[int(j) for j in i.split(" ")] for i in ("48 192 351 207", "48 392 351 407", "120 52 135 547", "260 52 275 547")]
print(data)

for d in data:
    print_grid(d, width=400, height=600)

img.show()
