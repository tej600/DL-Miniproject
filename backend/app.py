from fastapi import FastAPI, File, UploadFile
from fastapi.responses import Response
import numpy as np
import cv2

app = FastAPI()

@app.get("/")
def home():
    return {"message": "API Running"}

@app.post("/process")
async def process_image(file: UploadFile = File(...)):
    contents = await file.read()

    npimg = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    if img is None:
        return {"error": "Invalid image"}

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    img[gray > 120] = [0, 255, 0]

    _, buffer = cv2.imencode(".jpg", img)

    return Response(content=buffer.tobytes(), media_type="image/jpeg")
