from collections import defaultdict
from copy import copy


class LinearExpression:
    def __init__(self):
        self.variables = defaultdict(lambda: 0)
        self.constant = 0

    def __repr__(self):
        return f"LE with n_var: {len(self.variables)} and const: {self.constant}"

    def add_variable(self, variable, coefficient=1):
        self.variables[variable] += coefficient
        if self.variables[variable] == 0:
            del self.variables[variable]

    def add_constant(self, constant):
        self.constant += constant

    def __copy__(self):
        le = LinearExpression()
        for variable, coefficient in self.variables.items():
            le.add_variable(variable, coefficient)
        le.add_constant(self.constant)
        return le

    def __sub__(self, other):
        le = copy(self)
        for variable, coefficient in other.variables.items():
            le.add_variable(variable, -1 * coefficient)
        le.add_constant(-1 * other.constant)
        return le