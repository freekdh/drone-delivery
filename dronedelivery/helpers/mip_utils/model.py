from dataclasses import dataclass

from .linear_expression import LinearExpression


@dataclass
class Model:
    decision_variables: list
    objective: LinearExpression
    constraints: list
