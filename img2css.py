# SPDX-License-Identifier: BSD-2-Clause

import os
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory, session
from flask_session import Session
from werkzeug.utils import secure_filename
import procimage
import random
import time

wpath = os.path.dirname(os.path.abspath(__file__))

def touchfolders():
    try:
        folder = wpath + "/uploads"
        os.mkdir(folder)
    except:
        pass
    try:
        folder = wpath + "/output"
        os.mkdir(folder)
    except:
        pass

APP_WEB_ROOT = '/' #  '/' or /img2css/' or '/anything/'
APP_FOLDERS = wpath
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
ANOTHER_LINK = 'https://github.com/Rodrigo-NH/Flask-img2css'
ANOTHER_LINK_TEXT = 'Source code'
MAX_OUTPUT_SIZE = '200' # Max CSS 'image' output X & Y
touchfolders();

app = Flask(__name__, static_url_path = APP_WEB_ROOT + 'static/img2css', static_folder='static/img2css')
app.secret_key = b'Your_Secret_Key_Here(Change_Me)'
app.config['APP_FOLDERS'] = APP_FOLDERS
app.config['APP_WEB_ROOT'] = APP_WEB_ROOT
app.config['ANOTHER_LINK'] = ANOTHER_LINK
app.config['ANOTHER_LINK_TEXT'] = ANOTHER_LINK_TEXT
app.config['MAX_OUTPUT_SIZE'] = MAX_OUTPUT_SIZE

@app.route(app.config['APP_WEB_ROOT']+'css')
def css():
    return render_template('css.html')

@app.route(app.config['APP_WEB_ROOT']+'output/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['APP_FOLDERS'] + '/output',
                               filename, as_attachment=True, attachment_filename="static_page.zip")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route(app.config['APP_WEB_ROOT'], methods=['GET', 'POST'])
def home():
    if session.get('key') is None:
        skey = str(int(time.time()))+"-"+str(random.randint(0,99999)) #not too secure
        session['key'] = skey
    if request.method == 'POST':
        xsize = request.form.get('xsize')
        ysize = request.form.get('ysize')
        pixsize = request.form.get('pixsize')
        grid = request.form.get('grid')
        if 'file' in request.files:
            file = request.files['file']
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['APP_FOLDERS'] + '/uploads', filename))
                a = procimage
                webdata = a.transimg(app.config['APP_FOLDERS'],
                                     filename, session.get('key'), xsize,
                                     ysize, pixsize, grid,
                                     app.config['MAX_OUTPUT_SIZE'])
                filename = session.get('key')+".zip"
                return render_template('css.html', css=webdata[0],
                                          pixel=webdata[1],
                                          siteroot=app.config['APP_WEB_ROOT'],
                                          filename = filename,
                                       suggx=int(int(app.config['MAX_OUTPUT_SIZE'])/2),
                                       sugg43=int(int(int(app.config['MAX_OUTPUT_SIZE'])/2)
                                                  /1.3333333333333), # 4:3 aspect ratio suggestion
                                       maxxy=app.config['MAX_OUTPUT_SIZE']
                                       )

    return render_template('home.html', applink=app.config['ANOTHER_LINK'],
                           applinktext=app.config['ANOTHER_LINK_TEXT'],
                           suggx=int(int(app.config['MAX_OUTPUT_SIZE'])/2),
                           sugg43=int(int(int(app.config['MAX_OUTPUT_SIZE'])/2)
                                      /1.3333333333333),
                           maxxy=app.config['MAX_OUTPUT_SIZE']
                           )

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
