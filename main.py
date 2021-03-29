import os
from werkzeug.utils import secure_filename
from flask import Flask, flash, request, redirect, send_file, render_template
from flask_bootstrap import Bootstrap
import shutil

UPLOAD_FOLDER = 'uploads/'

app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Home page
@app.route('/')
def index():
    return render_template('index.html')

# Sentiment Analysis
@app.route('/sentimentanalysis', methods=['GET', 'POST'])
def sentimentanalysis():

    if request.method == 'POST':

        # Delete existing files from the upload, download, and audio folders before processing the next/new input audio
        for filename in os.listdir(UPLOAD_FOLDER) or filename:
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            try:
                if filename!=".gitkeep" in UPLOAD_FOLDER:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)

                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)

            except Exception as e:
                print('Failed to delete. Reason: %s' % (e))
    
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
        return redirect('sentimentanalysis.html')
    return render_template('sentimentanalysis.html')

if __name__ == "__main__":
    app.run(debug=True)