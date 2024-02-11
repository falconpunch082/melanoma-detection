# To run this script, enter the following command to Git Bash
# python input_preprocesssing.py (filepath/name of image)

# Importing relevant packages
import sys
import pandas as pd
import numpy as np
from PIL import Image
import cv2
import skimage
from skimage import io, color, exposure
from skimage.filters import threshold_otsu

# Input line
raw = Image.open(sys.argv[1])

'''
Section 1: Translating image into array
'''

# Resize the image to a consistent size of 300x300
img = raw.resize((300, 300))

# Convert the image to a NumPy array
img_array = np.array(img)

# Normalize pixel values
img_array = cv2.normalize(img_array, None, 255, 0, cv2.NORM_MINMAX, cv2.CV_8U)

'''
Section 2: Creating the mask to remove unnecessary features like healthy skin and hair.
Hair is first removed with the DullRazor algorithm, resulting in an image which is then used
to create a mask highlighting the skinmark.
'''

# Converting RGB picture to greyscale for hair removal DullRazor algorithm
img_gc = color.rgb2gray(img_array)

# DullRazor algorithm starts here
#Black hat filter
kernel = cv2.getStructuringElement(1,(9,9)) 
blackhat = cv2.morphologyEx(img_gc, cv2.MORPH_BLACKHAT, kernel)

#Gaussian filter
bhg= cv2.GaussianBlur(blackhat,(3,3),cv2.BORDER_DEFAULT)

#Masking hair
ret, mask = cv2.threshold(bhg,0.03,255,cv2.THRESH_BINARY)

# Normalise mask
mask = cv2.normalize(mask, None, 255, 0, cv2.NORM_MINMAX, cv2.CV_8U)

#Replace pixels of the mask
dst = cv2.inpaint(img_array, mask, 6, cv2.INPAINT_TELEA)
# DullRazor algorithm ends here

# Adjusting exposure
img_ex1 = exposure.adjust_log(dst)

p2, p98 = np.percentile(img_ex1, (2, 98))
img_ex2 = exposure.rescale_intensity(img_ex1, in_range=(p2, p98))

# Converting cleaned photo into greyscale for thresholding/segmentation
img_gs2 = color.rgb2gray(img_ex2)

# Global thresholding with Otsu
thresh = threshold_otsu(img_gs2)

# Creating threshold image
img_t = img_gs2 <= thresh

# Creating mask using threshold image
# Value 0 as black and white photo used
mask = np.where(img_t >= 0, img_t, 0)

'''
Section 3: Creating the final processed photo by only including parts of 
img_array that is highlighted by the mask.
'''

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