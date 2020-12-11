import pickle

from dronedelivery.product_paths_to_routes.product_paths_to_routes import (
    OrderToProductPaths,
)
from dronedelivery.heuristic_solver.heuristic_solver import HeuristicSolver


def test_product_path_to_route():
    full_problem, product_paths = pickle.load(
        open("data/product_paths_mip_solution_full_problem.pkl", "rb")
    )
    full_problem, product_paths

    order_to_product_paths = OrderToProductPaths(
        product_paths, full_problem.orders, full_problem.get_environment()
    )

    order_to_paths = order_to_product_paths.solve()

    assert len(order_to_paths) == len(full_problem.orders)

    for order, order_to_trip in order_to_paths.items():
        demanded_items = sum(
            product_quantity for product, product_quantity in order.get_demand().items()
        )

        assert len(list(order_to_trip.product_routes)) == demanded_items
