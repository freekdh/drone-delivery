from dataclasses import dataclass


@dataclass(frozen=True)
class Drone:
    drone_id: int
    max_payload: int
