from fastapi import FastAPI, File, UploadFile
from fastapi.responses import Response, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import cv2

app = FastAPI(title="AI Image Colorization API")

# ✅ Enable CORS (VERY IMPORTANT for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # you can restrict later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Health check
@app.get("/")
def home():
    return {"status": "API Running 🚀"}

# ✅ Main processing endpoint
@app.post("/process")
async def process_image(file: UploadFile = File(...)):
    try:
        contents = await file.read()

        # Convert to numpy array
        npimg = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

        if img is None:
            return JSONResponse(status_code=400, content={"error": "Invalid image"})

        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 🔥 YOUR LOGIC (replace with CNN later)
        colorized = img.copy()

        # Example pseudo-coloring (can be replaced with DL model)
        colorized[gray > 180] = [0, 255, 255]   # bright → yellow
        colorized[(gray > 100) & (gray <= 180)] = [0, 255, 0]  # mid → green
        colorized[gray <= 100] = [255, 0, 0]    # dark → blue

        # Encode image
        success, buffer = cv2.imencode(".jpg", colorized)

        if not success:
            return JSONResponse(status_code=500, content={"error": "Image encoding failed"})

        return Response(content=buffer.tobytes(), media_type="image/jpeg")

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
