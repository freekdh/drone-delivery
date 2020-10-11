from dataclasses import dataclass


@dataclass(frozen=True)
class Grid:
    n_x: int
    n_y: int


@dataclass(frozen=True)
class Location:
    x: int
    y: int
