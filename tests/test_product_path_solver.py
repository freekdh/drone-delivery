from dronedelivery.solve_product_path.solve_product_path import SolveProductTrips
from dronedelivery.utils.mip_utils.mip_solver import MipSolver
from statistics import mean

from tests.fixtures import full_problem


def test_product_path_solver_integration(full_problem):
    max_flight_capacity = mean(drone.max_payload for drone in full_problem.drones)

    customers = full_problem.get_customers()[:20]
    products = full_problem.products[:20]
    hubs = full_problem.warehouses[:10]

    solve_product_trips = SolveProductTrips(
        customers=customers,
        hubs=hubs,
        products=products,
        max_flight_capacity=max_flight_capacity,
        environment=full_problem.get_environment(),
    )

    product_trips = solve_product_trips.solve(Mip_Solver=MipSolver, max_seconds=60)

    assert product_trips

    customer_demand = {
        customer: {
            your_key: customer.demand[your_key]
            for your_key in products
            if your_key in customer.demand
        }
        for customer in customers
    }

    # apply trips to customers to see if everything is delivered
    for trip in product_trips["hub_to_customer"]:
        customer_demand[trip.destination][trip.product_type] -= trip.product_quantity

    for customer, demanded_products in customer_demand.items():
        for product, still_need_to_be_delivered in demanded_products.items():
            assert still_need_to_be_delivered == 0
