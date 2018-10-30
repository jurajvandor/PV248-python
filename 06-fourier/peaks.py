import wave
import numpy
import sys
import struct

import matplotlib.pyplot as plt

def parse_wave(file):
    wav = wave.open(file, 'r')

    frames_per_sample = int(wav.getframerate()*2)
    print(frames_per_sample)
    print(wav.getnframes()/frames_per_sample)
    for i in range(0, int(wav.getnframes()/frames_per_sample)):
        frames = wav.readframes(frames_per_sample)
        decoded_frames = struct.unpack("%ih" % (frames_per_sample * wav.getnchannels()), frames)
        decoded_frames = numpy.array(decoded_frames)
        if wav.getnchannels() == 2:
            decoded_frames = decoded_frames.reshape(-1, 2)
            decoded_frames = decoded_frames.sum(axis=1) / 2
        #print(decoded_frames)
        rfft_res = numpy.fft.rfft(decoded_frames) / len(decoded_frames)
        rfft_res = numpy.abs(rfft_res[:(wav.getframerate()//2)])
        avg = numpy.average(rfft_res)
        freqes = numpy.fft.fftfreq(len(rfft_res), 1 / wav.getframerate())[:(wav.getframerate()//2)]
        print("freq")
        print(freqes)
        print(freqes[numpy.argmax(rfft_res)])
        for item in rfft_res:
            if (item > avg*20):
                print(item)
                print(freqes[1330])
        #fig, (ax1, ax2) = plt.subplots(2, figsize=(10, 5), sharex=True, sharey=True)
        #ax1.set_title('mono signal')
        #ax1.set_xlim([0, 8000])
        #ax1.plot(freqes, rfft_res, 'b', lw=2)
        #plt.tight_layout()
        #plt.show()
        #avg = numpy.average(rfft_res)
        #print(rfft_res)
        #print(avg)
        #x = None
        #for data in rfft_res:
         #   if data > 20*avg:
          #      if x is None or data > x:
           #         x = data
    #print(x)

parse_wave(sys.argv[1])