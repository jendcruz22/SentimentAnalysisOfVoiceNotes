import os
import sys

sys.path.append(os.path.abspath("../"))
print(sys.path)

from sentiment_analysis.Utils import *


relative_path = "../assets/temp/models/audio_sentiment_model"

absolute_path = os.path.abspath(relative_path)

print(relative_path)
print(path(relative_path))