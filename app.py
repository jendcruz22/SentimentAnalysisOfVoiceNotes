import os
import glob
import shutil
import sys
from werkzeug.utils import secure_filename
from flask import Flask, flash, request, redirect, send_file, render_template, url_for, session, jsonify, json

sys.path.append(os.path.abspath("../"))

from sentiment_analysis.SentimentAnalysis import *
from sentiment_analysis.Utils import path
from sentiment_analysis.clean_folder import *

UPLOAD_FOLDER = "uploads/"
AUDIO_FOLDER = "./static/temp/"

app = Flask(__name__, template_folder="templates")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
final_filename = ""

# Home page
@app.route("/")
def index():
    return render_template("index.html")

# Upload API
@app.route("/uploadfile", methods=["GET", "POST"])
def sentimentanalysis():

    if request.method == "POST":
        # clean the existing files from the given folders
        clean_folder(UPLOAD_FOLDER)
        clean_folder(AUDIO_FOLDER)

        # check if the post request has the file part
        if "file" not in request.files:
            print("no file")
            return redirect(request.url)
        file = request.files["file"]

        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == "":
            print("no filename")
            return redirect(request.url)
        else:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            
            global final_filename
            final_filename = filename

            # send file name as parameter to downlad
            return redirect("/download_file/")
    return render_template("sentimentanalysis.html")

# Download API
@app.route("/download_file/", methods=["GET"])
def download_file():
    clips, emotions, temp_folder = analyzeSentiments(path(f"{UPLOAD_FOLDER}/{final_filename}"))
    emotions = np.array(emotions).flatten()

    return render_template(
        "download.html", clips=clips, emotions=emotions, len=len(clips)
    )


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)