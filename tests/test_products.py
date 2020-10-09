from tests.fixtures import full_problem


def test_product_in_a_warehouse(full_problem):
    for product in full_problem.products:
        assert any(
            product in warehouse.get_available_products()
            for warehouse in full_problem.warehouses
        )
