m4a_file = '4.mp3'
wav_filename = r"F:\20211210_151013.wav"
from pydub import AudioSegment
track = AudioSegment.from_file(m4a_file,  format= 'mp3')
file_handle = track.export(wav_filename, format='wav')