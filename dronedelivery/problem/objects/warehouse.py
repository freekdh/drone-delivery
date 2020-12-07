from dataclasses import dataclass
from collections import defaultdict

from .grid import Location
from .product import Product


class Inventory:
    def __init__(self):
        self._data = defaultdict(int)

    def add_product(self, product, n_items=1):
        self._data[product] += n_items

    def remove_product(self, product, n_items=1):
        assert self._data[product] >= n_items
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

    def __repr__(self):
        return f"Warehouse {self.warehouse_id}"

    def __contains__(self, key):
        assert isinstance(key, Product)
        return True if self.get_available_items(key) > 0 else False

    def get_available_products(self):
        return self.inventory.get_available_products()

    def get_available_items(self, product):
        return self.inventory.get_available_items(product)

    def get_inventory(self):
        return dict(self.inventory._data)