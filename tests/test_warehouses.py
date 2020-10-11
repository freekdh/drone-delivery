from tests.fixtures import full_problem
from problem.objects.grid import Location
from problem.objects.warehouse import Inventory


def test_n_warehouses(full_problem):
    assert len(full_problem.warehouses) == 10


def test_warehouse_id(full_problem):
    list_of_warehouses = [warehouse for warehouse in full_problem.warehouses]
    list_of_warehouses.sort(key=lambda x: x.warehouse_id)
    for warehouse1, warehouse2 in zip(list_of_warehouses, list_of_warehouses[1:]):
        assert warehouse1.warehouse_id == warehouse2.warehouse_id - 1


def test_location_of_warehouses(full_problem):
    for warehouse in full_problem.warehouses:
        assert isinstance(warehouse.location, Location)


def test_warehouses_inventory(full_problem):
    for warehouse in full_problem.warehouses:
        assert isinstance(warehouse.inventory, Inventory)
        assert len(list(warehouse.get_available_products())) > 0
