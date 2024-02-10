"""
Trained on the data set of skin images,
which includes around 5000 skin cancer photos and 5000 healthy skin photos
"""

import numpy as np
from flask import Flask, request,render_template,session
import os
import pickle
from helper import *

# Create app
app=Flask(__name__)
app.secret_key = 'proj4ct4Gr0up2'
# Load model
# model=pickle.load(open('models/model.pkl','rb'))

##########################
###         APP        ###
##########################

# Handle when upload photo
UPLOAD_FOLDER = 'uploads'
STATIC_FOLDER = 'static'
# Ensure the uploads directory exists
os.makedirs(STATIC_FOLDER, exist_ok=True)

#Photo link
uploads_dir = os.path.join(STATIC_FOLDER, UPLOAD_FOLDER)
os.makedirs(uploads_dir, exist_ok=True)
#Model link
model_dir=os.path.join(STATIC_FOLDER,'models')

# Home page
@app.route('/',methods=['POST','GET'])
def home_page():
    src_photo = ' '
    # Check if there is any memory in Flask
    if not session.get('_cleared_once'):
        session.clear()
        session['_cleared_once'] = True
        file_name='No file selected'
        session['file_name']='No file selected'
        prediction_result=''
        display_results='none'
    else:
        file_name = session.get('file_name', 'No file selected')
        prediction_result = session.get('prediction', 'No prediction available')
        display_results = session.get('display_results', 'none')

        # Get the scr file
        if session['file_name'] != 'No file selected':
            previous_filename = session['file_name']
            previous_filepath = os.path.join(uploads_dir, previous_filename)
            if os.path.exists(previous_filepath):
                src_photo = previous_filename

    # Check if the user upload a file
    if 'file' not in request.files:
        if session['file_name']!='No file selected':
            return render_template('skin-cancer-detection.html',src_photo=src_photo,
                                   file_name=file_name,prediction=prediction_result, display_results=display_results)
        else:
            file_name = session.get('file_name', 'No prediction available')
            return render_template('skin-cancer-detection.html',src_photo=src_photo,
                                   file_name=file_name,prediction=prediction_result,display_results='none')

    file = request.files['file']
    #Check if the file is empty
    if file.filename == '':
        file_name = session.get('file_name', 'No prediction available')
        return render_template('skin-cancer-detection.html',src_photo=src_photo,
                               file_name=file_name,prediction=prediction_result,display_results='none')

    # Remove previous files if it exists
    if os.path.exists(uploads_dir):
        # Get a list of all files in the directory
        files = os.listdir(uploads_dir)
        for file_name in files:
            # Construct the full file path
            file_path = os.path.join(uploads_dir, file_name)
            # Check if it's a file (not a directory) and delete it
            if os.path.isfile(file_path):
                os.remove(file_path)

    # Save the file to a location on the server
    file_name=file.filename
    session['file_name']=file_name
    file.save(os.path.join(uploads_dir, file.filename))

    return render_template('skin-cancer-detection.html',src_photo=src_photo,
                           file_name=file_name,prediction=prediction_result,display_results=display_results)

# Prediction page
@app.route('/predict',methods=['POST','GET'])
def predict():
    raw_data = request.data #For hadnling post request otherwise it will not work
    # Get the link file
    if os.path.exists(uploads_dir):
        # Get a list of all files in the directory
        files = os.listdir(uploads_dir)
        if len(files)>0:
            img_path = os.path.join(uploads_dir, files[0])

    # Check if there is a model exists
    if os.path.exists(model_dir):
        # Get a list of all files in the directory
        files = os.listdir(model_dir)
        if len(files)>0:
            model_path = os.path.join(model_dir, files[1]) #files[0] is model 1 and files[1] is model 2
            with open(model_path,'rb') as m:
                model=pickle.load(m)
            processed_img=prepro(img_path)
            if processed_img is not None:
                # Reshape the image for prediction
                processed_image = np.expand_dims(processed_img, axis=0)
                # Make predictions using the loaded model
                predictions = model.predict(processed_image)
                print(predictions)
                prediction_value = round(predictions[0][0])

    if session['file_name']=='No file selected':
        prediction_result = "Please upload a photo of your skin first!!!"
    else:
        if prediction_value==0:
            prediction_result = 'Analysis Result: <span style="color: green;">No sign of cancer was detected.</span>'
        else:
            prediction_result = 'Analysis Result: <span style="color: red;">Suspicious. Consult a dermatologist.</span>'

    session['prediction'] = prediction_result
    session['display_results']='show'
    return render_template('skin-cancer-detection.html', src_photo='',prediction=prediction_result, display_results='show')

#Clear Flask memory
@app.route('/reset',methods=['POST','GET'])
def reset():
    raw_data = request.data
    session.clear()
    return 'Data reset'

if __name__=="__main__":
    app.run(debug=False,host='0.0.0.0')
