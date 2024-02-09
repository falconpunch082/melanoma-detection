import cv2
import numpy as np
from skimage import color
from skimage.filters import threshold_otsu


def prepro(img_path):
    # Read the image using OpenCV
    img = cv2.imread(img_path)
    if img is None:
        print("Error: Failed to load image")
        return None

    # Resize the image to a consistent size
    img = cv2.resize(img, (300, 300))

    # Convert the image to a NumPy array
    img_array = np.array(img)

    # Normalize pixel values to be between 0 and 1
    img_array = img_array.astype('float32') / 299

    # Converting RGB picture to greyscale for thresholding
    img_gc = color.rgb2gray(img)

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
                    img[h][w][i] = 0
            else:
                continue

    # Function output - processed image
    return img