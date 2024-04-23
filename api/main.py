from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.responses import StreamingResponse
from io import BytesIO
from skimage import io
from imageio import imread
import torch
from PIL import Image
from RMBG.utilities import preprocess_image, postprocess_image
from RMBG.briarmbg import BriaRMBG

app = FastAPI()

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