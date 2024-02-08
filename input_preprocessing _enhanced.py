# To run this script, enter the following command to Git Bash
# python input_preprocesssing.py (filepath/name of image)

# Importing relevant packages
from tensorflow.image import resize
import numpy as np
import sys
import cv2
import imghdr
from skimage import io, color
from skimage.filters import threshold_otsu

# Input line
input = Image.open(sys.argv[1])

# Reading image with cv2 library and readjusting colour
img = cv2.imread(input)
img_corrected= cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Resizing image provided to 300x300
resize = resize(img_corrected, (300,300))

# Convert the image to a NumPy array
img_array = np.array(resize)

# Normalize pixel values to be between 0 and 1
img_array = img_corrected.astype('float32') / 299

# Converting RGB picture to greyscale for thresholding
img_gc = color.rgb2gray(img_array)

# Global thresholding with Otsu
thresh = threshold_otsu(img_gc)
img_t = img_gc <= thresh

# Creating mask using threshold image
# Value 0 as black and white photo used
mask = np.where(img_t >= 0, img_t, 0)

# Overlaying mask on original image
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
output = np.expand_dims(resize/255, 0)

print(output)