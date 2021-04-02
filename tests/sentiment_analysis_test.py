import sys
import os

sys.path.append(os.path.abspath("../"))

from sentiment_analysis.SentimentAnalysis import *
from sentiment_analysis.Utils import path

# Functions to be called
clips, emotions, temp_folder = analyzeSentiments(
    path("../uploads/Alice_in_Wonderland_test.mp3")
)
print(clips)
print(emotions)

print("List of clips:")
for clip in clips:
    print(clip)
print("\nList of emotions:")
for emotion in emotions:
    print(emotion)
print("\nTemp folder:\n", temp_folder)

# Call this at the end of the session
# deleteTempDirectory(temp_folder)