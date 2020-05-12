
import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

from my_module.video_processing import vp

app = Flask(__name__)

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['mov', 'mp4', 'm4a', 'avi', 'wmv'])
IMAGE_WIDTH = 640
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = os.urandom(24)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def temp():
    return render_template('temp.html')

@app.route('/send', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        video_file = request.files['img_file']

        # 変なファイルを弾く　
        if video_file and allowed_file(video_file.filename):
            filename = secure_filename(video_file.filename)
        else:
            return ''' <p>許可されていない拡張子です</p> '''

        pulse_graph_url = os.path.join(app.config['UPLOAD_FOLDER'], 'pulse_' + filename)

        # アップロードした動画を分析し、心拍数のグラフを保存
        vp(video_file, filename)

        return render_template('temp.html', pulse_graph_url=pulse_graph_url)

    else:
        return redirect(url_for('temp'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.debug = True
    app.run()