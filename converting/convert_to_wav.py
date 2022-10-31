import os
from pydub import AudioSegment


for folder in os.listdir('recorded_words'):
    i = 0
    for file in os.listdir('recorded_words\\' + folder):
        i = i + 1
        src = 'recorded_words\\' + folder + "\\" + file
        des = "recorded_words_wav\\" + folder + "\\" + str(i) + ".wav"
        print(i)
        track = AudioSegment.from_file(src,  format= 'm4a')
        file_handle = track.export(des, format='wav')



