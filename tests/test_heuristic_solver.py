from dronedelivery.product_paths_to_routes.product_paths_to_routes import (
    OrderToProductPaths,
)
from dronedelivery.heuristic_solver.heuristic_solver import HeuristicSolver
from dronedelivery.solvers.drone_schedule_configuration import (
    DroneScheduleConfiguration,
)
from tests.fixtures import problem_and_product_paths
from pytest import fixture
from dronedelivery.simulator.objective_simulator import Simulator


@fixture
def heuristic_solver(problem_and_product_paths):
    full_problem, product_paths = (
        problem_and_product_paths[0],
        problem_and_product_paths[1],
    )

    order_to_product_paths = OrderToProductPaths(
        product_paths, full_problem.orders, full_problem.get_environment()
    )

    order_to_paths = order_to_product_paths.solve()

    return HeuristicSolver(
        drones=full_problem.drones,
        orders_to_routes=order_to_paths,
        environment=full_problem.get_environment(),
    )


@fixture
def drone_schedule_after_solving(heuristic_solver):
    return heuristic_solver.solve()


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


def test_drone_schedule(problem_and_product_paths, drone_schedule_after_solving):
    full_problem, product_paths = (
        problem_and_product_paths[0],
        problem_and_product_paths[1],
    )

    environment = full_problem.get_environment()

    simulator = Simulator(full_problem.max_turns)
    simulator.run(drone_schedule_after_solving, environment)

    deliverd_orders = environment.get_delivered_orders()

    assert len(list(deliverd_orders)) == len(full_problem.orders)
