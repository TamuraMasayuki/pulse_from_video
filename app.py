import os
from flask import Flask, render_template, request, redirect, url_for
import numpy as np
import cv2

from my_module.video_processing import vp

app = Flask(__name__)

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['mov', 'mp4', 'm4a', 'avi', 'wmv'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = os.urandom(24)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        video_file = request.files['video_file']

        # 変なファイルを弾く　
        if not video_file or not allowed_file(video_file.filename):
            return ''' <p>許可されていない拡張子です</p> '''


        # アップロードした動画を分析し、心拍数を返す
        stream = video_file.stream
        img_array = np.asarray(bytearray(stream.read()), dtype=np.uint8)
        img_set = cv2.imdecode(img_array, 1)

        # img_setがOpenCVに読み込める動画の形式になっていないためエラーが出る
        heart_rate = vp(img_set)

        return render_template('index.html', heart_rate=heart_rate)

    else:
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.debug = True
    app.run()