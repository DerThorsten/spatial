import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import pyqtgraph.console

from layer_viewer import dcolors
from layer_viewer import LayerViewerWidget
from layer_viewer.layers import *

from sandbox.folders import get_masks_folder, get_ome_folder

import vigra
import os

import skimage
import skimage.io
import skimage.data
import numpy
import pylab
import sklearn
import sklearn.decomposition
import matplotlib.pyplot as plt


mask_folder = get_masks_folder()
img_folder = get_ome_folder()
dataset = []

img_count = len([img for img in os.listdir(img_folder) if img.endswith('.tiff')])
masks_count = len([img for img in os.listdir(mask_folder) if img.endswith('.tiff')])
if img_count != masks_count:
    raise ValueError(f'img_count = {img_count}, masks_count = {masks_count}')

# make pairs of (img, mask) for all images in the dataset
for filename in os.listdir(img_folder):
    img_path = filename
    mask_path = ''
    if filename.endswith('ome.tiff'): #or filename.endswith('.py'):
        mask_path = img_path.replace('.ome.tiff', '_full_mask.tiff')
    elif filename.endswith('full.tiff'):
        mask_path = img_path.replace('full.tiff', 'full_maks.tiff')
    img_path = os.path.join(img_folder, img_path)
    mask_path = os.path.join(mask_folder, mask_path)
    if os.path.isfile(img_path) and os.path.isfile(mask_path):
        dataset.append((img_path, mask_path))

if len(dataset) != img_count:
    raise ValueError(f'len(dataset) = {len(dataset)}, img_count = {img_count}')
print(len(dataset))

app = pg.mkQApp()

image = skimage.data.astronaut().swapaxes(0, 1)
print(image.shape)

item = 222

f = dataset[item][0]
mask = dataset[item][1]

img = skimage.io.imread(f)
mask = skimage.io.imread(mask)
plt.figure()
plt.hist(mask.ravel(), bins=50)
plt.show()

print(mask.min(), mask.max())

flat_mask = mask.ravel()
where_non_zero = numpy.where(flat_mask != 0)[0]
print(where_non_zero)

print(mask.shape)
img = img.squeeze()
shape = img.shape[1:3]
n_channels = img.shape[0]
print(f"shape {img.shape}")

n_components = 3
img = numpy.moveaxis(img, 0, 2)
img = vigra.taggedView(img, 'xyc')
img = vigra.filters.gaussianSmoothing(img, 0.5)
img = numpy.require(img, requirements=['C'])
X = img.reshape([-1, n_channels])
maskedX = X[flat_mask, :]
dim_red_alg = sklearn.decomposition.PCA(n_components=n_components)
dim_red_alg.fit(numpy.sqrt(X))
Y = dim_red_alg.transform(X)
reshape = tuple(shape) + (n_components,)
Y = Y.reshape(reshape)

print(f"Y {img.shape}")

for c in range(3):
    Yc = Y[..., c]
    Yc -= Yc.min()
    Yc /= Yc.max()

viewer = LayerViewerWidget()
viewer.setWindowTitle('LayerViewer')
viewer.show()
# layer = RGBImageLayer(name='img', data=image[...])
# viewer.addLayer(layer=layer)


layer = MultiChannelImageLayer(name='img', data=img[...])
viewer.addLayer(layer=layer)

layer = MultiChannelImageLayer(name='PCA-IMG', data=Y[...])
viewer.addLayer(layer=layer)

layer = ObjectLayer(name='mask', data=mask)
viewer.addLayer(layer=layer)

# labels = numpy.zeros(image.shape[0:2], dtype='uint8')
# label_layer = LabelLayer(name='labels', data=None)
# viewer.addLayer(layer=label_layer)
# viewer.setData('labels',image=labels)


# layer.setOpacity(0.5)


# # viewer.setLayerVisibility('img', False)
# viewer.setLayerOpacity('img', 0.4)
# viewer.setLayerOpacity('img', 0.4)
## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
