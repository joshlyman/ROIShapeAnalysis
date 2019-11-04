import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage as ndi

from skimage import feature
import SimpleITK
import os

filename = '/Users/yanzhexu/Google Drive/Marley Grant Data/CEDM pilot data-selected/benign'

casefile = 'Pt1'
filename2 = os.path.join(filename,casefile)
dicomfile = 'Pt1 - DES - MLO.dcm'

# read image to array
filename3 = os.path.join(filename2, dicomfile)
rawImage = SimpleITK.ReadImage(filename3)
imgArray = SimpleITK.GetArrayFromImage(rawImage)

if len(imgArray.shape) == 3:
    imgArray = imgArray[0, :, :]


# Compute the Canny filter for two values of sigma
edges1 = feature.canny(imgArray)
edges2 = feature.canny(imgArray, sigma=1)

# display results
fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(8, 3), sharex=True, sharey=True)


# ax1.imshow(imgArray, cmap=plt.cm.jet)
# ax1.axis('off')
# ax1.set_title('noisy image', fontsize=20)
#
# ax2.imshow(edges1, cmap=plt.cm.gray)
# ax2.axis('off')
# ax2.set_title('Canny filter, $\sigma=1$', fontsize=20)

ax3.imshow(edges2)
ax3.axis('off')

fig.subplots_adjust(wspace=0.02, hspace=0.02, top=0.9,
                    bottom=0.02, left=0.02, right=0.98)

plt.show()