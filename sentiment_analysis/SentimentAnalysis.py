from glob import glob
import keras
import librosa

# from multiprocessing import Pool
import shutil
import time

from sentiment_analysis.AudioAnalysis import *
from sentiment_analysis.Utils import *


def analyzeSentiments(file_path):

    file_name = (file_path.split("\\")[-1])[:-4]
    creation_time = time.time()

    paths = {
        "audio_model": path("assets/models/audio_sentiment_model"),
        "pickles": path("assets/pickles"),
        "wav_save_path": path(f"static/temp/{file_name}-{creation_time}"),
        "clips_save_path": path(f"static/temp/{file_name}-{creation_time}/clips"),
    }

    # Creating directories in temp to store the converted wav file and the clips
    os.mkdir(paths["wav_save_path"])
    os.mkdir(paths["clips_save_path"])

    # Loading the audio analyzer model, scaler and classes
    audio_model, audio_scaler, audio_classes = loadAudioAssets(
        model_path=paths["audio_model"], pickles_path=paths["pickles"]
    )
    print("Loaded audio model")

    # Converting the mp3 file to a wav file
    wav_file_path = convertToWav(
        file_name=file_name, file_path=file_path, save_path=paths["wav_save_path"]
    )
    print("Converted to wav")

    # Segment the audio file into 30 second clips
    segmentAudioFile(
        file_name=file_name, file_path=wav_file_path, save_path=paths["clips_save_path"]
    )
    print("Segmented audio")

    transcriptions = []
    emotions = []
    clips = glob(f'{paths["clips_save_path"]}/*.wav')

    for file_name in clips:

        weighted_emotions = analyzeAudio(
            file_name=file_name, model=audio_model, scaler=audio_scaler
        )
        print("performed audio analysis")

        # Picking the dominant emotion and labelling it
        weighted_emotions = weighted_emotions.argmax()
        weighted_emotions = weighted_emotions.astype(int).flatten()
        final_emotion = audio_classes.inverse_transform((weighted_emotions))

        emotions.append(final_emotion)
    print("performed sentiment analysis")

    final_clips = []

    for clip in clips:
        elements = clip.split("\\")
        final_clips.append("temp/" + "/".join(elements[len(elements) - 3 :]))

    return (
        final_clips,
        emotions,
        paths["wav_save_path"],
    )


def deleteTempDirectory(path):
    # Deleting the temperory directory
    try:
        shutil.rmtree(path)
    except OSError as e:
        print("Error: %s : %s" % (path, e.strerror))
