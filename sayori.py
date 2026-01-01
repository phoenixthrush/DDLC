import matplotlib.pylab as plt
import numpy as np
import scipy.signal
from pydub import (
    AudioSegment,
)  # ModuleNotFoundError: No module named 'pyaudioop' (on 3.14.2)

# Load audio
sound = AudioSegment.from_file("staged/sayori/0_sayori.ogg")
samples = np.array(sound.get_array_of_samples())

# -----------------------
# 1. Save raw waveform
# -----------------------
plt.figure(figsize=(12, 4))
plt.plot(samples, color="black")
plt.xlabel("Sample index")
plt.ylabel("Amplitude")
plt.title("Raw Waveform")
plt.tight_layout()
plt.savefig("staged/sayori/1_waveform.png")
plt.close()

# -----------------------
# 2. Compute spectrogram
# -----------------------
frequencies, times, spectrogram = scipy.signal.spectrogram(samples, nperseg=2048)

# Save full spectrogram (grayscale)
plt.figure(figsize=(8, 8))
plt.pcolormesh(times, frequencies, spectrogram, cmap="gray", shading="auto")
plt.yscale("log")
plt.xlabel("Time [s]")
plt.ylabel("Frequency [Hz]")
plt.title("Full Spectrogram")
plt.tight_layout()
plt.savefig("staged/sayori/2_spectrogram.png")
plt.close()

# -----------------------
# 3. Black-and-white thresholded
# -----------------------
freq_min = 0.21
freq_mask = frequencies >= freq_min
frequencies_bw = frequencies[freq_mask]
spectrogram_bw = spectrogram[freq_mask, :]

threshold = np.max(spectrogram_bw) * 0.01  # 1% of max
bw_spectrogram = np.where(spectrogram_bw > threshold, 1, 0)  # 1=white, 0=black

plt.figure(figsize=(8, 8))
plt.pcolormesh(times, frequencies_bw, bw_spectrogram, cmap="gray", shading="auto")
plt.yscale("log")
plt.xlabel("Time [s]")
plt.ylabel("Frequency [Hz]")
plt.title("Black-and-White Spectrogram")
plt.tight_layout()
plt.savefig("staged/sayori/3_bw_spectrogram.png")
plt.close()

# -----------------------
# 4. Inverted black-and-white
# -----------------------
inverted_bw_spectrogram = 1 - bw_spectrogram  # invert colors

plt.figure(figsize=(8, 8))
plt.pcolormesh(
    times, frequencies_bw, inverted_bw_spectrogram, cmap="gray", shading="auto"
)
plt.yscale("log")
plt.xlabel("Time [s]")
plt.ylabel("Frequency [Hz]")
plt.title("Inverted BW Spectrogram")
plt.tight_layout()
plt.savefig("staged/sayori/4_inverted_bw_spectrogram.png")

plt.figure(figsize=(8, 8))
plt.pcolormesh(
    times, frequencies_bw, inverted_bw_spectrogram, cmap="gray", shading="auto"
)
plt.yscale("log")
plt.axis("off")
plt.tight_layout()
plt.savefig(
    "staged/sayori/4_inverted_bw_spectrogram_noframe.png",
    bbox_inches="tight",
    pad_inches=0,
)
plt.close()

# -------------------------------
# 5. Read the saved inverted BW spectrogram while clipping to pixels
# -------------------------------

# TODO
