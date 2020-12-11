from dataclasses import dataclass


@dataclass(frozen=True)
class IntegerVariable:
    name: str
    lower_bound: int = None
    upper_bound: int = None
    data: dict = None

    def __hash__(self):
        return id(self)
