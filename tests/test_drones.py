from tests.fixtures import full_problem


def test_n_drones(full_problem):
    assert len(full_problem.drones) == 30


def test_drone_id(full_problem):
    list_of_drones = [drone for drone in full_problem.drones]
    list_of_drones.sort(key=lambda x: x.drone_id)
    for drone1, drone2 in zip(list_of_drones, list_of_drones[1:]):
        assert drone1.drone_id == drone2.drone_id - 1


def test_payload_drones(full_problem):
    for drone in full_problem.drones:
        assert drone.max_payload == 200


def test_drone_is_hashable(full_problem):
    assert {drone: None for drone in full_problem.drones}
