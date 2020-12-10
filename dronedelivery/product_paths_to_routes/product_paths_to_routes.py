from collections import defaultdict
from dataclasses import dataclass
from copy import copy
import math


@dataclass(frozen=True, eq=False)
class TripQ1:
    origin: str
    destination: str
    product_type: str

    def copy_with_new_destination(self, new_destination):
        return TripQ1(self.origin, new_destination, self.product_type)


@dataclass
class ProductRoute:
    trips: list


@dataclass
class OrderToTrips:
    order: str
    product_routes: dict

    def get_total_flights(self, max_flight_capacity):
        trips = self.get_all_trips()
        count_trips_based_on_location = defaultdict(lambda: 0)

        for trip in trips:
            count_trips_based_on_location[
                (trip.origin, trip.destination)
            ] += trip.product_type.weight

        total_flights = sum(
            math.ceil(weight / max_flight_capacity)
            for weight in count_trips_based_on_location.values()
        )

        return total_flights

    def get_all_trips(self):
        trips = set()
        for product_route in self.product_routes.values():
            for trip in product_route.trips:
                trips.add(trip)
        return trips


class OrderToProductPaths:
    def __init__(self, product_paths, orders, environment):
        self._product_paths = product_paths
        self._orders = orders
        self._environment = environment

    def solve(self):
        unique_trips_hub_to_customer = self.get_unique_trips_hub_to_customer()
        unique_trips_hub_to_hub = self.get_unique_trips_hub_to_hub()

        sorted_orders = copy(self._orders)
        sorted_orders.sort(key=lambda x: len(x.demand), reverse=True)

        order_to_product_paths = dict()
        for order in sorted_orders:
            product_routes = {}
            for product in order.demand:
                trips = self.get_trips(
                    order,
                    product,
                    unique_trips_hub_to_customer,
                    unique_trips_hub_to_hub,
                )
                product_routes[product] = ProductRoute(trips=trips)

            order_to_product_paths[order] = OrderToTrips(order, product_routes)

        return order_to_product_paths

    def get_unique_trips_hub_to_customer(self):
        unique_trips_hub_to_customer = defaultdict(lambda: set())
        for trip in self._product_paths["hub_to_customer"]:
            for _ in range(trip.product_quantity):
                unique_trips_hub_to_customer[
                    (trip.destination.location, trip.product_type)
                ].add(
                    TripQ1(
                        origin=trip.origin,
                        destination=trip.destination,
                        product_type=trip.product_type,
                    )
                )
        return unique_trips_hub_to_customer

    def get_unique_trips_hub_to_hub(self):
        unique_trips_hub_to_hub = defaultdict(lambda: set())
        for trip in self._product_paths["hub_to_hub"]:
            for _ in range(trip.product_quantity):
                unique_trips_hub_to_hub[
                    (trip.destination.location, trip.product_type)
                ].add(
                    TripQ1(
                        origin=trip.origin,
                        destination=trip.destination,
                        product_type=trip.product_type,
                    )
                )
        return unique_trips_hub_to_hub

    def get_trips(
        self, order, product, unique_trips_hub_to_customer, unique_trips_hub_to_hub
    ):
        hub_to_customer_trip = max(
            unique_trips_hub_to_customer[(order.location, product)],
            key=lambda x: self._environment.get_distance(
                x.origin.location, x.destination.location
            ),
        )
        unique_trips_hub_to_customer[(order.location, product)].remove(
            hub_to_customer_trip
        )

        hub_to_customer_trip = hub_to_customer_trip.copy_with_new_destination(order)

        try:
            hub_to_hub_trip = max(
                unique_trips_hub_to_hub[
                    (hub_to_customer_trip.origin.location, product)
                ],
                key=lambda x: self._environment.get_distance(
                    x.origin.location, x.destination.location
                ),
            )
            unique_trips_hub_to_hub[
                (hub_to_customer_trip.origin.location, product)
            ].remove(hub_to_hub_trip)

            trips = [hub_to_hub_trip, hub_to_customer_trip]
        except ValueError:
            trips = [hub_to_customer_trip]
        return trips
