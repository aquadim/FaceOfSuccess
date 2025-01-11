from typing import Annotated
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import Storage.Utils as Storage

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
    return photo.base64image