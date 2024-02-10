# To run this script, enter the following command to Git Bash
# python input_preprocesssing.py (filepath/name of image)

# Importing relevant packages
import sys
import tensorflow as tf
import pandas as pd
import numpy as np
from PIL import Image
import skimage
from skimage import io, color, exposure
from skimage.filters import threshold_otsu

# Input line
raw = Image.open(sys.argv[1])

# Resize the image to a consistent size of 300x300
img = raw.resize((300, 300))

# Convert the image to a NumPy array
img_array = np.array(img)

# Saving original array for comparison purposes
img_ori = img_array

# Normalize pixel values to be between 0 and 1
img_array = img_array.astype('float32') / 299

# Converting RGB picture to greyscale for thresholding
img_gc = color.rgb2gray(img_array)

# Adjusting exposure
img_ex1 = exposure.adjust_log(img_gc)

p2, p98 = np.percentile(img_ex1, (2, 98))
img_ex2 = exposure.rescale_intensity(img_ex1, in_range=(p2, p98))

# Global thresholding with Otsu
thresh = threshold_otsu(img_ex2)

# Creating threshold image
img_t = img_ex2 <= thresh

# Creating mask using threshold image
# Value 0 as black and white photo used
mask = np.where(img_t >= 0, img_t, 0)

# Overlaying mask on original image
# So that model will receive only skinmark (the less pixels to consider, the faster processing becomes)

# Nested for loop for each 'row' of img
for h in range(mask.shape[0]):
    # For each 'column' of img
    for w in range(mask.shape[1]):
        # If the pixel chosen from the mask is white, add in the pixel from the original image
        # Otherwise, discard/make pixel black
        if mask[h][w] == 0:
            for i in range(3):
                img_array[h][w][i] = 0
        else:
            continue

# Creating tensor to be passed into the model
output = np.expand_dims(img_array/255, 0)

print(output)