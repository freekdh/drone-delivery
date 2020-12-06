import numpy as np
from mip import Model, MINIMIZE, CBC, xsum, minimize, INTEGER

from .constraints import EqualityConstraint, LE_InequalityConstraint
from .variables import IntegerVariable


class MipModel:
    def __init__(self, model):
        self.m = Model(sense=MINIMIZE, solver_name=CBC)
        self.model_variables = self._add_variables_to_model(model.decision_variables)

        self._add_constraints_to_model(model.constraints)
        self._add_objective_to_model(model.objective)

    def _add_objective_to_model(self, objective):
        self.m.objective = minimize(
            xsum(
                coeff * self.model_variables[var]
                for var, coeff in objective.variables.items()
            )
        )

    def _add_constraints_to_model(self, constraints):
        for constraint in constraints:
            if isinstance(constraint, LE_InequalityConstraint):
                self.m += (
                    xsum(
                        coeff * self.model_variables[var]
                        for var, coeff in constraint.lhs.variables.items()
                    )
                    <= constraint.rhs
                )

            if isinstance(constraint, EqualityConstraint):
                self.m += (
                    xsum(
                        coeff * self.model_variables[var]
                        for var, coeff in constraint.lhs.variables.items()
                    )
                    == constraint.rhs
                )

    def _add_variables_to_model(self, decision_variables):
        model_variables = {}
        for decision_variable in decision_variables:
            if isinstance(decision_variable, IntegerVariable):
                model_variables[decision_variable] = self.m.add_var(
                    var_type=INTEGER, lb=decision_variable.lower_bound
                )
            else:
                raise Exception(f"Do not recognize this variable {decision_variable}")
        return model_variables

    def solve(self, max_seconds=None):
        self.status = self.m.optimize(max_seconds)
        return {
            name: int(np.round(model_variable.x))
            for name, model_variable in self.model_variables.items()
        }
