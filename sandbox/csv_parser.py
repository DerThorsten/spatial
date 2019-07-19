import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from colorama import init, Fore

init(autoreset=True)

luca = False
if os.path.isdir('/Users/macbook'):
    luca = True
if not luca:
    root_folder = "/media/thorsten/Data/embl/"
else:
    root_folder = '/Users/macbook/Downloads/data/'

csv_folder = os.path.join(root_folder, 'CSVs')

basel_patient_data_path = os.path.join(csv_folder, 'Basel_PatientMetadata.csv')
zurich_patient_data_path = os.path.join(csv_folder, 'Zuri_PatientMetadata.csv')
single_cell_data_path = os.path.join(csv_folder, 'Basel_Zuri_SingleCell.csv')
staining_data_path = os.path.join(csv_folder, 'Basel_Zuri_StainingPanel.csv')
whole_image_data_path = os.path.join(csv_folder, 'Basel_Zuri_WholeImage.csv')

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

def graphical_nan_inspection(df, title):
    nan_matrix = np.zeros(df.shape)
    for i in range(df.shape[1]):
        nan_matrix[:, i] = df.iloc[:, i].isnull()
    plt.figure()
    # plt.axis('equal')
    # grid_kws = {'height_ratios': (0.9, 0.05), 'hspace': 0.3}
    # f, (ax, cbar_ax) = plt.subplots(2, gridspec_kw=grid_kws)
    # ax.axis('equal')
    # ax = sns.heatmap(nan_matrix, ax=ax, cbar_ax=cbar_ax, cbar_kws={'orientation': 'horizontal'})
    cmap = plt.get_cmap('plasma', 2)
    mat = plt.matshow(nan_matrix, cmap=cmap)
    plt.title(title)
    cbar = plt.colorbar(ticks=[0, 1], orientation='horizontal', shrink=0.5)
    cbar.set_ticks([0.25, 0.75])
    cbar.set_ticklabels(['not null', 'null'])
    plt.show()

graphical_nan_inspection(basel_patient_data, 'basel patient data')
graphical_nan_inspection(zurich_patient_data, 'zurich patient data')
graphical_nan_inspection(staining_data, 'staining data')
graphical_nan_inspection(whole_image_data, 'whole image data')
input('this is going to require a lot of ram, press enter to continue...')

single_cell_data = pd.read_csv(single_cell_data_path)
