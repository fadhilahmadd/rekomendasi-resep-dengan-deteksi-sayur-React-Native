from flask import Flask, render_template, request, jsonify
from ultralytics import YOLO
import os
from features.image_classifier import classify_image

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

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

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        predicted_class = classify_image(file_path)  # Call classify_image function
        results.append({'class': predicted_class})

    return jsonify({'results': results})

if __name__ == '__main__':
    app.run(debug=True)