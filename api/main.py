from typing import List
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import FileResponse
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from io import BytesIO
from skimage import io
from imageio import imread
import torch
from PIL import Image
from RMBG.utilities import preprocess_image, postprocess_image
from RMBG.briarmbg import BriaRMBG


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/remove-bg/")
async def remove_background(file: UploadFile = File(...)):
    
    # Load model
    net = BriaRMBG()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    net = BriaRMBG.from_pretrained("briaai/RMBG-1.4")
    net.to(device)
    net.eval()    
    
    
    # prepare input    
    model_input_size = [1024,1024]
    
    
    # Read image from file
    image_bytes = await file.read()
    image_stream = BytesIO(image_bytes)
    orig_im = imread(image_stream, format='jpg')
    orig_im_pil = Image.fromarray(orig_im)
    orig_im_size = orig_im.shape[0:2]
    image = preprocess_image(orig_im, model_input_size).to(device)

    # inference 
    result=net(image)

    # post process
    result_image = postprocess_image(result[0][0], orig_im_size)

    # save result
    pil_im = Image.fromarray(result_image)
    no_bg_image = Image.new("RGBA", pil_im.size, (0,0,0,0))
    no_bg_image.paste(orig_im_pil, mask=pil_im)

    # Save to bytes
    img_byte_arr = BytesIO()
    no_bg_image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)

    return StreamingResponse(img_byte_arr, media_type="image/png")

@app.post('/add-background/')
def add_background(request: Request, files: List[UploadFile] = File(...)):
    foreground = Image.open(files[1].file)
    background = Image.open(files[0].file)

    # Resize background to match the size of the foreground
    background = background.resize(foreground.size)

    # If the foreground image has an alpha channel, use it as the mask
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