import wave
import numpy
import sys
import struct
import matplotlib.pyplot as plt


def parse_wave(file):
    wav = wave.open(file, 'r')

    frames_per_sample = wav.getframerate()
    print(frames_per_sample)
    print(wav.getnframes()/frames_per_sample)
    min = None
    max = None
    for i in range(0, int(wav.getnframes()/frames_per_sample)):
        frames = wav.readframes(frames_per_sample)
        decoded_frames = struct.unpack("%ih" % (frames_per_sample * wav.getnchannels()), frames)
        decoded_frames = numpy.array(decoded_frames)
        normalize = frames_per_sample
        if wav.getnchannels() == 2:
            print("stereo")
            decoded_frames = decoded_frames.reshape(-1, 2)
            decoded_frames = decoded_frames.sum(axis=1) / 2
            normalize = normalize * 2
        nq_freq = wav.getframerate()//2
        print(nq_freq)
        rfft_res = numpy.fft.rfft(decoded_frames) / normalize
        rfft_res = numpy.abs(rfft_res[:nq_freq])
        avg = numpy.average(rfft_res)
        freqes = numpy.fft.fftfreq(len(rfft_res)*2, 1 / wav.getframerate())[:nq_freq]
        print("freq")
        print(rfft_res)
        print(freqes)
        print(freqes[numpy.argmax(rfft_res)])
        for i, item in enumerate(rfft_res):
            if item > avg*20:
                print(item)
                if freqes[i] > min
                print(freqes[i])
        #fig, ax1 = plt.subplots(1, figsize=(10, 5), sharex=True, sharey=True)
        #ax1.set_title('mono signal')
        #ax1.set_xlim([0, 2050])
        #ax1.plot(freqes, rfft_res, 'b', lw=2)
        #plt.tight_layout()
        #plt.show()


parse_wave(sys.argv[1])