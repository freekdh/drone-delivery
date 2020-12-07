from dronedelivery.product_paths_to_routes.product_paths_to_routes import (
    OrderToProductPaths,
)

from tests.fixtures import problem_and_product_paths


def test_order_to_product_paths_integration(problem_and_product_paths):
    full_problem, product_paths = (
        problem_and_product_paths[0],
        problem_and_product_paths[1],
    )

    order_to_product_paths = OrderToProductPaths(
        product_paths, full_problem.orders, full_problem.environment
    )

    order_to_paths = order_to_product_paths.solve()

    assert order_to_paths