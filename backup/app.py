from flask import Flask, render_template, request, jsonify
from ultralytics import YOLO
import os
import numpy as np

app = Flask(__name__)

# Load YOLO model
model_path = '/Users/fadhilahmad/Documents/apl deteksi sayur/runs/classify/train/weights/best.pt'
model = YOLO(model_path)

# Define the upload folder for images
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def classify_image(image_path):
    # Predict on the uploaded image
    results = model(image_path)
    names_dict = results[0].names
    probs = results[0].probs.data.tolist()
    predicted_class = names_dict[np.argmax(probs)]
    return predicted_class

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'files[]' not in request.files:
        return jsonify({'error': 'No files part'})

    files = request.files.getlist('files[]')
    results = []

    for file in files:
        if file.filename == '':
            continue

        # Save the uploaded file
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Classify the uploaded image
        predicted_class = classify_image(file_path)
        results.append({'class': predicted_class})

    return jsonify({'results': results})

if __name__ == '__main__':
    app.run(debug=True)
