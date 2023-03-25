from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def hello_world():
    return jsonify(message='Hello, World!')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return {"error": "No file part in the request."}, 400

    file = request.files['file']

    if file.filename == '':
        return {"error": "No file selected for uploading."}, 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return {"success": f"Image '{filename}' uploaded and saved."}, 200
    else:
        return {"error": "File type not allowed."}, 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
   
