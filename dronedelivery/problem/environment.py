from itertools import product
import math
from dronedelivery.solvers.drone_schedule_configuration import Deliver, Load, Unload
from dronedelivery.problem.objects.grid import Location


class EmptyInventory(Exception):
    pass


class WarehouseInventory:
    def __init__(self, products_to_n_items: dict = {}):
        self._products_to_n_items = products_to_n_items

    def add(self, product):
        if product in self._products_to_n_items:
            self._products_to_n_items[product] += 1
        else:
            self._products_to_n_items[product] = 1

    def remove(self, product):
        if (
            product in self._products_to_n_items
            or self._products_to_n_items[product] == 0
        ):
            raise EmptyInventory(f"product {product} is not available in inventory")
        else:
            self._products_to_n_items[product] -= 1

        if self._products_to_n_items[product] == 0:
            del self._products_to_n_items[product]


class OrderInventory:
    def __init__(self, order):
        self.order = order
        self._products_to_n_items = dict()

        self.last_order_delivered_at = None

    def add(self, product, time):
        if product in self._products_to_n_items:
            self._products_to_n_items[product] += 1
        else:
            self._products_to_n_items[product] = 1

        if self.all_products_are_delivered():
            self.last_order_delivered_at = time

    def all_products_are_delivered(self):
        return self.order.get_demand() == self._products_to_n_items


class Environment:
    def __init__(self, grid, warehouses, orders):
        self.grid = grid
        self.warehouses = warehouses
        self.orders = orders

        self._current_time = 0
        self._warehouse_inventory = {
            warehouse: WarehouseInventory(warehouse.get_full_inventory())
            for warehouse in self.warehouses
        }
        self._order_demand = {order: OrderInventory(order) for order in self.orders}

    def __contains__(self, key):
        return key.location.x <= self.grid.n_x and key.location.y <= self.grid.n_y

    def get_all_locations(self):
        return iter(
            Location(x=x, y=y)
            for x, y in product(range(self.grid.n_x), range(self.grid.n_y))
        )

    def get_nearest_warehouse(self, place):
        distances_to_warehouses = {
            warehouse: self.get_distance(
                location_1=place.location, location_2=warehouse.location
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

    def remove_product_from_warehouse(self, warehouse, product):
        self._warehouse_inventory[warehouse].remove(product)

    def add_product_to_warehouse(self, warehouse, product):
        self._warehouse_inventory[warehouse].add(product)

    def add_product_to_order(self, order, product):
        self._order_demand[order].add(product, self._current_time)

    def apply_actions(self, drone_actions, time):
        """
        When applying actions, first unload then load
        """
        self._current_time = time
        for drone_action in drone_actions:
            if isinstance(drone_action, Unload):
                self.add_product_to_warehouse(
                    warehouse=drone_action.warehouse, product=drone_action.product
                )
            elif isinstance(drone_action, Deliver):
                self.add_product_to_order(
                    order=drone_action.order, product=drone_action.product
                )

        for drone_action in drone_actions:
            if isinstance(drone_action, Load):
                self.remove_product_from_warehouse(
                    warehouse=drone_action.warehouse, product=drone_action.product
                )

    def get_time_last_product_delivered(self, order):
        return self._order_demand[order].last_order_delivered_at

    def is_delivered(self, order):
        return self._order_demand[order].all_products_are_delivered()

    def get_delivered_orders(self):
        return (order for order in self.orders if self.is_delivered(order))