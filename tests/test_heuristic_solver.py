from dronedelivery.product_paths_to_routes.product_paths_to_routes import (
    OrderToProductPaths,
)
from dronedelivery.heuristic_solver.heuristic_solver import HeuristicSolver
from dronedelivery.solvers.drone_schedule_configuration import (
    DroneScheduleConfiguration,
)
from tests.fixtures import problem_and_product_paths
from pytest import fixture


@fixture
def heuristic_solver(problem_and_product_paths):
    full_problem, product_paths = (
        problem_and_product_paths[0],
        problem_and_product_paths[1],
    )

    order_to_product_paths = OrderToProductPaths(
        product_paths, full_problem.orders, full_problem.environment
    )

    order_to_paths = order_to_product_paths.solve()

    return HeuristicSolver(drones=full_problem.drones, orders_to_routes=order_to_paths)


def test_heuristic_solver(heuristic_solver):
    drone_schedule = heuristic_solver.solve()
    assert isinstance(drone_schedule, DroneScheduleConfiguration)


def test_get_trip_to_priority_databse(heuristic_solver):
    trip_to_databases = heuristic_solver._get_trip_to_priority_database()
    assert isinstance(trip_to_databases, dict)


def test_get_sorted_order_to_routes_by_number_of_flights(heuristic_solver):
    sorted_order_to_route = (
        heuristic_solver._get_sorted_order_to_routes_by_number_of_flights()
    )

    num_flights_orders = [
        order_route.get_total_flights(200)
        for order, order_route in sorted_order_to_route.items()
    ]

    assert all(
        num_flights_orders[i] <= num_flights_orders[i + 1]
        for i in range(len(num_flights_orders) - 1)
    )
