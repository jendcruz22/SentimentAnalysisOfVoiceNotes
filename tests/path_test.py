import os
import sys

sys.path.append(os.path.abspath("../"))

from sentiment_analysis.Utils import *

relative_path = "../assets/temp/models/audio_sentiment_model"

print("Relative path: ", relative_path)
print("Absloute path: ", path(relative_path))