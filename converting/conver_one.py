import os
from pydub import AudioSegment

src = '4.mp3'
des = '4.wav'
track = AudioSegment.from_file(src,  format= 'm4a')
file_handle = track.export(des, format='wav')
