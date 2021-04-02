import os
import glob
from werkzeug.utils import secure_filename
from flask import Flask,flash,request,redirect,send_file,render_template

UPLOAD_FOLDER = 'uploads/'

app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

headings = ["Audio segment", "Predicted emotion"]
data = [["blah1", "blah1"], ["blah2", "blah2"], ["blah3", "blah3"], ["blah4", "blah4"], ["blah5", "blah5"], ["blah6", "blah6"]]
arr = os.listdir('./uploads')

# Home page
@app.route('/')
def index():
    return render_template('index.html')

# Upload API
@app.route('/uploadfile', methods=['GET', 'POST'])
def sentimentanalysis():

    # Delete existing files from the upload before processing the next/new input audio
    # for filename in os.listdir(UPLOAD_FOLDER):
    #     file_path = os.path.join(UPLOAD_FOLDER, filename)
        
    #     try:
    #         if filename!=".gitkeep":
    #             if os.path.isfile(file_path) or os.path.islink(file_path):
    #                 os.unlink(file_path)

    #             elif os.path.isdir(file_path):
    #                 shutil.rmtree(file_path)

    #     except Exception as e:
    #         print('Failed to delete. Reason: %s' % (e))
    
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
            print("saved file successfully")

      #send file name as parameter to downlad
            return redirect('/downloadfile/'+ filename)
    return render_template('sentimentanalysis.html')


# Download API
@app.route("/downloadfile/<filename>", methods = ['GET'])
def download_file(filename):
    for i in arr:
        if i!='.gitkeep':
            # print(i)
        
            for j, i in enumerate(glob.glob(".\\uploads\\*.mp3")):
                data[j][0] = i
    return render_template('download.html',value=filename, headings=headings, data=data)

# @app.route('/return-files/<filename>')
# def return_files_tut(filename):
#     file_path = UPLOAD_FOLDER + filename
#     return send_file(file_path, as_attachment=True, attachment_filename='')

if __name__ == "__main__":
    app.run(debug=True)