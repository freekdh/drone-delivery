import pickle
from collections import defaultdict


def test_product_to_paths():
    full_problem, product_paths = pickle.load(
        open("data/product_paths_mip_solution_full_problem.pkl", "rb")
    )

    full_problem, product_paths

    customer_to_product = defaultdict(list)
    for path in product_paths["hub_to_customer"]:
        for _ in range(path.product_quantity):
            customer_to_product[path.destination.location].append(path.product_type)

    order_to_product = defaultdict(list)
    for order in full_problem.orders:
        for product, product_quantity in order.get_demand().items():
            for _ in range(product_quantity):
                order_to_product[order.location].append(product)

    locations = set(order.location for order in full_problem.orders)

    assert all(
        len(customer_to_product[location]) == len(order_to_product[location])
        for location in locations
    )
