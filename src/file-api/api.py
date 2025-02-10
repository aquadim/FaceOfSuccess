# API для взаимодействия с файловой системой терминала из веб-окружения
from typing import Annotated
from fastapi import FastAPI, Request, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import filesystem
import os

class SaveRequest(BaseModel):
    zipfile: UploadFile = File(...)
    savepath: str

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Возвращает имя файла для сохранения
@app.get("/get-name-to-save")
async def getMountPoint():
    mountPoint = filesystem.getMountPoint()
    if mountPoint == None:
        return {"ok": False}
    return {"ok": True, "path": filesystem.generateZipName(mountPoint)}

# Сохраняет zip файл в заданный путь
@app.post("/save")
async def save(r: SaveRequest = Form(..., media_type="multipart/form-data")):
    with open(r.savepath, "wb") as f:
        f.write(await r.zipfile.read())