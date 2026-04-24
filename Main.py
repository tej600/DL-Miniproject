from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
import numpy as np
import cv2
import io

app = FastAPI()

@app.post("/process")
async def process_image(file: UploadFile = File(...)):
    contents = await file.read()

    npimg = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Example: threshold coloring
    colored = img.copy()
    colored[gray > 120] = [0, 255, 0]

    _, buffer = cv2.imencode('.jpg', colored)
    io_buf = io.BytesIO(buffer)

    return StreamingResponse(io_buf, media_type="image/jpeg")