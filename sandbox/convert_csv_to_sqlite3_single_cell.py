import re
import pandas as pd
import subprocess
import progressbar

# single_cell_data_path = '/Users/macbook/temp/test.csv'
# database_single_cell = '/Users/macbook/temp/test_processed.db'

from sandbox.folders import single_cell_data_path
from sandbox.data_connector import single_cell_data_connection


def convert_csv_to_sqlite3_single_cell():
    cursor = single_cell_data_connection.cursor()
    single_cell_reduced = pd.read_csv(single_cell_data_path, nrows=0)
    columns = sorted(single_cell_reduced.columns.values)
    columns_channels_removed = sorted(set(map(lambda x: re.sub(r'(.*?_)c[0-9]+', r'\1xxx', x), columns)))
    print('readable version of the columns:')
    print(columns_channels_removed)
    # these columns are converted into bytes by sqlite3, but they are integer, here we explicitly specify that they
    # are integers
    types = {c: 'REAL' for c in columns}
    # I would have guessed that AreaShape_Area would have been a double, but it is an int In the .csv,
    # AreaShape_Center_X and Location_Center_X (the same for Y) are both double, but the first, always (I checked)
    # represents an integer; this integer is often, but not always, the rounded value of the second one
    for c in ['AreaShape_Area', 'AreaShape_Center_X', 'AreaShape_Center_Y', 'ImageNumber',
              'Neighbors_FirstClosestObjectNumber_1',
              'Neighbors_SecondClosestObjectNumber_1', 'Number_Object_Number', 'ObjectNumber', 'Parent_RescaledCells']:
        types[c] = 'INT'
    typed_columns = [f'{c} {t}' for c, t in types.items()]
    sql_typed_command_columns = '(' + ', '.join(typed_columns) + ')'
    sql_untyped_command_columns = '(' + ', '.join(columns) + ')'
    sql_command_placeholder = '(' + ', '.join(['?'] * len(columns)) + ')'
    sql_command = f'CREATE TABLE single_cell_data {sql_typed_command_columns};'
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
            single_cell_data_connection.commit()
            i += chunksize
            bar.update(min(i, lines))
    print('creating indexes')
    cursor.execute('CREATE INDEX ImageNumber_index on single_cell_data (ImageNumber)')
    cursor.execute('CREATE INDEX AreaShape_Center_X_index on single_cell_data (AreaShape_Center_X)')
    cursor.execute('CREATE INDEX AreaShape_Center_Y_index on single_cell_data (AreaShape_Center_Y)')
    print('finished creating the database')


if __name__ == '__main__':
    convert_csv_to_sqlite3_single_cell()


def cmd(sql_command, print_values=False, *args):
    cursor = single_cell_data_connection.cursor()
    cursor.execute(sql_command, *args)
    l = cursor.fetchall()
    print(len(l))
    if print_values:
        print(l)
