import os

from Helpers import get_int_list

for dirname, _, filenames in os.walk("/input"):
    for filename in filenames:
        print(os.path.join(dirname, filename))


with open("input/busy_day.in") as file:
    data_list = file.read().splitlines()

n_rows_grids, n_collumns_grids, n_drones, n_turns, max_payload = [int(x) for x in data_list[0].split(" ")]

n_product_types = int(data_list[1])
all_product_weights = [int(x) for x in data_list[2].split(" ")]
product_weights = {i: all_product_weights[i] for i in range(n_product_types)}
n_warehouses = int(data_list[3])


location_warehouses = dict()
inventory_warehouses = dict()

indices = zip(range(4,4+n_warehouses*2,2), range(5,20+n_warehouses*2,2))
for index_warehouse,(row_location,row_inventory) in enumerate(indices):
    location_warehouses[index_warehouse] = [int(x) for x in data_list[row_location].split(" ")]
    all_product_inventory = get_int_list(data_list[row_inventory])
    inventory_warehouses[index_warehouse] = {i: all_product_inventory[i] for i in range(n_product_types)}
n_orders = get_int_list(data_list[24])

print(location_warehouses, inventory_warehouses)
print(

    "rows of grid,columns of grid,drones,turns, maxpay load in units(u):",
    data_list[0],
    "\n Different product types:",
    data_list[1],
    "\n product types weigh:",
    data_list[2],
    "\n warehouses:",
    data_list[3],
    "\n First warehouse location (row, column):",
    data_list[4],
    "\n Inventory of products:",
    data_list[5],
    "\n second warehouse location (row, column)  :",
    data_list[6],
    "\n Inventory of products at second ware house:",
    data_list[7],
    "\n Number of orders:",
    data_list[24],
    "\n First order to be delivery at:",
    data_list[25],
    "\n Number of items in order:",
    data_list[26],
    "\n Items of product types:",
    data_list[27],
)

