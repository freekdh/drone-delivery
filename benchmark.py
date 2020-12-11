from dronedelivery.simulator import Simulator
from dronedelivery.objective_calculator import ObjectiveCalculator
from dronedelivery.product_paths_to_routes.product_paths_to_routes import (
    OrderToProductPaths,
)
from dronedelivery.heuristic_solver.heuristic_solver import HeuristicSolver
import pickle


def main():

    full_problem, product_paths = pickle.load(
        open("data/product_paths_mip_solution_full_problem.pkl", "rb")
    )

    order_to_product_paths = OrderToProductPaths(
        product_paths, full_problem.orders, full_problem.get_environment()
    )

    order_to_paths = order_to_product_paths.solve()

    heuristic_solver = HeuristicSolver(
        drones=full_problem.drones,
        orders_to_routes=order_to_paths,
        environment=full_problem.get_environment(),
    )

    drone_schedule = heuristic_solver.solve()

    simulator = Simulator(max_turns=full_problem.max_turns)
    objective_calculator = ObjectiveCalculator(
        orders=full_problem.orders,
        simulator=simulator,
        max_turns=full_problem.max_turns,
    )

    environment = full_problem.get_environment()
    objective = objective_calculator.get_objective(drone_schedule, environment)

    print(f"The objective for this drone schedule in {objective}")


if __name__ == "__main__":
    main()