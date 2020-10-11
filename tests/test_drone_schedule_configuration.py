from copy import deepcopy

from solvers.drone_schedule_configuration import DroneScheduleConfiguration, Command
from tests.fixtures import full_problem, fixture


class MockCommand(Command):
    def get_string_representation(self):
        return "mock command"


@fixture
def drone_schedule_configuration(full_problem):
    return DroneScheduleConfiguration(drones=full_problem.drones)


def test_append_command(drone_schedule_configuration):
    drone_schedule_configuration = deepcopy(drone_schedule_configuration)

    command = MockCommand()
    drone = drone_schedule_configuration.get_drones()[0]
    drone_schedule_configuration.append_command_to_drone_schedule(drone, command)
    assert drone_schedule_configuration.get_last_drone_command(drone) == command


def test_get_last_command(drone_schedule_configuration):
    drone_schedule_configuration = deepcopy(drone_schedule_configuration)

    command1, command2 = MockCommand(), MockCommand()
    drone = drone_schedule_configuration.get_drones()[0]
    drone_schedule_configuration.append_command_to_drone_schedule(drone, command1)
    drone_schedule_configuration.append_command_to_drone_schedule(drone, command2)
    assert drone_schedule_configuration.get_last_drone_command(drone) == command2


def test_pop_command(drone_schedule_configuration):
    drone_schedule_configuration = deepcopy(drone_schedule_configuration)
    drone = drone_schedule_configuration.get_drones()[0]
    command = MockCommand()
    drone_schedule_configuration.append_command_to_drone_schedule(drone, command)

    assert len(list(drone_schedule_configuration.drone_schedules[drone])) == 1
    drone_schedule_configuration.pop_command_from_drone_schedule(drone)
    assert len(list(drone_schedule_configuration.drone_schedules[drone])) == 0


def test_get_drone_commands(drone_schedule_configuration):
    drone_schedule_configuration = deepcopy(drone_schedule_configuration)
    drone = drone_schedule_configuration.get_drones()[0]
    assert len(drone_schedule_configuration.get_drone_commands(drone)) == 0
