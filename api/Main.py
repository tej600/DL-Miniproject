from fastapi import FastAPI, File, UploadFile
import numpy as np
import cv2
from fastapi.responses import Response

app = FastAPI()

@app.get("/")
def home():
    return {"message": "API is running"}

@app.post("/process")
async def process_image(file: UploadFile = File(...)):
    contents = await file.read()

    npimg = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Your logic
    img[gray > 120] = [0, 255, 0]

    _, buffer = cv2.imencode(".jpg", img)

    return Response(content=buffer.tobytes(), media_type="image/jpeg")
