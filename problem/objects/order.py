from dataclasses import dataclass
from .grid import Location


@dataclass(frozen=True)
class Order:
    order_id: int
    location: Location
    demand: list
