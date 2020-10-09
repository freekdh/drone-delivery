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

