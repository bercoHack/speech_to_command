import librosa    
import numpy as np
import scipy
from scipy.io.wavfile import write

y, s = librosa.load('converting/pc.wav', sr=8000) # Downsample 44.1kHz to 8kHz
print(y)
print(s)

scipy.io.wavfile.write('converting/pc.wav', s, y)
