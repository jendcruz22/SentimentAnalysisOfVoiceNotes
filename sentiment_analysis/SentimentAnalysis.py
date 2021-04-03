from glob import glob
import keras
import ktrain
import librosa

# from multiprocessing import Pool
import shutil
import tensorflow as tf
import time

from sentiment_analysis.AudioAnalysis import *
from sentiment_analysis.IbmTranscription import *
from sentiment_analysis.TextAnalysis import *
from sentiment_analysis.Utils import *


def analyzeSentiments(file_path):

    file_name = (file_path.split("\\")[-1])[:-4]
    creation_time = time.time()

    paths = {
        "audio_model": path("assets/models/audio_sentiment_model"),
        "pickles": path("assets/pickles"),
        "text_model": path("assets/models/text_sentiment_model"),
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

    # Loading the text analyzer model and classes
    text_predictor = ktrain.load_predictor(paths["text_model"])
    text_classes = text_predictor.get_classes()
    print("Loaded text model")

    # Setting up IBM
    stt = setUpIBM()
    print("Setup IBM")

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

        text_emotions, transcription = analyzeText(
            file_name=file_name, stt=stt, predictor=text_predictor
        )
        print("performed text analysis")

        audio_emotions = analyzeAudio(
            file_name=file_name, model=audio_model, scaler=audio_scaler
        )
        print("performed audio analysis")

        # Taking weighted average of text and audio emotions in the ratio 65:35
        weighted_text_emotions = text_emotions * 0.5
        weighted_audio_emotions = audio_emotions * 0.5
        weighted_emotions = weighted_text_emotions + weighted_audio_emotions

        # Picking the dominant emotion and labelling it
        weighted_emotions = weighted_emotions.argmax()
        weighted_emotions = weighted_emotions.astype(int).flatten()
        final_emotion = audio_classes.inverse_transform((weighted_emotions))

        transcriptions.append(transcription)
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
