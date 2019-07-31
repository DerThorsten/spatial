import os
import hashlib
import numpy as np
import vigra
import matplotlib
import matplotlib.pyplot as plt
import skimage
import itertools
from sandbox.folders import get_ome_files, get_masks_files, get_ome_folder, get_masks_folder
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
        ome_path = os.path.join(get_ome_folder(), ome_filename)
        if ome_path in remaining_ome_files:
            self.ome_path = ome_path
            remaining_ome_files.remove(ome_path)
        else:
            raise FileNotFoundError(f'file not found: {ome_path}')

        if ome_filename.endswith('ome.tiff'):
            mask_filename = ome_filename.replace('.ome.tiff', '_full_mask.tiff')
        elif ome_filename.endswith('full.tiff'):
            mask_filename = ome_filename.replace('full.tiff', 'full_maks.tiff')
        mask_path = os.path.join(get_masks_folder(), mask_filename)
        if mask_path in remaining_mask_files:
            self.mask_path = mask_path
        else:
            raise FileNotFoundError(f'file not found {mask_filename}')
        self.compute_statistics()

        # hash_md5 = hashlib.md5()
        # with open(self.ome_path, 'rb') as infile:
        #     for chunk in iter(lambda: infile.read(4096), b''):
        #         hash_md5.update(chunk)
        # hex_digest = hash_md5.hexdigest()
        # print(f'hex_digest = {hex_digest}')

    def compute_statistics(self):
        masks = skimage.io.imread(self.mask_path)
        plt.figure()
        cmap = matplotlib.colors.ListedColormap(np.random.rand(masks.max() + 1, 3))
        cmap.colors[0] = (0, 0, 0)
        im = plt.imshow(masks, cmap=cmap)
        # plt.colorbar(im)
        plt.show()
        pass

# class Cell:
#     def __init__(self):



def call_the_initializer(cls):
    cls.initialize()
    return cls


@call_the_initializer
class JacksonFischerDataset:
    @classmethod
    def initialize(cls):
        basel_patient_ids = set(basel_patient_data.PID)
        zurich_patient_ids = set(zurich_patient_data.PID)
        cls.patients = []
        for pid in basel_patient_ids:
            patient = Patient(Patient.Source.basel, pid)
            cls.patients.append(patient)
        for pid in zurich_patient_ids:
            patient = Patient(Patient.Source.zurich, pid)
            cls.patients.append(patient)
#
#
# if __name__ == '__main__':
#     patient = Patient(Patient.Source.basel, pid=12)
