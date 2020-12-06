from .objects import Drone, WareHouse, Grid, Order, Product, Location, Inventory


class LoadProblemFromFile:
    def __init__(self, ProblemClass, file_location):
        self._ProblemClass = ProblemClass
        self._file_location = file_location

        with open(self._file_location) as file:
            self._data = file.read().splitlines()

        self._get_raw_data()

    def get_problem(self):
        return self._ProblemClass(
            warehouses=self.get_warehouses(),
            drones=self.get_drones(),
            products=self.get_products(),
            grid=self.get_grid(),
            orders=self.get_orders(),
            max_turns=self._n_turns,
        )

    def get_orders(self):
        return [
            Order(
                order_id=i,
                location=self._location_order[i],
                demand=self._demand_order[i],
            )
            for i in range(self._n_orders)
        ]

    def get_grid(self):
        return Grid(n_x=self._n_rows_grids, n_y=self._n_collumns_grids)

    def get_drones(self):
        return [
            Drone(drone_id=i, max_payload=self._max_payload)
            for i in range(self._n_drones)
        ]

    def get_warehouses(self):
        return [
            WareHouse(
                warehouse_id=i,
                location=self._location_warehouses[i],
                inventory=self._inventory_warehouses[i],
            )
            for i in range(self._n_warehouses)
        ]

    def get_products(self):
        return [
            Product(product_id=i, weight=self._product_weights[i])
            for i in range(self._n_product_types)
        ]

    def _get_raw_data(self):

        (
            self._n_rows_grids,
            self._n_collumns_grids,
            self._n_drones,
            self._n_turns,
            self._max_payload,
        ) = self._get_int_list(self._data[0])

        self._n_product_types = self._get_n_product_types()

        self._all_product_weights = self._get_int_list(self._data[2])
        self._product_weights = {
            i: self._all_product_weights[i] for i in range(self._n_product_types)
        }
        self._n_warehouses = self._get_n_warehouses()

        (
            self._location_warehouses,
            self._inventory_warehouses,
        ) = self._get_warehouse_data(
            n_warehouses=self._n_warehouses, n_product_types=self._n_product_types
        )

        self._n_orders = int(self._data[24])

        self._location_order, self._demand_order = self._get_order_data(
            n_orders=self._n_orders
        )

    def _get_n_product_types(self):
        return int(self._data[1])

    def _get_n_warehouses(self):
        return int(self._data[3])

    def _get_warehouse_data(self, n_warehouses, n_product_types):
        location_warehouses = dict()
        inventory_warehouses = dict()
        indices = zip(
            range(4, 4 + n_warehouses * 2, 2), range(5, 20 + n_warehouses * 2, 2)
        )
        for index_warehouse, (row_location, row_inventory) in enumerate(indices):
            raw_locations = self._get_int_list(self._data[row_location])
            location_warehouses[index_warehouse] = Location(
                x=raw_locations[0], y=raw_locations[1]
            )
            all_product_inventory = self._get_int_list(self._data[row_inventory])
            inventory = Inventory()
            for i in range(n_product_types):
                inventory.add_product(
                    Product(product_id=i, weight=self._product_weights[i]),
                    n_items=all_product_inventory[i],
                )

            inventory_warehouses[index_warehouse] = inventory

        return location_warehouses, inventory_warehouses

    def _split(self, string):
        return string.split(" ")

    def _to_int(self, string_list):
        return list(map(int, string_list))

    def _get_int_list(self, string):
        return self._to_int(self._split(string))

    def _get_order_data(self, n_orders):
        location_orders = dict()
        demand_orders = dict()
        indices = zip(
            range(25, 26 + n_orders * 3, 3),
            range(26, 26 + n_orders * 3, 3),
            range(27, 26 + n_orders * 3, 3),
        )
        for index_order, (row_location, row_n_items, row_product_type) in enumerate(
            indices
        ):
            raw_locations = self._get_int_list(self._data[row_location])
            location_orders[index_order] = Location(
                x=raw_locations[0], y=raw_locations[1]
            )

            n_items_in_order = int(self._data[row_n_items])
            products_in_order = self._get_int_list(self._data[row_product_type])

            demand_orders[index_order] = [
                Product(
                    product_id=products_in_order[item],
                    weight=self._product_weights[products_in_order[item]],
                )
                for item in range(n_items_in_order)
            ]

        return location_orders, demand_orders


# print(
#     "rows of grid,columns of grid,drones,turns, maxpay load in units(u):",
#     data_list[0],
#     "\n Different product types:",
#     data_list[1],
#     "\n product types weigh:",
#     data_list[2],
#     "\n warehouses:",
#     data_list[3],
#     "\n First warehouse location (row, column):",
#     data_list[4],
#     "\n Inventory of products:",
#     data_list[5],
#     "\n second warehouse location (row, column)  :",
#     data_list[6],
#     "\n Inventory of products at second ware house:",
#     data_list[7],
#     "\n Number of orders:",
#     data_list[24],
#     "\n First order to be delivery at:",
#     data_list[25],
#     "\n Number of items in order:",
#     data_list[26],
#     "\n Items of product types:",
#     data_list[27],
# )
