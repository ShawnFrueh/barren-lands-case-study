import itertools
from barren_lands.land import Zone, Coord, Field

matrix = [
    [1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1],
    [1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1],
]
matrix = [
    [1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 1, 1],
    [1, 1, 1, 0, 1, 1],
    [1, 0, 1, 0, 1, 1],
]

if __name__ == "__main__":
    # https://stackoverflow.com/questions/2254697/how-can-i-group-an-array-of-rectangles-into-islands-of-connected-regions
    barren_zones = set()

    #barren_zones.add(Zone(Coord(1, 1), Coord(4, 1)))
    #barren_zones.add(Zone(Coord(1, 1), Coord(1, 4)))
    #barren_zones.add(Zone(Coord(4, 1), Coord(4, 4)))
    #barren_zones.add(Zone(Coord(1, 4), Coord(4, 4)))
    barren_zones.add(Zone(Coord(0, 3), Coord(3, 3)))
    barren_zones.add(Zone(Coord(3, 3), Coord(3, 5)))
    barren_zones.add(Zone(Coord(1, 5), Coord(1, 5)))

    field = Field(width=6, height=6)

    for zone in barren_zones:
        field.add_zone(zone, barren=True)

    field.check_zones()

    n_list = set()


    # print(field.find_neighbours(field.fertile_zones.copy().pop()))
    # def find_neighbours(zone, field):
    #     for f_zone in field.fertile_zones:
    #         if f_zone not in n_list and f_zone.is_neighbor(zone):
    #             n_list.add(f_zone)
    #             find_neighbours(f_zone)

    from collections import defaultdict
    print(field.fertile_zones)
    def get_connected():
        neighbours = defaultdict(set)
        for zone in field.fertile_zones:
            for n_zone in field.fertile_zones:
                if zone != n_zone and zone.is_neighbor(n_zone):
                    neighbours[zone.id()].add(n_zone)
        print(neighbours)
        components = list()
        done = set()
        for zone in field.fertile_zones:
            if zone.id() in done:
                continue
            cur_comp = set()
            queue = set()
            queue.add(zone)
            while queue:
                r = queue.pop()
                for n in neighbours.get(r.id(), [r]):
                    if n.id() not in done:
                        done.add(n.id())
                        queue.add(n)
                        cur_comp.add(n)
            components.append(cur_comp)
        print(components)


    my_dict = {"start:0-0 end:5-0": "all"}


    get_connected()

    # for i in field.fertile_zones:
    #     for j in field.fertile_zones:
    #         if i != j and j.is_neighbour(i):
    #             neighbours[i]

    # field.display()
    zone_a = Zone(Coord(5, 1), Coord(5, 4))
    zone_b = Zone(Coord(2, 2), Coord(3, 3))

    print(zone_a.is_neighbor(zone_b))
