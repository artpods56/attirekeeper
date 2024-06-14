import os
from typing import List
from io import BytesIO
import torch
from PIL import Image
from skimage import io
from imageio import imread
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

from utils import load_model
from inference import remove_background
from config import Config


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app = FastAPI()


@app.on_event("startup")
def startup_event():
    global model
    model = load_model()


@app.post("/remove-bg/")
async def rm_bg(file: UploadFile = File(...)):
    image_bytes = await file.read()
    image_stream = BytesIO(image_bytes)
    orig_im = imread(image_stream, format='jpg')
    orig_im_pil = Image.fromarray(orig_im)

    result_pil = remove_background(model, orig_im_pil)

    result_byte_arr = BytesIO()
    result_pil.save(result_byte_arr, format='PNG')
    result_byte_arr.seek(0)

    return StreamingResponse(result_byte_arr, media_type="image/png")

@app.post('/add-background/')
def add_background(request: Request, files: List[UploadFile] = File(...)):
    foreground = Image.open(files[1].file)
    background = Image.open(files[0].file)
    background = background.resize(foreground.size)

    mask = None
    if foreground.mode == 'RGBA':
        mask = foreground.split()[3]  # The alpha channel

    background.paste(foreground, (0, 0), mask)
    byte_arr = BytesIO()

    # Convert image to RGB before saving
    background = background.convert('RGB')
    background.save(byte_arr, format='JPEG')
    byte_arr.seek(0)
    
    return StreamingResponse(byte_arr, media_type='image/jpeg')