import numpy as np
from flask import Flask, request, jsonify, render_template 
from flask_cors import CORS
import tensorflow as tf
from pydub import AudioSegment
from keras.models import load_model
import io
import os
import pathlib




application = Flask(__name__) #Initialize the flask App

CORS(application)

AUTOTUNE = tf.data.AUTOTUNE


commands = ['Back', 'Close', 'Forward', 'Home', 'Refresh', 'Tab']


# Decode WAV-encoded audio files to `float32` tensors, normalized
# to the [-1.0, 1.0] range. Return `float32` audio and a sample rate.
def decode_audio(audio_binary):
    audio, _ = tf.audio.decode_wav(contents=audio_binary)
    # Since all the data is single channel (mono), drop the `channels` axis from the array.
    return tf.squeeze(audio, axis=-1)
#get label for file
def get_label(file_path):
    parts = tf.strings.split(input=file_path, sep=os.path.sep)
    return parts[-2]
#compbine both functions
def get_waveform_and_label(file_path):
    label = get_label(file_path)
    audio_binary = tf.io.read_file(file_path)
    waveform = decode_audio(audio_binary)
    return waveform, label

def get_spectrogram(waveform):
    # Zero-padding for an audio waveform with less than 60000 samples.
    input_len = 60000
    waveform = waveform[:input_len]
    zero_padding = tf.zeros([60000] - tf.shape(waveform), dtype=tf.float32)
    # Cast the waveform tensors' dtype to float32.
    waveform = tf.cast(waveform, dtype=tf.float32)
    # Concatenate the waveform with `zero_padding`, which ensures all audio
    # clips are of the same length.
    equal_length = tf.concat([waveform, zero_padding], 0)
    # Convert the waveform to a spectrogram via a STFT.
    spectrogram = tf.signal.stft(equal_length, frame_length=255, frame_step=128)
    # Obtain the magnitude of the STFT.
    spectrogram = tf.abs(spectrogram)
    # Add a `channels` dimension, so that the spectrogram can be used
    # as image-like input data with convolution layers (which expect
    # shape (`batch_size`, `height`, `width`, `channels`).
    spectrogram = spectrogram[..., tf.newaxis]
    return spectrogram


def get_spectrogram_and_label_id(audio, label):
    spectrogram = get_spectrogram(audio)
    label_id = tf.argmax(label == commands)
    return spectrogram, label_id

def preprocess_dataset(files):
    files_ds = tf.data.Dataset.from_tensor_slices(files)
    output_ds = files_ds.map(map_func=get_waveform_and_label, num_parallel_calls=AUTOTUNE)
    output_ds = output_ds.map(map_func=get_spectrogram_and_label_id,num_parallel_calls=AUTOTUNE)
    return output_ds

def get_mono(np_arr):
    s = io.BytesIO(np_arr)
    audio = AudioSegment.from_file(s)
    audio.split_to_mono()[0].export("recordings/recording.wav",format="wav")

@application.route('/')
def home():
    return render_template('idx.html')

@application.route('/predict',methods=['POST'])
def predict():
    #get value from request
    wav_file = request.files['audio_data']
    np_arr = np.array(wav_file.read())
    get_mono(np_arr)

    model = load_model('model.h5')

    
    data_dir = pathlib.Path('recordings/')


    sample_file = data_dir/'recording.wav'

    sample_ds = preprocess_dataset([str(sample_file)])

    for spectrogram, label in sample_ds.batch(1):
        prediction = model(spectrogram)
        arr = tf.nn.softmax(prediction[0]).numpy()
    
    
    return jsonify(commands[arr.argmax()])



if __name__ == "__main__":
    application.run(debug=True)