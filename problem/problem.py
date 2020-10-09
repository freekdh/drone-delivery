from problem.file_loader import LoadProblemFromFile


class Problem:
    def __init__(self, grid, warehouses, drones, products, orders):
        self.grid = grid
        self.warehouses = warehouses
        self.drones = drones
        self.products = products
        self.orders = orders

    @classmethod
    def from_file(cls, file_location):
        return LoadProblemFromFile(cls, file_location).get_problem()
