from dataclasses import dataclass
from .grid import Location
from collections import Counter


@dataclass(frozen=True)
class Order:
    order_id: int
    location: Location
    demand: list

    def get_demand(self):
        return dict(Counter(self.demand))

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return f"Order {self.order_id}"