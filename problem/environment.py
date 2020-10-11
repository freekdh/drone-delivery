from itertools import product
import math

from problem.objects.grid import Location


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

    def get_nearest_warehouse(self, location):
        distances_to_warehouses = {
            warehouse: self.get_distance(
                location_1=location, location_2=warehouse.location
            )
            for warehouse in self.warehouses
        }
        return min(distances_to_warehouses.items(), key=lambda x: x[1])[0]

    def get_distance(self, location_1, location_2):
        return math.ceil(
            math.sqrt(
                abs(location_1.x - location_2.x) ** 2
                + abs(location_1.y - location_2.y) ** 2
            )
        )
