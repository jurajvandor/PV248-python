import wave
import numpy
import sys
import struct
#import matplotlib.pyplot as plt


def parse_wave(file):
    wav = wave.open(file, 'r')
    frames_per_sample = wav.getframerate()
    min = None
    max = None
    for i in range(0, int(wav.getnframes()/frames_per_sample)):
        frames = wav.readframes(frames_per_sample)
        decoded_frames = struct.unpack("%ih" % (frames_per_sample * wav.getnchannels()), frames)
        decoded_frames = numpy.array(decoded_frames)
        normalize = frames_per_sample
        if wav.getnchannels() == 2:
            decoded_frames = decoded_frames.reshape(-1, 2)
            decoded_frames = decoded_frames.sum(axis=1) / 2
            normalize = normalize * 2
        nq_freq = wav.getframerate()//2
        rfft_res = numpy.fft.rfft(decoded_frames) / normalize
        rfft_res = numpy.abs(rfft_res[:nq_freq])
        avg = numpy.average(rfft_res)
        freqes = numpy.fft.fftfreq(len(rfft_res)*2, 1 / wav.getframerate())[:nq_freq]
        for i, item in enumerate(rfft_res):
            if item > avg*20:
                if max is None or freqes[i] > max:
                    max = freqes[i]
                if min is None or freqes[i] < min:
                    min = freqes[i]
        #fig, ax1 = plt.subplots(1, figsize=(10, 5), sharex=True, sharey=True)
        #ax1.set_title('transformation')
        #ax1.set_xlim([0, nq_freq])
        #ax1.plot(freqes, rfft_res, 'b', lw=2)
        #ax1.plot(range(0, nq_freq), [avg*20]*nq_freq)
        #plt.tight_layout()
        #plt.show()
    if min is not None and max is not None:
        print("low = " + str(min) + ", high = " + str(max))
    else:
        print("no peaks")


parse_wave(sys.argv[1])