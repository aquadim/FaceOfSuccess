from typing import Annotated
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import Storage.Utils as Storage
import FaceCoding.AcceptFace as AcceptFace
import base64
import tempfile
import Database
import os

def getDb():
    return Database.DB("db.sqlite3")

class Photo(BaseModel):
    base64image: str

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/usb-exists")
def usbExists():
    return Storage.main()

@app.post("/accept-face")
async def acceptFace(photo: Photo):
    db = getDb()
    
    # Сохранение изображения во временный файл
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, 'facecodingimage')
        with open(path, 'wb') as f:
            f.write(base64.decodebytes(str.encode(photo.base64image)))

        # Поиск лиц
        response = AcceptFace.accept(path, db)

    db.close()
    
    # Возвращаем данные на клиент
    return response