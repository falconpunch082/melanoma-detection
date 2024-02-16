"""
Trained on the data set of skin images,
which includes around 5000 skin cancer photos and 5000 healthy skin photos
"""

from flask import Flask, request,render_template,session
import os
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
        if file_name != 'No file selected':
            previous_filename = session['file_name']
            previous_filepath = os.path.join(uploads_dir, previous_filename)
            if os.path.exists(previous_filepath):
                src_photo = previous_filename
    # Clear memory to make the web look nice
    if session.get('prediction'):
        session.clear()

    # Check if the user upload a file
    if 'file' not in request.files:
        if file_name!='No file selected':
            return render_template('skin-cancer-detection.html',src_photo=src_photo,
                                   file_name=file_name,prediction=prediction_result, display_results=display_results)
        else:
            file_name = session.get('file_name', 'No file selected')
            return render_template('skin-cancer-detection.html',src_photo=src_photo,
                                   file_name=file_name,prediction=prediction_result,display_results=display_results)

    file = request.files['file']
    #Check if the file is empty
    if file.filename == '':
        file_name = session.get('file_name', 'No file selected')
        return render_template('skin-cancer-detection.html',src_photo=src_photo,
                               file_name=file_name,prediction=prediction_result,display_results=display_results)

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
@app.route('/predict/<file_name>',methods=['POST','GET'])
def predict(file_name):
    raw_data = request.data #For hadnling post request otherwise it will not work
    colors=[
        'rgb(255,4,2)', #red
        'rgb(255,69,32)',
        'rgb(255,109,51)',
        'rgb(255,159,75)',
        'rgb(255,197,93)', #orange
        'rgb(175,204,95)',
        'rgb(124,196,91)',
        'rgb(73,188,86)',
        'rgb(22,179,82)' #green
    ]
    text_color=colors[8]
    # Get the link file
    if os.path.exists(uploads_dir):
        # Get a list of all files in the directory
        files = os.listdir(uploads_dir)
        if len(files) > 0:
            img_path = ""  # Initialize img_path outside the loop
            for file in files:
                print(file)
                print(file_name)
                if file_name in file:  # Check if file_name is present in the file name
                    img_path = os.path.join(uploads_dir, file)
                    break  # Exit the loop once the file is found
    try:
        # Check if there is a model exists
        if os.path.exists(model_dir):
            # Get a list of all files in the directory
            files = os.listdir(model_dir)
            if len(files)>0:
                model_path = os.path.join(model_dir, files[0]) #files[0] is model 1 and files[1] is model 2
                    #Using tensorflow to load the model
                model = load_model(model_path)
                processed_img=prepro(img_path)
                if processed_img is not None:
                    # Reshape the image for prediction
                    processed_image = np.expand_dims(processed_img/255, 0)
                    # Make predictions using the loaded model
                    predictions = model.predict(processed_image)
                    prediction_value = round(100-predictions[0][0]*100)
        if session['file_name']=='No file selected':
            prediction_result = "Please upload a photo of your skin first!!!"
        else:
            for i, pred in enumerate(range(90, 0, -10)):
                if prediction_value >= pred:
                    text_color=colors[i]
                    break
            if prediction_value<60:
                prediction_value=' There is a low'
            else:
                prediction_value=str(prediction_value)+'%'
            prediction_result = f'Analysis Result: <span style="color: {text_color};">{prediction_value} chance that the given photo has cancer.</span>'
    except Exception as e:
        prediction_result = 'Ooops, something went wrong. Please re-upload the file and try again.'
        session['_cleared_once'] = True
        print(e)

    session['prediction'] = prediction_result
    session['display_results'] = 'show'

    return render_template('skin-cancer-detection.html', src_photo='',prediction=prediction_result, display_results='show')

#Clear Flask memory
@app.route('/reset',methods=['POST','GET'])
def reset():
    raw_data = request.data
    session.clear()
    return 'Data reset'

if __name__=="__main__":
    app.run(debug=True)