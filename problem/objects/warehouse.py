from dataclasses import dataclass
from collections import defaultdict

from .grid import Location


class Inventory:
    def __init__(self):
        self._data = defaultdict(lambda: 0)

    def add_product(self, product, n_items=1):
        self._data[product] += n_items

    def remove_product(self, product, n_items=1):
        self._data[product] -= n_items

    def get_available_products(self):
        return (product for product, items in self._data.items() if items > 0)

    def get_available_items(self, product):
        return self._data[product]


@dataclass(frozen=True)
class WareHouse:
    warehouse_id: int
    location: Location
    inventory: Inventory

    def get_available_products(self):
        return self.inventory.get_available_products()

    def get_available_items(self, product):
        return self.inventory.get_available_items(product)
