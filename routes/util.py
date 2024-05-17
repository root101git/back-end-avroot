import numpy as np
from fastapi import APIRouter,UploadFile
import tensorflow as tf
import pandas as pd
import shutil
import numpy as np
import os
import cv2
import pickle
from fastapi.responses import JSONResponse

router = APIRouter()

def extract_features(image_path):
    # Read the image
    image = cv2.imread(image_path)
    
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Extract Haralick texture features
    haralick = cv2.HuMoments(cv2.moments(gray)).flatten()
    
    # Extract Hu-moments
    moments = cv2.HuMoments(cv2.moments(gray)).flatten()
    
    # Convert the image to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Calculate the HSV histogram
    hist_hue = cv2.calcHist([hsv], [0], None, [256], [0, 256]).flatten()
    hist_saturation = cv2.calcHist([hsv], [1], None, [256], [0, 256]).flatten()
    hist_value = cv2.calcHist([hsv], [2], None, [256], [0, 256]).flatten()
    
    # Concatenate all features into a single array
    features = np.hstack([haralick, moments, hist_hue, hist_saturation, hist_value])
    
    return features
@router.post("/predict")
async def PredictAns(photo:UploadFile):
    try:
        current_dir = os.path.dirname(os.path.realpath(__file__))
        # save_path = os.path.join(current_dir,'/uploads')
        file_path = os.path.join(current_dir, photo.filename)
        with open(file_path, "wb") as i:
            shutil.copyfileobj(photo.file, i)
        print(file_path)
        model_path = os.path.join(current_dir, 'random_forest_model.pkl')


        with open(model_path, 'rb') as f:
            loaded_model = pickle.load(f)
        print("yaha par hain")
        
        features = extract_features(file_path)
    
    
        prediction =  loaded_model.predict([features])  # Note: The predict method expects a 2D array
        

        # img = image.load_img(file_path,target_size=(299,299))   
        # x=  image.img_to_array(img)   
        # x=x/255
        # x=np.expand_dims(x,axis=0)
        # img_data=  preprocess_input(x)
        # result = model.predict(img_data)
        # a=np.argmax(result , axis=1)[0]
        # a = int(a)
        print("this",prediction[0])
        df = pd.read_csv(os.path.join(current_dir, 'lables.csv'))
        ans = df[df['index'] == prediction[0]].values[0][1]
        os.remove(file_path)
        return JSONResponse(content={"plantName":ans})
    except Exception as e:
        error_message = str(e)  # Get the error message as a string
        return JSONResponse(content={"error": error_message})
    
