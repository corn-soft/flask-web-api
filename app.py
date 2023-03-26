from flask import Flask, jsonify, request, send_file
from werkzeug.utils import secure_filename
from PIL import Image
import io
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

# 画像入力（結果画像送信有り）

@app.route('/upload', methods=['POST'])
def upload_image():
    # print(request.headers)  # リクエストのヘッダー情報を出力
    # print(request.files)    # リクエストのファイル情報を出力
    # print(request.data)    # リクエストのファイル情報を出力

    if 'file' not in request.files:
        return {"error": "No file part in the request."}, 400

    file = request.files['file']

    if file.filename == '':
        return {"error": "No file selected for uploading."}, 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)

#        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#        return {"success": f"Image '{filename}' uploaded and saved."}, 200

        # Read the image file and convert it to grayscale
        image = Image.open(file.stream).convert('L')

        # Save the grayscale image to a temporary file
        output_buffer = io.BytesIO()
        image.save(output_buffer, format='JPEG')
        output_buffer.seek(0)

        # Return the grayscale image to the client
        return send_file(output_buffer, mimetype='image/jpeg', as_attachment=True, download_name='grayscale.jpg')

    else:
        return {"error": "File type not allowed."}, 400

# 画像入力（結果画像送信有り）

@app.route('/upload2', methods=['POST'])
def upload_image2():
    if 'file' not in request.files:
        return {"error": "No file part in the request."}, 400

    file = request.files['file']

    if file.filename == '':
        return {"error": "No file selected for uploading."}, 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)

#        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return {"success": f"Image '{filename}' uploaded and saved."}, 200
    else:
        return {"error": "File type not allowed."}, 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
   
