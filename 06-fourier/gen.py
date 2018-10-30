import numpy as np
import scipy.io.wavfile as wf

sr = 44100    # sample rate
len_sig = 2   # length of resulting signal in seconds

f = 1000      # frequency in Hz

# set you time axis
t = np.linspace(0, len_sig, sr*len_sig)

# set your signal
mono_data = np.sin(2*np.pi*t*f)

# write single channel .wav file
wf.write('mono.wav', sr, mono_data)

# write two-channel .wav file
stereo_data = np.vstack((mono_data, mono_data)).T
wf.write('stereo.wav', sr, stereo_data)