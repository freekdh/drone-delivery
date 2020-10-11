from tests.fixtures import full_problem, fixture
from problem.objects.grid import Location
from collections import defaultdict


def test_n_orders(full_problem):
    assert len(full_problem.orders) == 1250


def test_order_location(full_problem):
    for order in full_problem.orders:
        assert isinstance(order.location, Location)


@fixture
def full_order_demand(full_problem):
    full_demand = defaultdict(lambda: 0)
    for order in full_problem.orders:
        for product in order.demand:
            full_demand[product] += 1
    return full_demand


@fixture
def full_supply(full_problem):
    full_supply = defaultdict(lambda: 0)
    for warehouse in full_problem.warehouses:
        for product in warehouse.inventory.get_available_products():
            full_supply[product] += warehouse.get_available_items(product)
    return full_supply


def test_all_products_appear_in_orders(full_order_demand, full_problem):
    for product in full_problem.products:
        assert product in full_order_demand


def test_product_demand_in_warehouses(full_order_demand, full_supply, full_problem):
    for product in full_problem.products:
        assert full_order_demand[product] <= full_supply[product]
