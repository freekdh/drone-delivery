from tests.fixtures import full_problem
from problem.objects.grid import Location
from problem.objects.warehouse import WareHouse
from unittest.mock import Mock


def test_warehouses_in_environment(full_problem):
    for warehouse in full_problem.warehouses:
        assert warehouse in full_problem.environment


def test_orders_in_environment(full_problem):
    for order in full_problem.orders:
        assert order in full_problem.environment


def test_get_all_locations(full_problem):
    assert (
        len(list(full_problem.environment.get_all_locations()))
        == full_problem.grid.n_x * full_problem.grid.n_y
    )


def test_get_nearest_warehouse(full_problem):
    place1 = Mock()
    place1.location = Location(x=10, y=30)
    nearest_warehouse = full_problem.environment.get_nearest_warehouse(place1)
    assert isinstance(nearest_warehouse, WareHouse)


def test_get_distance(full_problem):
    place1 = Mock()
    place1.location = Location(x=10, y=40)

    place2 = Mock()
    place2.location = Location(x=15, y=50)
    distance = full_problem.environment.get_distance(place1, place2)
    assert distance == 12
