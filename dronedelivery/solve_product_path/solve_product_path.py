import itertools

from dronedelivery.utils.mip_utils.variables import IntegerVariable
from dronedelivery.utils.mip_utils.linear_expression import LinearExpression
from dronedelivery.utils.mip_utils.constraints import (
    EqualityConstraint,
    LE_InequalityConstraint,
)
from dronedelivery.utils.mip_utils.model import Model


class SolveProductPath:
    def __init__(self, customers, hubs, products, max_flight_capacity, environment):
        self.environment = environment
        self.max_flight_capacity = max_flight_capacity

        variables = self.get_variables(customers, hubs, products)
        objective = self.get_objective(customers, hubs)
        constraints = self.get_constraints(customers, hubs, products)

        self.model = Model(
            variables=variables, objective=objective, constraints=constraints
        )

    def solve(self, Mip_Solver, max_seconds=120):
        mip_solver = Mip_Solver(model=self.model)
        return mip_solver.solve(max_seconds=max_seconds)

    def get_variables(self, customers, hubs, products):
        self.n_flights_variables = self._get_n_flights_variables(customers, hubs)
        self.n_product_move_variables = self._get_n_products_move_variables(
            customers, hubs, products
        )
        self.n_flights_hub_to_hub_variables = self._get_n_flights_hub_to_hub(hubs)
        self.n_products_move_hub_to_hub_variables = (
            self._get_n_products_move_hub_to_hub(hubs, products)
        )
        return (
            list(self.n_flights_variables.values())
            + list(self.n_product_move_variables.values())
            + list(self.n_flights_hub_to_hub_variables.values())
            + list(self.n_products_move_hub_to_hub_variables.values())
        )

    def get_objective(self, customers, hubs):
        le = LinearExpression()
        for customer, hub in itertools.product(customers, hubs):
            le.add_variable(
                variable=self.n_flights_variables[customer, hub],
                coefficient=self.environment.get_distance(hub, customer),
            )

        for hub1, hub2 in itertools.product(hubs, hubs):
            if hub1 != hub2:
                le.add_variable(
                    variable=self.n_flights_hub_to_hub_variables[hub1, hub2],
                    coefficient=self.environment.get_distance(hub1, hub2),
                )
        return le

    def get_constraints(self, customers, hubs, products):
        demand_constraints = self._get_demand_constraints(customers, products, hubs)
        supply_constraints = self._get_supply_constraints(customers, products, hubs)
        trips_constraints = self._get_trips_constraints(customers, products, hubs)
        trips_hub_hub_constraints = self._get_trips_hub_to_hub_constraints(
            products, hubs
        )
        return (
            demand_constraints
            + supply_constraints
            + trips_constraints
            + trips_hub_hub_constraints
        )

    def _get_n_flights_variables(self, customers, hubs):
        return {
            (customer, hub): FlightsCustomerHub(
                name={f"number of flights from {hub} to {customer}"},
                lower_bound=0,
                data={"customer": customer, "hub": hub},
            )
            for customer, hub in itertools.product(customers, hubs)
        }

    def _get_n_products_move_variables(self, customers, hubs, products):
        return {
            (customer, hub, product): ProductsMoveCustomerHub(
                name={
                    f"number of products of product type {product} from {hub} to {customer}"
                },
                lower_bound=0,
                upper_bound=customer.demand[product]
                if product in customer.demand
                else 0,
                data={"customer": customer, "hub": hub, "product": product},
            )
            for customer, hub, product in itertools.product(customers, hubs, products)
        }

    def _get_n_flights_hub_to_hub(self, hubs):
        return {
            (hub1, hub2): FlightsHubHub(
                name={f"number of flights from {hub1} to {hub2}"},
                lower_bound=0,
                data={"hub1": hub1, "hub2": hub2},
            )
            for hub1, hub2 in itertools.product(hubs, hubs)
            if hub1 != hub2
        }

    def _get_n_products_move_hub_to_hub(self, hubs, products):
        return {
            (hub1, hub2, product): ProductsMoveHubHub(
                name={
                    f"number of products of product type {product} from {hub1} to {hub2}"
                },
                lower_bound=0,
                data={"hub1": hub1, "hub2": hub2, "product": product},
            )
            for hub1, hub2, product in itertools.product(hubs, hubs, products)
            if hub1 != hub2
        }

    def _get_demand_constraints(self, customers, products, hubs):
        constraints = []
        for customer, product in itertools.product(customers, products):
            if product in customer.demand:
                lhs = LinearExpression()
                for hub in hubs:
                    lhs.add_variable(
                        self.n_product_move_variables[(customer, hub, product)]
                    )
                constraints.append(
                    EqualityConstraint(lhs=lhs, rhs=customer.demand[product])
                )
        return constraints

    def _get_supply_constraints(self, customers, products, hubs):
        constraints = []
        for hub, product in itertools.product(hubs, products):
            le_1 = LinearExpression()
            for customer in customers:
                le_1.add_variable(
                    self.n_product_move_variables[(customer, hub, product)]
                )

            le_2 = LinearExpression()
            for hub_ in hubs:
                if hub_ != hub:
                    le_2.add_variable(
                        self.n_products_move_hub_to_hub_variables[(hub_, hub, product)],
                        1,
                    )
                    le_2.add_variable(
                        self.n_products_move_hub_to_hub_variables[(hub, hub_, product)],
                        -1,
                    )

            constraints.append(
                LE_InequalityConstraint(
                    lhs=le_1 - le_2, rhs=hub.get_inventory()[product]
                )
            )
        return constraints

    def _get_trips_constraints(self, customers, products, hubs):
        constraints = []
        for customer, hub in itertools.product(customers, hubs):
            le_1 = LinearExpression()
            for product in products:
                le_1.add_variable(
                    self.n_product_move_variables[(customer, hub, product)]
                )

            le_2 = LinearExpression()
            le_2.add_variable(
                self.n_flights_variables[(customer, hub)], self.max_flight_capacity
            )

            constraints.append(LE_InequalityConstraint(lhs=le_1 - le_2, rhs=0))
        return constraints

    def _get_trips_hub_to_hub_constraints(self, products, hubs):
        constraints = []
        for hub1, hub2 in itertools.product(hubs, hubs):
            if hub1 != hub2:
                le_1 = LinearExpression()
                for product in products:
                    le_1.add_variable(
                        self.n_products_move_hub_to_hub_variables[(hub1, hub2, product)]
                    )

                le_2 = LinearExpression()
                le_2.add_variable(
                    self.n_flights_hub_to_hub_variables[(hub1, hub2)],
                    self.max_flight_capacity,
                )

                constraints.append(LE_InequalityConstraint(lhs=le_1 - le_2, rhs=0))
        return constraints


class FlightsCustomerHub(IntegerVariable):
    pass


class ProductsMoveCustomerHub(IntegerVariable):
    pass


class FlightsHubHub(IntegerVariable):
    pass


class ProductsMoveHubHub(IntegerVariable):
    pass
