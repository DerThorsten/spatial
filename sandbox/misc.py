import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import pyqtgraph.console

from layer_viewer import dcolors
from layer_viewer import LayerViewerWidget
from layer_viewer.layers import *

import vigra
import numpy
import skimage.data

import skimage
import skimage.io
import numpy
import pylab
import sklearn
import sklearn.decomposition







app = pg.mkQApp()

image = skimage.data.astronaut().swapaxes(0,1)
print(image.shape)



f = "/media/thorsten/Data/embl/hartlandj/Data/Basel_Zuri/ome/BaselTMA_SP41_15.475kx12.665ky_10000x8500_5_20170905_90_000029_X11Y5_242_a0.ome.tiff"
mask = "/media/thorsten/Data/embl/masks/BaselTMA_SP41_15.475kx12.665ky_10000x8500_5_20170905_90_000029_X11Y5_242_a0_full_mask.tiff"


img = skimage.io.imread(f)
mask = skimage.io.imread(mask)
print(mask.min(), mask.max())

flat_mask = mask.ravel()
where_non_zero  = numpy.where(flat_mask != 0)[0]
print(where_non_zero)


print(mask.shape)
img = img.squeeze()
shape = img.shape[1:3]
n_channels = img.shape[0]
print(f"shape {img.shape}")


n_components = 3
img =  numpy.moveaxis(img,0,2)
X = img.reshape([-1, n_channels])
maskedX = X[flat_mask,:]
dim_red_alg = sklearn.decomposition.PCA(n_components=n_components)
dim_red_alg.fit(numpy.sqrt(maskedX))
Y = dim_red_alg.transform(X)
reshape = tuple(shape) + (n_components,)
Y = Y.reshape(reshape)

print(f"Y {img.shape}")


for c in range(3):
    Yc = Y[...,c]
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



