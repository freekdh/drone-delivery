from dronedelivery.helpers.linked_list import LinkedList, LinkedListNode, EmptyListError
from abc import ABC, abstractmethod


class DroneScheduleConfiguration:
    def __init__(self, drones):
        self.drone_schedules = {drone: [] for drone in drones}

    def append_command_to_drone_schedule(self, drone, command):
        self.drone_schedules[drone].append(command)

    def pop_command_from_drone_schedule(self, drone):
        try:
            self.drone_schedules[drone].pop()
        except EmptyListError:
            raise EmptyDroneSchedule("Cannot pop command, no command to pop")

    def get_last_drone_command(self, drone):
        try:
            return list(self.drone_schedules[drone])[-1]
        except AttributeError:
            return None

    def get_drone_commands(self, drone):
        return list(self.drone_schedules[drone])

    def get_drones(self):
        return list(self.drone_schedules.keys())


class Command(LinkedListNode, ABC):
    @abstractmethod
    def get_string_representation(self):
        raise NotImplementedError

    def get_travel_turns(self):
        raise NotImplementedError

    def get_execution_turns(self):
        raise NotImplementedError

    def get_location(self):
        raise NotImplementedError


class Load(Command):
    def __init__(self, drone, product, n_items, warehouse):
        super().__init__()
        self.drone = drone
        self.product = product
        self.n_items = n_items
        self.warehouse = warehouse

    def get_string_representation(self):
        return f"{self.drone.drone_id} L {self.warehouse.warehouse_id} {self.product.product_id} {self.n_items}"

    def get_travel_turns(self, previous_location, environment):
        return environment.get_distance(previous_location, self.warehouse.location)

    def get_execution_turns(self):
        return 1

    def get_location(self):
        return self.warehouse.location


class Unload(Command):
    def __init__(self, drone, product, n_items, warehouse):
        super().__init__()
        self.drone = drone
        self.product = product
        self.n_items = n_items
        self.warehouse = warehouse

    def get_string_representation(self):
        return f"{self.drone.drone_id} U {self.warehouse.warehouse_id} {self.product.product_id} {self.n_items}"

    def get_travel_turns(self, previous_location, environment):
        return environment.get_distance(previous_location, self.warehouse.location)

    def get_execution_turns(self):
        return 1

    def get_location(self):
        return self.warehouse.location


class Deliver(Command):
    def __init__(self, drone, order, product, n_items):
        super().__init__()
        self.drone = drone
        self.product = product
        self.n_items = n_items
        self.order = order

    def get_string_representation(self):
        return f"{self.drone.drone_id} D {self.order.order_id} {self.product.product_id} {self.n_items}"

    def get_travel_turns(self, previous_location, environment):
        return environment.get_distance(previous_location, self.order.location)

    def get_execution_turns(self):
        return 1

    def get_location(self):
        return self.order.location


class Wait(Command):
    def __init__(self, drone, wait_turns):
        super().__init__()
        self.drone = drone
        self.wait_turns = wait_turns

    def get_string_representation(self):
        return f"{self.drone.drone_id} W {self.wait_turns}"

    def get_travel_turns(self, previous_location, environment):
        return 0

    def get_execution_turns(self):
        return self.wait_turns

    def get_location(self):
        raise NotImplementedError


class EmptyDroneSchedule(Exception):
    pass
