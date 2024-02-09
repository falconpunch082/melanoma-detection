"""
Trained on the data set of skin images,
which includes around 5000 skin cancer photos and 5000 healthy skin photos
"""

import numpy as np
from flask import Flask, request,render_template
import pickle

# Create app
app=Flask(__name__)

#Load model