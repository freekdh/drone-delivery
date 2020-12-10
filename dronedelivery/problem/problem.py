from collections import defaultdict

from dronedelivery.problem.file_loader import LoadProblemFromFile
from dronedelivery.problem.environment import Environment
from dronedelivery.problem.objects.customer import Customer


class Problem:
    def __init__(self, grid, warehouses, drones, products, orders, max_turns):
        self.grid = grid
        self.warehouses = warehouses
        self.drones = drones
        self.products = products
        self.orders = orders
        self.max_turns = max_turns

        self.customers = self.get_customers()

    @classmethod
    def from_file(cls, file_location):
        return LoadProblemFromFile(cls, file_location).get_problem()

    def get_environment(self):
        return Environment(
            grid=self.grid, warehouses=self.warehouses, orders=self.orders
        )

    def get_customers(self):
        orders_by_location = defaultdict(list)
        for order in self.orders:
            orders_by_location[order.location].append(order)

        return [Customer(orders) for location, orders in orders_by_location.items()]
