from dataclasses import dataclass

from .linear_expression import LinearExpression


@dataclass
class Model:
    variables: list
    objective: LinearExpression
    constraints: list
