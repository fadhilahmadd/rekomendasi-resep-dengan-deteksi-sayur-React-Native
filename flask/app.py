import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from features.image_classifier import classify_image
from flask_cors import CORS
from werkzeug.utils import secure_filename

from routes.categories import categories_blueprint
from routes.meals import meals_blueprint
from routes.recipe import recipe_blueprint
from routes.categories_detect import categories_detect_blueprint
from routes.meals_detect import meals_detect_blueprint
from routes.all_categories_detect import all_categories_detect_blueprint
from routes.all_meals_detect import all_meals_detect_blueprint

app = Flask(__name__, static_folder='img')
CORS(app, resources={r"/*": {"origins": "*"}})

app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/img/<path:filename>') 
def send_file(filename): 
    return send_from_directory(app.static_folder, filename)

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'files[]' not in request.files:
        return jsonify({'error': 'No files part'})

    files = request.files.getlist('files[]')
    results = []

    for file in files:
        if file.filename == '':
            continue

        # Secure and clean the filename before saving
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        predicted_class = classify_image(file_path)

        # Replace underscore with space in the predicted_class
        predicted_class = predicted_class.replace('_', ' ')

        results.append({'class': predicted_class})

    return jsonify({'results': results})

app.register_blueprint(categories_blueprint)
app.register_blueprint(meals_blueprint)
app.register_blueprint(recipe_blueprint)
app.register_blueprint(categories_detect_blueprint)
app.register_blueprint(meals_detect_blueprint)
app.register_blueprint(all_categories_detect_blueprint)
app.register_blueprint(all_meals_detect_blueprint)

if __name__ == '__main__':
    app.run(host='192.168.0.160', port=5000,debug=True)
    # app.run(debug=True)
