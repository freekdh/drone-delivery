from dronedelivery.solvers.drone_schedule_configuration import (
    DroneScheduleConfiguration,
)
import math


class ObjectiveCalculator:
    def __init__(self, problem, simulator):
        self.simulator = simulator
        self.problem = problem

    def get_objective(self, drone_schedule: DroneScheduleConfiguration):
        environment = self.problem.get_environment()
        self.simulator.run(drone_schedule, environment)
        return sum(
            self._get_order_score(order, environment) for order in self.problem.orders
        )

    def _get_order_score(self, order, environment):
        try:
            return math.ceil(
                100
                * (self.max_turns - environment.get_time_last_product_delivered(order))
                / (self.max_turns)
            )
        except TypeError:
            return 0


class DroneSimulator:
    def __init__(self, drone, ordered_commands, environment):
        self.drone = drone
        self.ordered_commands = ordered_commands
        self.environment = environment

        self.time_to_actions = self._get_actions()

    def get_action(self, t):
        return self.time_to_actions[t]

    def has_action(self, t):
        return True if t in self.time_to_actions else False

    def _get_actions(self):
        current_time = 0
        current_location = self.drone.start_location
        time_to_action = dict()
        for command in self.ordered_commands:
            time_after_travel = current_time + command.get_travel_turns(
                previous_location=current_location, environment=self.environment
            )
            time_after_execution = time_after_travel + command.get_execution_turns()
            time_to_action[time_after_travel] = command
            current_time = time_after_execution
            current_location = command.get_location()
        return time_to_action


class Simulator:
    def __init__(self, max_turns):
        self.max_turns = max_turns

    def run(self, drone_schedule, environment):
        drone_simulators = [
            DroneSimulator(
                drone=drone,
                ordered_commands=drone_schedule.get_drone_commands(drone),
                environment=environment,
            )
            for drone in drone_schedule.get_drones()
        ]

        for t in range(self.max_turns):
            drone_actions = [
                drone_simulator.get_action(t)
                for drone_simulator in drone_simulators
                if drone_simulator.has_action(t)
            ]
            environment.apply_actions(drone_actions, t)
