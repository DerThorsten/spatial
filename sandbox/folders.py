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
#
#
# def match_filenames_with_full_paths(full_paths: List[str], filenames: Tuple[str]) -> Tuple[str]:
#     """
#     Matches a tuple of filenames onto a list of path strings; returns the matched paths in the same order as the input tuple.
#     In case of ambiguities raises an exception.
#     The complexity, which can be improved, is n * m, where n and m are the lengths of the two input parameters.
#
#     :param full_paths: list of paths
#     :param filenames: tuple of filenames
#     :return: tuple of paths which match the input tuple, in the same order as the input tuple
#     """
#     if len(filenames) == 0 or len(filenames) > len(full_paths):
#         raise ValueError(f'len(filenames) = {len(filenames)}, len(full_paths) = {len(full_paths)}')
#
#     def find_path(filename: str) -> str:
#         found = 0
#         found_path = ''
#         for path in full_paths:
#             if path.endswith('/' + filename):
#                 found += 1
#                 found_path = path
#         if found == 0 or found > 1:
#             raise ValueError(f'filename = {filename}, found = {found}')
#         else:
#             return found_path
#
#     matched = [find_path(filename) for filename in filenames]
#     return tuple(matched)
