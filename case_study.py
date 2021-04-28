
from barren_lands import land, utils

width = 400
height = 600
inputs = {"0 292 399 307"}
#inputs = {"48 192 351 207", "48 392 351 407", "120 52 135 547", "260 52 275 547"}

# width = 5
# height = 5
# inputs = {"1 0 4 1"}

Field = land.Field(width, height)

for barren_coord in inputs:
    barren_zone = utils.format_input(barren_coord)
    Field.add_zone(barren_zone, barren=True)

Field.check_zones()
Field.display()

for zone in Field.fertile_zones:
    print("Fertile:", zone, zone.get_size())

for zone in Field.barren_zones:
    print("Barren:", zone.get_size())
