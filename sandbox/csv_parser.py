import pandas as pd
import numpy as np
import os
import sys
import re
import matplotlib.pyplot as plt
from colorama import init, Fore
from sandbox.folders import basel_patient_data_path, \
    zurich_patient_data_path, \
    single_cell_data_path, \
    staining_data_path, \
    whole_image_data_path

if __name__ == '__main__':
    init(autoreset=True)

    basel_patient_data = pd.read_csv(basel_patient_data_path)
    zurich_patient_data = pd.read_csv(zurich_patient_data_path)
    print('shape of the basel data:', basel_patient_data.shape)
    print('shape of the zurich data:', zurich_patient_data.shape)
    basel_columns = set(basel_patient_data.columns.values)
    zurich_columns = set(zurich_patient_data.columns.values)
    a = basel_columns.intersection(zurich_columns)
    b = basel_columns.difference(zurich_columns)
    c = zurich_columns.difference(basel_columns)
    print(f'{len(a)} common columns:')
    print(a)
    print(f'{len(b)} columns only in the basel data:')
    print(b)
    print(f'{len(c)} columns only in the zurich data:')
    print(c)


    def nans_color(nans):
        if nans > 100:
            style = Fore.RED
        elif nans > 10:
            style = Fore.YELLOW
        elif nans > 0:
            style = Fore.LIGHTYELLOW_EX
        else:
            style = Fore.RESET
        return style


    for x in a:
        basel_nans = basel_patient_data[x].isnull().sum(axis=0)
        zurich_nans = zurich_patient_data[x].isnull().sum(axis=0)

        basel_style = nans_color(basel_nans)
        zurich_style = nans_color(zurich_nans)

        print(f'{x:35}{basel_style}{basel_nans:3}/{basel_patient_data.shape[0]}{Fore.RESET} | '
              f'{zurich_style}{zurich_nans:3}/{zurich_patient_data.shape[0]}')

    for x in b:
        basel_nans = basel_patient_data[x].isnull().sum(axis=0)
        basel_style = nans_color(basel_nans)

        print(f'{x:35}{basel_style}{basel_nans:3}/{basel_patient_data.shape[0]}{Fore.RESET} | '
              f'---/---')

    for x in c:
        zurich_nans = zurich_patient_data[x].isnull().sum(axis=0)
        zurich_style = nans_color(zurich_nans)

        print(f'{x:35}---/--- | {zurich_style}{zurich_nans:3}/{zurich_patient_data.shape[0]}')

    staining_data = pd.read_csv(staining_data_path)
    whole_image_data = pd.read_csv(whole_image_data_path)


    def graphical_nan_inspection(df, title, csv_path):
        nan_matrix = np.zeros(df.shape)
        for i in range(df.shape[1]):
            nan_matrix[:, i] = df.iloc[:, i].isnull()
        plt.figure()
        cmap = plt.get_cmap('plasma', 2)
        plt.matshow(nan_matrix, cmap=cmap)
        plt.title(title)
        cbar = plt.colorbar(ticks=[0, 1], orientation='horizontal', shrink=0.5)
        cbar.set_ticks([0.25, 0.75])
        cbar.set_ticklabels(['not null', 'null'])
        output_folder = 'generated_data'
        os.makedirs(output_folder, exist_ok=True)
        output_image_path = os.path.join(output_folder, os.path.basename(csv_path.replace('.csv', '.png')))
        plt.savefig(output_image_path)
        # plt.show()


    graphical_nan_inspection(basel_patient_data, 'basel patient data', basel_patient_data_path)
    graphical_nan_inspection(zurich_patient_data, 'zurich patient data', zurich_patient_data_path)
    graphical_nan_inspection(staining_data, 'staining data', staining_data_path)
    graphical_nan_inspection(whole_image_data, 'whole image data', whole_image_data_path)


    # input('this is going to require a lot of ram, press enter to continue...')
    # single_cell_data = pd.read_csv(single_cell_data_path)

    def describe_dataframe(df: pd.DataFrame, columns, file=None):
        if file is None:
            kwargs = {}
        else:
            kwargs = {'file': open(file, 'w')}
        for x in columns:
            print('-' * 100, **kwargs)
            print(x, **kwargs)
            print(df[x].describe(), **kwargs)
            print(df[x].value_counts().sort_index().describe(), **kwargs)
            print(df[x].value_counts().sort_index(), **kwargs)
        if not file is None:
            kwargs['file'].close()


    df = basel_patient_data
    # df = zurich_patient_data
    columns = df.columns
    # columns = c
    describe_dataframe(df, columns)
    describe_dataframe(staining_data, staining_data.columns)
    # describe_dataframe(staining_data, staining_data.columns, file='generated_data/test')
    # describe_dataframe(whole_image_data, whole_image_data.columns)

    # print('place0')
    # single_cell_data = pd.read_csv(single_cell_data_path)
    # print('place1')
    # describe_dataframe(single_cell_data, single_cell_data.columns, file='generated_data/single_cell_data_summary')
    # print('place2')
    # graphical_nan_inspection(single_cell_data, 'single cell data', single_cell_data_path)
    # print('place_last')

    single_cell_reduced = pd.read_csv(single_cell_data_path, nrows=2)
    columns = single_cell_reduced.columns.values
    columns_without_channels = set(map(lambda x: re.sub(r'(.*?)_c[0-9]{1,2}', r'\1_cXX', x), columns))
    print(sorted(columns_without_channels))