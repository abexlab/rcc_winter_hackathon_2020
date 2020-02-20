import glob, rwave
import librosa

files = glob.glob('audio/*.wav')
for f in files:
    wave, fs = librosa.load(f)
    wave *= 10000
    wave, _  = rwave.convert_fs(wave, fs, 8000)

    rwave.write_wave(f, wave, 8000)
