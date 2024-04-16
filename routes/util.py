import numpy as np
from fastapi import APIRouter,UploadFile
import tensorflow as tf
import pandas as pd
import shutil
import os

from fastapi.responses import JSONResponse
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.inception_v3 import preprocess_input
router = APIRouter()


@router.post("/predict")
async def PredictAns(photo:UploadFile):
    try:
        current_dir = os.path.dirname(os.path.realpath(__file__))
        # save_path = os.path.join(current_dir,'/uploads')
        file_path = os.path.join(current_dir, photo.filename)
        with open(file_path, "wb") as i:
            shutil.copyfileobj(photo.file, i)
        
        model = load_model(os.path.join(current_dir, 'models/inception4.h5'))
      

        img = image.load_img(file_path,target_size=(299,299))   
        x=  image.img_to_array(img)   
        x=x/255
        x=np.expand_dims(x,axis=0)
        img_data=  preprocess_input(x)
        result = model.predict(img_data)
        a=np.argmax(result , axis=1)[0]
        a = int(a)
        df = pd.read_csv(os.path.join(current_dir, 'new.csv'))
        ans = df[df['index'] == a ].values[0][1]
        os.remove(file_path)
        return JSONResponse(content={"plantName":ans})
    except Exception as e:
        return JSONResponse(content={e})
    
