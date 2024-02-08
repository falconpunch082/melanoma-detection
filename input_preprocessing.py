# To run this script, enter the following command to Git Bash
# python input_preprocesssing.py (filepath/name of image)

# Importing relevant packages
from tensorflow.image import resize
import numpy as np
import sys
import cv2
import imghdr

# Input line
input = Image.open(sys.argv[1])

# Reading image with cv2 library and readjusting colour
img = cv2.imread(input)
img_corrected= cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Resizing image provided to 300x300
resize = resize(img_corrected, (300,300))

# Creating tensor to be passed into the model
output = np.expand_dims(resize/255, 0)

print(output)