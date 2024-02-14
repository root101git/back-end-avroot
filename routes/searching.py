from fastapi import APIRouter
import firebase_admin
from firebase_admin import firestore
from db import connectDb
connectDb()
router = APIRouter()
db = firestore.client()


@router.get('/search/{input}')
async def index(input:str=""):
    doc_ref = db.collection("data_plants")
    data = doc_ref.where("name", ">=", input).where("name", "<=",input+ "\uf8ff").get()
    result =  [elem.to_dict() for elem in data]
    return result