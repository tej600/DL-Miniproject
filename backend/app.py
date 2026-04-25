from flask import Flask, request, jsonify, send_file
import cv2
import numpy as np
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def process_image(image_path):
    # Read image
    img = cv2.imread(image_path)

    # Example processing (you can modify this)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 100, 200)

    return edges


@app.route('/')
def home():
    return "Image Processing API is running"


@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['image']
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # Process image
    output = process_image(filepath)

    output_path = os.path.join(OUTPUT_FOLDER, "processed_" + file.filename)
    cv2.imwrite(output_path, output)

    return send_file(output_path, mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True)
