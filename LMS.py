import numpy as np
import soundfile as sf
import padasip as pa
import os
import random
import librosa
def signaltonoise(a, axis=0, ddof=0):
    a = np.asanyarray(a)
    m = a.mean(axis)
    sd = a.std(axis=axis, ddof=ddof)
    return np.where(sd == 0, 0, m/sd)



def denoise_audio(noisy_audio_path, noise_path900,noise_path750,noise_path600,noise_path500, output_path):
    filenames = os.listdir(noisy_audio_path)
    random.shuffle(filenames)  # Shuffle the list in-place
    for filename in filenames:
        file_path = os.path.join(noisy_audio_path, filename)
        noisy_file_path = os.path.join(noisy_audio_path, file_path)
        #compare pitch
        y, sr = librosa.load(noisy_file_path)
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
        dominant_pitches = pitches[magnitudes > np.median(magnitudes)]
        if len(dominant_pitches) > 0:
            dominant_pitch = np.mean(dominant_pitches)
        else:
            dominant_pitch = 0
        
        if 900 <= dominant_pitch:
            noise, sr_noise = sf.read(noise_path900)
            print(f"Dominant Pitch: {dominant_pitch} Hz" + filename +" 900")
        elif 750 <= dominant_pitch <900:
            noise, sr_noise = sf.read(noise_path750)
            print(f"Dominant Pitch: {dominant_pitch} Hz" + filename + "750")
        elif 600 <= dominant_pitch < 750:
            noise, sr_noise = sf.read(noise_path600)
            print(f"Dominant Pitch: {dominant_pitch} Hz" + filename + "600")
        elif dominant_pitch <600: 
            noise, sr_noise = sf.read(noise_path500)
            print(f"Dominant Pitch: {dominant_pitch} Hz" + filename + "500")
        # Load the noisy audio and the noise (assuming same length and sample rate)
            
        # Remove DC offset by subtracting the mean
        #y -= np.mean(y)


        # Ensure the audio is normalized to avoid clipping
        #y = librosa.util.normalize(y)
        noisy_audio, sr_noisy = sf.read(noisy_file_path)
        
        # Ensure both files have the same sample rate and are mono
        assert sr_noisy == sr_noise, "Sample rates do not match"
        assert len(noisy_audio.shape) == 1 and len(noise.shape) == 1, "Audio files are not mono"
        
        # Initialize the LMS filter
        # The filter length (n) can be adjusted based on your specific needs
        n = 320 # Number of taps in the LMS filter
        lms_filter = pa.filters.FilterLMS(n=n, mu=0.01, w="zeros")
        
        # Prepare the input vector for the LMS filter
        # Using the noise as the reference input and the noisy audio as the desired signal
        N = min(len(noisy_audio), len(noise)) - n
        X = np.array([noise[i:i+n] for i in range(N)])
        d = noisy_audio[n:N+n]
        
        # Apply the LMS filter
        y, e, w = lms_filter.run(d, X)
        
        # 'e' contains the filtered signal (denoised audio)
        # Save the denoised audio
        enhanced_file_path = os.path.join(output_path, "enh" + filename)
        sf.write(enhanced_file_path, e, sr_noisy)

        print("estimated Original SNR: ", signaltonoise(noisy_audio))
        print("estimated Enhanced SNR: ", signaltonoise(e))

# Example usage
noisy_audio_path = "D:/20241.1-2024.8.31/drone_microphone/dataset/keywords/20mm/320/test"
noise_path900 = "D:/20241.1-2024.8.31/drone_microphone/dataset/noise/output900.wav"
noise_path750 = "D:/20241.1-2024.8.31/drone_microphone/dataset/noise/output750.wav"
noise_path600 = "D:/20241.1-2024.8.31/drone_microphone/dataset/noise/output600.wav"
noise_path500 = "D:/20241.1-2024.8.31/drone_microphone/dataset/noise/output500.wav"
output_path = "D:/20241.1-2024.8.31/drone_microphone/dataset/keywords/20mm/320/oneref_test"
denoise_audio(noisy_audio_path, noise_path900,noise_path750,noise_path600,noise_path500, output_path)