import pickle
from dronedelivery.product_paths_to_routes.product_paths_to_routes import (
    OrderToProductPaths,
)
from dronedelivery.heuristic_solver.heuristic_solver import HeuristicSolver

from tests.fixtures import problem_and_product_paths
from dronedelivery.output_handlers.write_to_csv import WriteToCSV


def main():

    full_problem, product_paths = pickle.load(
        open("data/product_paths_mip_solution_full_problem.pkl", "rb")
    )
    full_problem, product_paths

    order_to_product_paths = OrderToProductPaths(
        product_paths, full_problem.orders, full_problem.environment
    )

    order_to_paths = order_to_product_paths.solve()

    heuristic_solver = HeuristicSolver(
        drones=full_problem.drones,
        orders_to_routes=order_to_paths,
        environment=full_problem.environment,
    )

    drone_schedule = heuristic_solver.solve()

    write_to_csv = WriteToCSV()
    write_to_csv.run(drone_schedule, output_file="test_location_to_save_csv")


if __name__ == "__main__":
    main()