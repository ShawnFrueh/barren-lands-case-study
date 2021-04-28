
from barren_lands import land, utils


inputs = {"0 292 399 307"}

Field = land.Field(width=399, height=599)

for barren_coord in inputs:
    barren_zone = utils.format_input(barren_coord)
    print(barren_zone)
    Field.add_zone(barren_zone, barren=True)

Field.check_zones()

for zone in Field.fertile_zones:
    print("Fertile:", zone, zone.get_size())

for zone in Field.barren_zones:
    print("Barren:", zone.get_size())
