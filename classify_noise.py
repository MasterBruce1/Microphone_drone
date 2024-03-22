import numpy as np
import os
import random
import librosa
import shutil

def denoise_audio(noisy_audio_path, output_path900, output_path750, output_path600,output_path500):
    filenames = os.listdir(noisy_audio_path)
    random.shuffle(filenames)  # Shuffle the list in-place
    a = 0
    b = 0
    for filename in filenames:
        file_path = os.path.join(noisy_audio_path, filename)
        noisy_file_path = os.path.join(noisy_audio_path, file_path)
        # Load the noisy audio and the noise 
        noisy_audio, sr_noisy = librosa.load(noisy_file_path)
        pitches, magnitudes = librosa.piptrack(y=noisy_audio, sr=sr_noisy)
        # and then calculate the mean of these values.
        dominant_pitches = pitches[magnitudes > np.median(magnitudes)]
        if len(dominant_pitches) > 0:
            dominant_pitch = np.mean(dominant_pitches)
        else:
            dominant_pitch = 0

        print(f"Dominant Pitch: {dominant_pitch} Hz" + filename)

        if 900 <= dominant_pitch:
            shutil.move(file_path, os.path.join(output_path900, filename))
            print(f"Moved: {filename} - Pitch: {dominant_pitch} Hz")
        elif 750 <= dominant_pitch < 900:
            shutil.move(file_path, os.path.join(output_path750, filename))
            print(f"Moved: {filename} - Pitch: {dominant_pitch} Hz")
        elif 600 <= dominant_pitch < 750:
            shutil.move(file_path, os.path.join(output_path600, filename))
            print(f"Moved: {filename} - Pitch: {dominant_pitch} Hz")
        elif dominant_pitch < 600:
            shutil.move(file_path, os.path.join(output_path500, filename))
            print(f"Moved: {filename} - Pitch: {dominant_pitch} Hz")

        a = a + dominant_pitch
        b = b + 1
    C = a/b
    print("average pitch :" + str(C) + "Hz")

noisy_audio_path = "D:/20241.1-2024.8.31/drone_microphone/dataset/noise/20mm_40%"
output_path900 = "D:/20241.1-2024.8.31/drone_microphone/dataset/noise/20mm_900p"
output_path750 = "D:/20241.1-2024.8.31/drone_microphone/dataset/noise/20mm_750p"
output_path600 = "D:/20241.1-2024.8.31/drone_microphone/dataset/noise/20mm_600p"
output_path500 = "D:/20241.1-2024.8.31/drone_microphone/dataset/noise/20mm_500p"
denoise_audio(noisy_audio_path, output_path900, output_path750, output_path600,output_path500)