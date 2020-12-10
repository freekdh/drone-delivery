from pytest import fixture
import random
from statistics import mean
import pickle

from dronedelivery.problem.problem import Problem
from dronedelivery.solvers.drone_schedule_configuration import (
    DroneScheduleConfiguration,
)
from dronedelivery.solvers.drone_schedule_configuration import (
    Load,
    Unload,
    Deliver,
    Wait,
)
from dronedelivery.solve_product_path.solve_product_path import SolveProductTrips
from dronedelivery.utils.mip_utils.mip_solver import MipSolver


@fixture(scope="session")
def full_problem():
    data_file = "data/busy_day.in"
    return Problem.from_file(data_file)


@fixture(scope="session")
def nonsense_drone_schedule_configuration():
    data_file = "data/busy_day.in"
    full_problem = Problem.from_file(data_file)

    drone_schedule_configuration = DroneScheduleConfiguration(
        drones=full_problem.drones
    )

    for drone in full_problem.drones:
        for _ in range(random.randint(0, 5)):
            random_command = get_random_command(full_problem)
            drone_schedule_configuration.append_command_to_drone_schedule(
                drone, random_command
            )

    return drone_schedule_configuration


@fixture(scope="session")
def problem_and_product_paths():
    try:
        full_problem, product_paths = pickle.load(
            open("data/product_paths_mip_solution_full_problem.pkl", "rb")
        )
        return full_problem, product_paths
    except:
        data_file = "data/busy_day.in"
        full_problem = Problem.from_file(data_file)
        max_flight_capacity = mean(drone.max_payload for drone in full_problem.drones)
        solve_product_trips = SolveProductTrips(
            customers=full_problem.customers,
            hubs=full_problem.warehouses,
            products=full_problem.products,
            max_flight_capacity=max_flight_capacity,
            environment=full_problem.get_environment(),
        )
        product_paths = solve_product_trips.solve(MipSolver, max_seconds=120)
        pickle.dump(
            (full_problem, product_paths),
            open("data/product_paths_mip_solution_full_problem.pkl", "wb"),
        )
        return full_problem, product_paths


def get_random_command(problem):
    commands = [Load, Unload, Deliver, Wait]
    chosen_command = random.choice(commands)
    chosen_drone = random.choice(problem.drones)
    if chosen_command == Load:
        return Load(
            drone=chosen_drone,
            product=get_random(problem.products),
            n_items=random.randint(1, 10),
            warehouse=get_random(problem.warehouses),
        )
    elif chosen_command == Unload:
        return Unload(
            drone=chosen_drone,
            product=get_random(problem.products),
            n_items=random.randint(1, 10),
            warehouse=get_random(problem.warehouses),
        )
    elif chosen_command == Deliver:
        return Deliver(
            drone=chosen_drone,
            order=get_random(problem.orders),
            product=get_random(problem.products),
            n_items=random.randint(1, 10),
        )
    elif chosen_command == Wait:
        return Wait(drone=chosen_drone, wait_turns=random.randint(1, 5))


def get_random(items):
    return random.choice(items)
