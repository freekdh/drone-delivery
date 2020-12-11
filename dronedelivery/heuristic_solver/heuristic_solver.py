from dronedelivery.solvers.drone_schedule_configuration import (
    DroneScheduleConfiguration,
    Load,
    Deliver,
    Unload,
)
from dronedelivery.helpers.linked_list import LinkedListNode
from dataclasses import dataclass
from collections import defaultdict
from dronedelivery.problem.objects.warehouse import WareHouse
import operator


@dataclass(eq=False)
class TripLL(LinkedListNode):
    def __init__(self, priority, origin, destination, product_type):
        super().__init__()

        self.priority = priority
        self.origin = origin
        self.destination = destination
        self.product_type = product_type


class HeuristicSolver:
    def __init__(self, drones, orders_to_routes, environment):
        self._orders_to_routes = orders_to_routes
        self._drones = drones
        self._orders = orders_to_routes.values()
        self._environment = environment

    def solve(self):
        drone_schedule_configuration = DroneScheduleConfiguration(drones=self._drones)

        trip_to_priority = self._get_trip_to_priority_database()

        self.trips_by_hub_origin = self._get_trips_by_hub_origin(
            list(trip_to_priority.keys())
        )

        while True:
            for drone in self._drones:
                hub = self._choose_best_hub(drone)
                if hub is None:
                    break

                sequence_of_commands = self._get_best_sequence_of_commands(
                    hub=hub, drone=drone
                )

                for command in sequence_of_commands:
                    drone_schedule_configuration.append_command_to_drone_schedule(
                        drone, command
                    )

            hub = self._choose_best_hub(drone)
            if hub is None:
                break
        return drone_schedule_configuration

    def _get_easiest_trip_for_drone(self, current_location, trips):
        min_priority = min(trip.priority for trip in trips)
        max_priority = max(trip.priority for trip in trips)

        if max_priority == min_priority:
            relative_trip_priorities = {trip: 1 / len(trips) for trip in trips}
        else:
            relative_trip_priorities = {
                trip: ((trip.priority - min_priority) / (max_priority - min_priority))
                for trip in trips
            }

        min_distance = min(
            self._environment.get_distance(
                current_location.location, trip.destination.location
            )
            for trip in trips
        )

        max_distance = max(
            self._environment.get_distance(
                current_location.location, trip.destination.location
            )
            for trip in trips
        )

        if min_distance == max_distance:
            relative_distance = {trip: 1 / len(trips) for trip in trips}
        else:
            relative_distance = {
                trip: (
                    (
                        self._environment.get_distance(
                            current_location.location, trip.destination.location
                        )
                        - min_distance
                    )
                    / (max_distance - min_distance)
                )
                for trip in trips
            }

        return max(
            {
                trip: ((1 - relative_distance[trip]) * relative_trip_priorities[trip])
                for trip in trips
            }.items(),
            key=operator.itemgetter(1),
        )[0]

    def _get_best_sequence_of_commands(self, hub, drone, look_n_trips_in_the_future=10):

        total_weight = 0
        trips_for_drone = []
        current_location = hub

        while True:
            filtered_trips = []
            for trip in self.trips_by_hub_origin[hub]:
                if trip.product_type.weight + total_weight > drone.max_payload:
                    continue
                # try:
                #     previous_node = trip.get_previous_node()
                #     if previous_node in self.trips_by_hub_origin[previous_node.origin]:
                #         continue
                # except:
                #     pass

                filtered_trips.append(trip)

                if len(filtered_trips) == 10:
                    break

            if len(filtered_trips) == 0:
                break

            selected_trip = self._get_easiest_trip_for_drone(
                current_location, filtered_trips
            )

            current_location = selected_trip.destination
            total_weight += selected_trip.product_type.weight
            trips_for_drone.append(selected_trip)
            self.trips_by_hub_origin[hub].remove(trips_for_drone[-1])

        commands = []

        trips_for_drone_by_product_type = defaultdict(set)
        for trip in trips_for_drone:
            trips_for_drone_by_product_type[trip.product_type].add(trip)

        for product_type, trips in trips_for_drone_by_product_type.items():
            commands.append(Load(drone, product_type, len(trips), trip.origin)),

        for trip in trips_for_drone:
            if isinstance(trip.destination, WareHouse):
                commands.append(Unload(drone, trip.product_type, 1, trip.destination))
            else:  # TODO, get the right order...
                commands.append(Deliver(drone, trip.destination, trip.product_type, 1))
        return commands

    def _choose_best_hub(self, drone, look_n_trips_in_the_future=10):
        hub_to_score = {}
        remove_keys = set()
        for hub, trips in self.trips_by_hub_origin.items():
            score = sum(trip.priority for trip in trips[:look_n_trips_in_the_future])
            if score == 0:
                assert len(self.trips_by_hub_origin[hub]) == 0
                remove_keys.add(hub)
            else:
                hub_to_score[hub] = score

        for key in remove_keys:
            del self.trips_by_hub_origin[key]

        try:
            return max(
                (hub_and_score for hub_and_score in hub_to_score.items()),
                key=lambda x: x[1],
            )[0]
        except:
            return None

    def _get_trips_by_hub_origin(self, trips):
        trips_by_origin_hub = defaultdict(list)
        for trip in trips:
            trips_by_origin_hub[trip.origin].append(trip)

        return trips_by_origin_hub

    def _get_trip_to_priority_database(self):
        sorted_order_to_route = self._get_sorted_order_to_routes_by_number_of_flights()

        order_award = 1300
        trip_to_priority_database = dict()
        for order, order_route in sorted_order_to_route.items():
            product_award = order_award
            for product_route in order_route.product_routes:
                trip_award = product_award
                current_trip = None
                for trip in reversed(product_route.trips):
                    trip_ll = TripLL(**{**trip.__dict__, **{"priority": trip_award}})
                    if current_trip:
                        trip_ll.set_next_node(current_trip)
                        current_trip.set_previous_node(trip_ll)
                    current_trip = trip_ll
                    trip_to_priority_database[trip_ll] = trip_award
                    trip_award -= 1
            order_award -= 1

        return trip_to_priority_database

    def _get_sorted_order_to_routes_by_number_of_flights(self):
        return dict(
            sorted(
                self._orders_to_routes.items(),
                key=lambda item: (item[1].get_total_flights(200), len(item[0].demand)),
            )
        )
