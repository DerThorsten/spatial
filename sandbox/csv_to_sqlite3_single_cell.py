import os
import re
import numpy as np
import sqlite3
import pandas as pd
import subprocess
import progressbar

from sandbox.folders import single_cell_data_path, get_processed_data_folder

database_single_cell = os.path.join(get_processed_data_folder(),
                                    os.path.basename(single_cell_data_path.replace('.csv', '.db')))


def convert_csv_to_sqlite3_single_cell():
    single_cell_data_path = '/Users/macbook/temp/test.csv'
    database_single_cell = '/Users/macbook/temp/test_processed.db'
    sqlite3.register_adapter(np.int64, lambda val: int(val))
    connection = sqlite3.connect(database_single_cell)
    cursor = connection.cursor()
    single_cell_reduced = pd.read_csv(single_cell_data_path, nrows=0)
    columns = sorted(single_cell_reduced.columns.values)
    # these columns are converted into bytes by sqlite3, but they are integer, here we esplicitely specify that they are integers
    types = {c: '' for c in columns}
    for c in ['AreaShape_Area', 'ImageNumber', 'Neighbors_FirstClosestObjectNumber_1',
              'Neighbors_SecondClosestObjectNumber_1', 'Number_Object_Number', 'ObjectNumber', 'Parent_RescaledCells']:
        types[c] = 'INT'
    typed_columns = [f'{c} {t}' for c, t in types.items()]
    sql_typed_command_columns = '(' + ', '.join(typed_columns) + ')'
    sql_untyped_command_columns = '(' + ', '.join(columns) + ')'
    sql_command_placeholder = '(' + ', '.join(['?'] * len(columns)) + ')'
    sql_command = f'CREATE TABLE single_cell_data {sql_typed_command_columns};'
    print(sql_command)
    cursor.execute(sql_command)
    print('determining the number of rows to parse')
    lines = subprocess.check_output('wc -l ' + single_cell_data_path, shell=True).decode('utf-8').rstrip('\n')
    lines = int(re.sub(r'\s+([0-9]+).*', r'\1', lines))

    with progressbar.ProgressBar(max_value=lines) as bar:
        i = 0
        bar.update(i)
        chunksize = 10000
        for chunk in pd.read_csv(single_cell_data_path, chunksize=chunksize):
            chunk = chunk.reindex(sorted(chunk.columns), axis=1)
            sql_command = f'INSERT INTO single_cell_data {sql_untyped_command_columns} VALUES {sql_command_placeholder};'
            cursor.executemany(sql_command, list(chunk.to_records(index=False)))
            connection.commit()
            i += chunksize
            bar.update(min(i, lines))
    print('creating index on ImageNumber')
    cursor.execute('CREATE INDEX ImageNumber_index on single_cell_data (ImageNumber)')
    connection.close()
    print('finished creating the database')


if __name__ == '__main__':
    convert_csv_to_sqlite3_single_cell()


def cmd(sql_command, *args):
    database_single_cell = '/Users/macbook/temp/test_processed.db'
    sqlite3.register_adapter(np.int64, lambda val: int(val))
    connection = sqlite3.connect(database_single_cell)
    cursor = connection.cursor()
    cursor.execute(sql_command, *args)
    l = cursor.fetchall()
    print(len(l))
    print(l)
    connection.close()

