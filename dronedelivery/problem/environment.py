from itertools import product
import math

from dronedelivery.problem.objects.grid import Location


class Environment:
    def __init__(self, grid, warehouses):
        self.grid = grid
        self.warehouses = warehouses

    def __contains__(self, key):
        return key.location.x <= self.grid.n_x and key.location.y <= self.grid.n_y

    def get_all_locations(self):
        return iter(
            Location(x=x, y=y)
            for x, y in product(range(self.grid.n_x), range(self.grid.n_y))
        )

    def get_nearest_warehouse(self, place):
        distances_to_warehouses = {
            warehouse: self.get_distance(place_1=place, place_2=warehouse)
            for warehouse in self.warehouses
        }
        return min(distances_to_warehouses.items(), key=lambda x: x[1])[0]

    def get_distance(self, place_1, place_2):
        return math.ceil(
            math.sqrt(
                abs(place_1.location.x - place_2.location.x) ** 2
                + abs(place_1.location.y - place_2.location.y) ** 2
            )
        )
