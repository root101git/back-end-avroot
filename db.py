
import firebase_admin
from firebase_admin import credentials

def connectDb():
    try:
        cred = credentials.Certificate("credentials.json")  
        firebase_admin.initialize_app(cred)
        print("database connected")
    except Exception as e:
        print(e)