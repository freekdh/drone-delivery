import math

from dronedelivery.solvers.drone_schedule_configuration import (
    DroneScheduleConfiguration,
)


class ObjectiveCalculator:
    def __init__(self, orders, simulator, max_turns):
        self.simulator = simulator
        self.max_turns = max_turns
        self.orders = orders

    def get_objective(self, drone_schedule: DroneScheduleConfiguration, environment):
        self.simulator.run(drone_schedule, environment)
        return sum(self._get_order_score(order, environment) for order in self.orders)

    def _get_order_score(self, order, environment):
        try:
            return math.ceil(
                100
                * (self.max_turns - environment.get_time_last_product_delivered(order))
                / (self.max_turns)
            )
        except TypeError:
            return 0
