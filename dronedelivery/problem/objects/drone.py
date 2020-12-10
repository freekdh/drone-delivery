from dataclasses import dataclass
from dronedelivery.problem.environment import Location


@dataclass(frozen=True)
class Drone:
    drone_id: int
    start_location: Location
    max_payload: int
