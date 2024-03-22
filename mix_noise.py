import librosa
import numpy as np
import soundfile as sf
import os

def average_audio_files(folder_path, output_file):
    # List all the audio files in the folder
    audio_files = [f for f in os.listdir(folder_path) if f.endswith('.wav')]
    accumulated_audio = None
    sample_rate = None

    for file_name in audio_files:
        # Load the audio file
        file_path = os.path.join(folder_path, file_name)
        audio, sr = librosa.load(file_path, sr=None) # Load with original sample rate
        
        if accumulated_audio is None:
            accumulated_audio = np.zeros_like(audio)
            sample_rate = sr
        elif sr != sample_rate:
            raise ValueError("Sample rates do not match across audio files.")
        
        # Accumulate the audio data
        accumulated_audio += audio
    
    # Average the accumulated audio data
    average_audio = accumulated_audio / len(audio_files)
    
    # Remove DC offset by subtracting the mean
    # average_audio -= np.mean(average_audio)


    # Ensure the audio is normalized to avoid clipping
    # average_audio = librosa.util.normalize(average_audio)
    
    # Write the result to the output file
    sf.write(output_file, average_audio, sample_rate)

# Define the path to the folder and the output file
folder_path = 'D:/20241.1-2024.8.31/drone_microphone/dataset/noise/20mm_600_750p'
output_file = 'D:/20241.1-2024.8.31/drone_microphone/dataset/noise/output600.wav'

# Generate the representative audio file
average_audio_files(folder_path, output_file)
