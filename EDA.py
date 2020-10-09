import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


with open('input/busy_day.in') as file:
    data_list = file.read().splitlines()

# lets get all the 10 ware house co-ordinates
ware_house_locs = data_list[4:24:2]
ware_house_rows = [ware_house_r.split()[0] for ware_house_r in ware_house_locs]
ware_house_cols = [ware_house_c.split()[1] for ware_house_c in ware_house_locs]

warehouse_df = pd.DataFrame({'ware_house_row': ware_house_rows, 'ware_house_col': ware_house_cols}).astype(np.uint16)


print('rows of grid,columns of grid,drones,turns, maxpay load in units(u):',data_list[0],
      '\n Different product types:',data_list[1],
      '\n product types weigh:',data_list[2],
      '\n warehouses:',data_list[3],
      '\n First warehouse location at first warehouse (row, column):',data_list[4],
      '\n Inventory of products:',data_list[5],
      '\n second warehouse location (row, column)  :',data_list[6],
      '\n Inventory of products at second ware house:',data_list[7],
      '\n Number of orders:',data_list[24],
      '\n First order to be delivery at:',data_list[25],
      '\n Number of items in order:',data_list[26],
      '\n Items of product types:',data_list[27]    )

# lets get all the 10 ware house co-ordinates
ware_house_locs = data_list[4:24:2]
ware_house_rows = [ware_house_r.split()[0] for ware_house_r in ware_house_locs]
ware_house_cols = [ware_house_c.split()[1] for ware_house_c in ware_house_locs]

warehouse_df = pd.DataFrame({'ware_house_row': ware_house_rows, 'ware_house_col': ware_house_cols}).astype(np.uint16)

# Lets aggregate all the products available at their respoective ware houses

cols=[f'ware_house_{i}' for i in range(len(warehouse_df))]

products_df = pd.DataFrame([x.split() for x in data_list[5:24:2]]).T

products_df.columns=cols