from collections import Counter
import itertools


class Customer:
    def __init__(self, orders):
        assert all(
            order1.location == order2.location
            for order1, order2 in itertools.combinations(orders, 2)
        )
        self.orders = orders
        self.location = orders[0].location
        self.demand = dict(
            sum((Counter(order.get_demand()) for order in orders), Counter())
        )

    def __repr__(self):
        return f"customer ({self.location.x}, {self.location.y})"

    def __hash__(self):
        return id(self)
