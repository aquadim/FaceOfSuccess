from typing import Annotated, List
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import FaceCoding.AcceptFace as AcceptFace
import base64
import tempfile
import Database
import os
import zipfile

# Фотография от клиента в кодировке base64
class Photo(BaseModel):
    base64image: str

# Запрос на создание ZIP архива по id
class ZipRequest(BaseModel):
    imageIds: List[int]

def getDb():
    return Database.DB("db.sqlite3")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Принимает фотографию с терминала
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

# Возвращает фотографию по её id
@app.get("/photo")
async def getPhoto(id: int):
    db = getDb()
    photoPath = db.getPhotoPath(id)
    db.close()
    return FileResponse(photoPath)

# Возвращает zip файл
@app.post("/zip")
async def createZip(r: ZipRequest):
    db = getDb()
    photoPaths = db.getPathsByIds(r.imageIds)
    db.close()

    # Сохранение изображения во временный файл
    # Генерируем путь к файлу
    tmpDir = tempfile.gettempdir()
    zipPath = os.path.join(tmpDir, 'bundle.zip')

    # Запись ZIP файла
    with zipfile.ZipFile(zipPath, "w") as z:
        for row in photoPaths:
            z.write(row[0], os.path.basename(row[0]))

    # Возвращаем на клиент zip файл
    return FileResponse(zipPath)