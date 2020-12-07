from dataclasses import dataclass


@dataclass(frozen=True)
class Product:
    product_id: int
    weight: int

    def __repr__(self):
        return f"Product {self.product_id}"