import os
import pickle
import numpy as np
import vigra
import matplotlib
import matplotlib.pyplot as plt
import skimage
import progressbar
import pandas as pd
from typing import Set, Dict

from sandbox.folders import get_ome_files, get_masks_files, get_ome_folder, \
    get_mask_path_associated_to_ome_path, get_region_features_path_associated_to_ome_path
from sandbox.data_connector import basel_patient_data, zurich_patient_data

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
        self.ome_path: str
        self.mask_path: str
        self.masks: np.ndarray
        self.region_features: Dict[str, np.array]

        self.ome_path = os.path.join(get_ome_folder(), ome_filename)
        if self.ome_path in remaining_ome_files:
            remaining_ome_files.remove(self.ome_path)
        else:
            raise FileNotFoundError(f'file not found: {self.ome_path}')

        self.mask_path = get_mask_path_associated_to_ome_path(self.ome_path)
        if self.mask_path in remaining_mask_files:
            remaining_mask_files.remove(self.mask_path)
        else:
            raise FileNotFoundError(f'file not found {self.mask_path}')

        region_features_path = get_region_features_path_associated_to_ome_path(self.ome_path)
        if os.path.isfile(region_features_path):
            self.region_features = pickle.load(open(region_features_path, 'rb'))
        else:
            self.compute_and_save_region_features(region_features_path)

    def get_ome(self) -> np.ndarray:
        ome = skimage.io.imread(self.ome_path)
        ome = np.moveaxis(ome, 0, 2)
        ome = np.require(ome, requirements=['C'])
        return ome

    def get_masks(self) -> np.ndarray:
        masks = skimage.io.imread(self.mask_path)
        masks = masks.astype('uint32')
        masks = np.require(masks, requirements=['C'])
        return masks

    def compute_and_save_region_features(self, region_features_path: str):
        ome = self.get_ome()
        masks = self.get_masks()

        # plt.figure()
        # cmap = matplotlib.colors.ListedColormap(np.random.rand(masks.max() + 1, 3))
        # cmap.colors[0] = (0, 0, 0)
        # im = plt.imshow(masks, cmap=cmap)
        # # plt.colorbar(im)
        # plt.show()

        # supported_features = vigra.analysis.extractRegionFeatures(ome, labels=masks, features=None,
        #                                                           ignoreLabel=0).supportedFeatures()
        # print(f'supported features: {supported_features}')
        features = vigra.analysis.extractRegionFeatures(ome, labels=masks, ignoreLabel=0,
                                                        features=['Count', 'Maximum', 'Mean', 'Sum',
                                                                  'Variance', 'RegionCenter'])

        self.region_features = {'count': features['Count'],
                                'max': features['Maximum'],
                                'mean': features['Mean'],
                                'sum': features['Sum'],
                                'variance': features['Variance'],
                                'center': features['RegionCenter']}
        pickle.dump(self.region_features, open(region_features_path, 'wb'))

    @staticmethod
    def get_mask_for_specific_cell(masks: np.ndarray, region_number: int):
        return (masks == region_number).astype(int)


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
