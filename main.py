import os
from werkzeug.utils import secure_filename
from flask import Flask, flash, request, redirect, send_file, render_template
from flask_bootstrap import Bootstrap
import shutil

UPLOAD_FOLDER = 'voicenote/'

app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Home page
@app.route('/')
def index():
    return render_template('index.html')

# Upload API
@app.route('/uploadfile', methods=['GET', 'POST'])
def upload_file():

    # Delete existing files from the upload, download, and audio folders before processing the next/new input audio
    for filename in os.listdir(UPLOAD_FOLDER):
        file_path1 = os.path.join(UPLOAD_FOLDER, filename)
        try:
            if filename!=".gitkeep":
                if os.path.isfile(file_path1) or os.path.islink(file_path1):
                    os.unlink(file_path1)

                elif os.path.isdir(file_path1):
                    shutil.rmtree(file_path1)

        except Exception as e:
            print('Failed to delete. Reason: %s' % (e))
    
    if request.method == 'POST':

        # check if the post request has the file part
        if 'file' not in request.files:
            print('no file')
            return redirect(request.url)
        file = request.files['file']

        # if user does not select file, browser also submit a empty part without filename
        if file.filename == '':
            print('no filename')
            return redirect(request.url)

        else:
            filename = secure_filename(file.filename)
            # save the input audio in the uploads folder
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print("saved file successfully")

            # send file name as parameter to download
            # return redirect('/player/'+ filename)
    return render_template('upload_file.html')

if __name__ == "__main__":
    app.run(debug=True)