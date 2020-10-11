from abc import ABC, abstractmethod
from collections import namedtuple

Solution = namedtuple("Solution", ["drone_schedule_configuration", "objective"])


class Solver(ABC):
    def __init__(self, objective_function, constraint_handler):
        self.objective_function = objective_function
        self.constraint_handler = constraint_handler

    @abstractmethod
    def solve(self, **kwargs):
        """
        return: Solution
        """
        raise NotImplementedError

    @abstractmethod
    def __str__(self):
        raise NotImplementedError

    def get_solution(self):
        return Solution(self.drone_schedule_configuration, self.objective)
