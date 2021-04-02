import os
import glob
from werkzeug.utils import secure_filename
from flask import Flask,flash,request,redirect,send_file,render_template
import shutil

UPLOAD_FOLDER = 'uploads/'
AUDIO_FOLDER = './static/audios/'

app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
data=[]
emotion=["angry","sad"]

# Home page
@app.route('/')
def index():
    return render_template('index.html')

# Upload API
@app.route('/uploadfile', methods=['GET', 'POST'])
def sentimentanalysis():

    # Delete existing files from the upload, download, and audio folders before processing the next/new input audio
    for filename in os.listdir(UPLOAD_FOLDER) or filename in os.listdir(AUDIO_FOLDER):
        file_path1 = os.path.join(UPLOAD_FOLDER, filename)
        file_path2 = os.path.join(AUDIO_FOLDER, filename)
        try:
            if filename!=".gitkeep":
                if os.path.isfile(file_path1) or os.path.islink(file_path1) or os.path.isfile(file_path2) or os.path.islink(file_path2):
                    os.unlink(file_path1)
                    os.unlink(file_path2)

                elif os.path.isdir(file_path1) or os.path.isdir(file_path2):
                    shutil.rmtree(file_path1)
                    shutil.rmtree(file_path2)

        except Exception as e:
            print('Failed to delete. Reason: %s' % (e))
    
    if request.method == 'POST':

        # check if the post request has the file part
        if 'file' not in request.files:
            print('no file')
            return redirect(request.url)
        file = request.files['file']

        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print('no filename')
            return redirect(request.url)
        else:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # shutil.copy(os.path.join(app.config['UPLOAD_FOLDER'], filename), os.path.join(app.config['AUDIO_FOLDER'], filename))

      #send file name as parameter to downlad
            return redirect('/downloadfile/'+ filename)
    return render_template('sentimentanalysis.html')


# Download API
@app.route("/downloadfile/<filename>", methods = ['GET'])
def download_file(filename):
    for audio_files in AUDIO_FOLDER:
        data=glob.glob('./static/audios/*.mp3', recursive=True)
    result = [sub.replace('./static/', '') for sub in data]
    res = [sub.replace('\\', '/') for sub in result]
    return render_template('download.html',data=data, res=res, emotion=emotion, len=len(emotion))

if __name__ == "__main__":
    app.run(debug=True)