import os
import pickle
import numpy as np
import vigra
import matplotlib
import matplotlib.pyplot as plt
import skimage
import progressbar
import pandas as pd

from sandbox.folders import get_ome_files, get_masks_files, get_ome_folder, get_masks_folder, \
    get_mask_path_associated_to_ome_path, get_region_features_path_associated_to_ome_path
from sandbox.data_connector import basel_patient_data, zurich_patient_data, single_cell_data_connection

from enum import Enum

remaining_ome_files = set(get_ome_files())
remaining_mask_files = set(get_masks_files())


class Patient:
    Source = Enum('Source', 'basel zurich')

    def __init__(self, source: Source, pid: int):
        self.plates = []
        self.source = source
        self.pid = pid
        if self.source == Patient.Source.basel:
            self.df = basel_patient_data
        else:
            self.df = zurich_patient_data
        self.initialize_plates()

    def initialize_plates(self):
        plate_rows = self.df[self.df.PID == self.pid]
        for plate_row in plate_rows.itertuples():
            filename = plate_row.FileName_FullStack
            plate = Plate(filename)
            self.plates.append(plate)


class Plate:
    def __init__(self, ome_filename: str):
        self.region_features = None
        self.cell_labels = None
        ome_path = os.path.join(get_ome_folder(), ome_filename)
        if ome_path in remaining_ome_files:
            self.ome_path = ome_path
            remaining_ome_files.remove(ome_path)
        else:
            raise FileNotFoundError(f'file not found: {ome_path}')

        mask_path = get_mask_path_associated_to_ome_path(ome_path)
        if mask_path in remaining_mask_files:
            self.mask_path = mask_path
        else:
            raise FileNotFoundError(f'file not found {mask_path}')

        region_features_path = get_region_features_path_associated_to_ome_path(self.ome_path)
        if os.path.isfile(region_features_path):
            self.region_features = pickle.load(open(region_features_path, 'rb'))
        else:
            self.compute_and_save_region_features(region_features_path)

        # hash_md5 = hashlib.md5()
        # with open(self.ome_path, 'rb') as infile:
        #     for chunk in iter(lambda: infile.read(4096), b''):
        #         hash_md5.update(chunk)
        # hex_digest = hash_md5.hexdigest()
        # print(f'hex_digest = {hex_digest}')

    def compute_and_save_region_features(self, region_features_path: str):
        masks = skimage.io.imread(self.mask_path, )
        masks = masks.astype('uint32')
        # note, self.cell_labels can also be a set of non-consecutive numbers
        self.cell_labels = set(masks.ravel())
        # plt.figure()
        # cmap = matplotlib.colors.ListedColormap(np.random.rand(masks.max() + 1, 3))
        # cmap.colors[0] = (0, 0, 0)
        # im = plt.imshow(masks, cmap=cmap)
        # # plt.colorbar(im)
        # plt.show()

        ome = skimage.io.imread(self.ome_path)
        ome = np.moveaxis(ome, 0, 2)

        masks = np.require(masks, requirements=['C'])
        ome = np.require(ome, requirements=['C'])
        # supported_features = vigra.analysis.extractRegionFeatures(ome, labels=masks, features=None,
        #                                                           ignoreLabel=0).supportedFeatures()
        # print(f'supported features: {supported_features}')
        features = vigra.analysis.extractRegionFeatures(ome, labels=masks, ignoreLabel=0,
                                                        features=['Count', 'Maximum', 'Mean', 'Sum',
                                                                  'Variance', 'RegionCenter'])
        # 'count': features['Count'],
        #                    'max': features['Maximum'],
        #                    'sum': features['Sum'],
        #                    'variance': features['Variance'],
        # df = pd.DataFrame({'center_x': features['RegionCenter'][:, 0],
        #                    'center_y': features['RegionCenter'][:, 1]})
        # return df

        self.region_features = {'count': features['Count'],
                                'max': features['Maximum'],
                                'mean': features['Mean'],
                                'sum': features['Sum'],
                                'variance': features['Variance'],
                                'center': features['RegionCenter']}
        pickle.dump(self.region_features, open(region_features_path, 'wb'))


# class Cell:
#     def __init__(self):


def call_the_initializer(cls):
    cls.initialize()
    return cls


@call_the_initializer
class JacksonFischerDataset:
    @classmethod
    def initialize(cls):
        # pickle_path = 'pickles/JacksonFisherDataset.pickle'
        # if os.path.isfile(pickle_path):
        #     cls.patients = pickle.load(open(pickle_path, 'rb'))
        # else:
        #     os.makedirs('pickles', exist_ok=True)
        basel_patient_ids = set(basel_patient_data.PID)
        zurich_patient_ids = set(zurich_patient_data.PID)
        cls.patients = []
        with progressbar.ProgressBar(max_value=len(basel_patient_ids) + len(zurich_patient_ids)) as bar:
            i = 0
            bar.update(0)
            for pid in basel_patient_ids:
                patient = Patient(Patient.Source.basel, pid)
                cls.patients.append(patient)
                i += 1
                bar.update(i)
            for pid in zurich_patient_ids:
                patient = Patient(Patient.Source.zurich, pid)
                cls.patients.append(patient)
                i += 1
                bar.update(i)
            # pickle.dump(cls.patients, open(pickle_path, 'wb'))

#
# if __name__ == '__main__':
#     patient = Patient(Patient.Source.basel, pid=12)
