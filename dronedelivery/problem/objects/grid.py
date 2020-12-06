from dataclasses import dataclass


@dataclass(frozen=True)
class Grid:
    n_x: int
    n_y: int


@dataclass(frozen=True)
class Location:
    x: int
    y: int

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
