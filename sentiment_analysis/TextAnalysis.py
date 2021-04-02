import ktrain
from ktrain import text
import numpy as np
import pandas as pd
import tensorflow as tf

from sentiment_analysis.IbmTranscription import transcribeAudio


def loadModel(modelPath):
    predictor = ktrain.load_predictor(modelPath)
    classes = predictor.get_classes()
    return predictor, classes


def analyzeText(file_name, stt, predictor):

    # Transcribe the audio
    text, conf = transcribeAudio(file=file_name, stt=stt)

    words = text.split(" ")
    split_length = len(words) // 3

    split_text = []
    split_index = 0

    for i in range(2):
        split_text.append(text[split_index : split_index + split_length])
        split_index = split_index + split_length
    split_text.append(text[split_index::])

    split_sentences = []
    for i in range(len(split_text)):
        sentence = " ".join(split_text[i])
        split_sentences.append(sentence)

    final_preds = []
    for i in range(len(split_sentences)):
        prediction = predictor.predict(split_sentences[i], return_proba=True)
        final_preds.append(prediction)

    text_emotions = np.sum(final_preds, axis=0) / 3

    return text_emotions, text
