import os
from typing import List, Tuple


def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func

    return decorate


@static_vars(data_folder='')
def get_data_folder() -> str:
    user_path = os.path.expanduser('~')
    paths = {'luca': os.path.join(user_path, 'Downloads/JacksonFischer_Collaborators'),
             'thorsten': '/media/throsten/Data/embl/',
             'odcf': '/icgc/dkfzlsdf/analysis/B260/projects/spatial_zurich/data'}

    if get_data_folder.data_folder != '':
        return get_data_folder.data_folder
    else:
        found = 0
        current_machine = ''
        for k, v in paths.items():
            if os.path.isdir(v):
                current_machine = k
                get_data_folder.data_folder = v
                found += 1

        if found == 0:
            raise Exception(
                'Unable to find the data, please download the data and/or update the values of the "paths" dictionary')

        if found > 1:
            raise Exception('Multiple data folder found, aborting')

        print(f'current machine = {current_machine}')
        return get_data_folder.data_folder


def get_csv_folder() -> str:
    return os.path.join(get_data_folder(), 'csv')


def get_masks_folder() -> str:
    return os.path.join(get_data_folder(), 'Basel_Zuri_masks')


def get_ome_folder() -> str:
    return os.path.join(get_data_folder(), 'ome')


basel_patient_data_path = os.path.join(get_csv_folder(), 'Basel_PatientMetadata.csv')
zurich_patient_data_path = os.path.join(get_csv_folder(), 'Zuri_PatientMetadata.csv')
single_cell_data_path = os.path.join(get_csv_folder(), 'Basel_Zuri_SingleCell.csv')
staining_data_path = os.path.join(get_csv_folder(), 'Basel_Zuri_StainingPanel.csv')
whole_image_data_path = os.path.join(get_csv_folder(), 'Basel_Zuri_WholeImage.csv')


def get_masks_files() -> List[str]:
    to_return = list()
    folder = get_masks_folder()
    for file in os.listdir(folder):
        if file.endswith('.tiff'):
            to_return.append(os.path.join(folder, file))
    return to_return


def get_ome_files() -> List[str]:
    to_return = list()
    folder = get_ome_folder()
    for file in os.listdir(folder):
        if file.endswith('.tiff'):
            to_return.append(os.path.join(folder, file))
    return to_return


def get_processed_data_folder() -> str:
    root = get_data_folder()
    path = os.path.join(root, 'stegle_processed')
    os.makedirs(path, exist_ok=True)
    return path


def get_region_features_folder() -> str:
    path = os.path.join(get_processed_data_folder(), 'region_features')
    os.makedirs(path, exist_ok=True)
    return path


def get_mask_path_associated_to_ome_path(ome_path: str) -> str:
    ome_filename = os.path.basename(ome_path)
    if ome_filename.endswith('ome.tiff'):
        mask_filename = ome_filename.replace('.ome.tiff', '_full_mask.tiff')
    elif ome_filename.endswith('full.tiff'):
        mask_filename = ome_filename.replace('full.tiff', 'full_maks.tiff')
    else:
        raise ValueError(f'ome_filename = {ome_filename}')
    mask_path = os.path.join(get_masks_folder(), mask_filename)
    return mask_path


def get_region_features_path_associated_to_ome_path(ome_path: str) -> str:
    ome_filename = os.path.basename(ome_path)
    region_features_filename = ome_filename.replace('.tiff', '_region_features.pickle')
    path = os.path.join(get_region_features_folder(), region_features_filename)
    return path
