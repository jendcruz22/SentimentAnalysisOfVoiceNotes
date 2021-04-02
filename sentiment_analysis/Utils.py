import subprocess
import os
import librosa
import soundfile as sf


def path(relative_path):
    return os.path.abspath(relative_path)


def convertToWav(file_name, file_path, save_path):
    wav_file_name = f"{save_path}\{file_name}.wav"
    subprocess.call(["ffmpeg", "-i", file_path, wav_file_name])
    return wav_file_name


def segmentAudioFile(file_name, file_path, save_path):
    audio, sr = librosa.load(file_path)
    buffer = 30 * sr

    samples_total = len(audio)
    samples_wrote = 0
    counter = 1

    while samples_wrote < samples_total:

        # check if the buffer is not exceeding total samples
        if buffer > (samples_total - samples_wrote):
            buffer = samples_total - samples_wrote

        block = audio[samples_wrote : (samples_wrote + buffer)]
        out_file_name = f"{file_name}_clip_" + str(counter) + ".wav"
        complete_name = f"{save_path}/{out_file_name}"

        sf.write(complete_name, block, sr)

        counter += 1
        samples_wrote += buffer