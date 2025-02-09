from typing import Annotated, List
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import Storage.Utils as Storage
import FaceCoding.AcceptFace as AcceptFace
import base64
import tempfile
import Database
import os
import zipfile

def getDb():
    return Database.DB("db.sqlite3")

class Photo(BaseModel):
    base64image: str

class SaveRequest(BaseModel):
    images: List[int]
    savepath: str

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/get-name-to-save")
async def getMountPoint():
    mountPoint = Storage.getMountPoint()
    if mountPoint == None:
        return {"ok": False}
    return {"ok": True, "path": Storage.generateZipName(mountPoint)}

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

@app.get("/photo")
async def getPhoto(id: int):
    db = getDb()
    photoPath = db.getPhotoPath(id)
    db.close()
    return FileResponse(photoPath)

@app.post("/save")
async def save(r: SaveRequest):
    db = getDb()
    photoPaths = db.getPathsByIds(r.images)
    db.close()

    with zipfile.ZipFile(r.savepath, "w") as z:
        for row in photoPaths:
            z.write(row[0], os.path.basename(row[0]))
    return {"ok": True}