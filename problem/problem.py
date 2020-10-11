from problem.file_loader import LoadProblemFromFile
from problem.environment import Environment


class Problem:
    def __init__(self, grid, warehouses, drones, products, orders):
        self.grid = grid
        self.warehouses = warehouses
        self.drones = drones
        self.products = products
        self.orders = orders

        self.environment = self._get_environment()

    @classmethod
    def from_file(cls, file_location):
        return LoadProblemFromFile(cls, file_location).get_problem()

    def _get_environment(self):
        return Environment(grid=self.grid, warehouses=self.warehouses)
