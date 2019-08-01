import vigra



def accumulate_region_features(image, masks):
    vimage = vigra.taggedView(image, 'xyc')
    mimage = vigra.taggedView(image, 'xy')
    res = vigra.analysis.extractRegionFeatures(vimage, mimage)