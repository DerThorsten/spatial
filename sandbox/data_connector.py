import pandas as pd
import numpy as np
import os
import sqlite3

from sandbox.folders import basel_patient_data_path, \
    zurich_patient_data_path, \
    single_cell_data_path, \
    staining_data_path, \
    whole_image_data_path, \
    get_processed_data_folder

database_single_cell = os.path.join(get_processed_data_folder(),
                                    os.path.basename(single_cell_data_path.replace('.csv', '.db')))


basel_patient_data = pd.read_csv(basel_patient_data_path)
zurich_patient_data = pd.read_csv(zurich_patient_data_path)
staining_data = pd.read_csv(staining_data_path)
whole_image_data = pd.read_csv(whole_image_data_path)

sqlite3.register_adapter(np.int64, lambda val: int(val))
# the connection will be closed when the program exits
single_cell_data_connection = sqlite3.connect(database_single_cell)

