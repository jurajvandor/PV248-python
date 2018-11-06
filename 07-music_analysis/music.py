import wave
import numpy
import sys
import struct


def parse_wave(file):
    pitches = {440: "a'", 220: "a"}
    wav = wave.open(file, 'r')
    frames_per_sample = wav.getframerate()
    for i in range(0, int(wav.getnframes()/frames_per_sample)):
        frames = wav.readframes(frames_per_sample)
        decoded_frames = struct.unpack("%ih" % (frames_per_sample * wav.getnchannels()), frames)
        decoded_frames = numpy.array(decoded_frames)
        if wav.getnchannels() == 2:
            decoded_frames = decoded_frames.reshape(-1, 2)
            decoded_frames = decoded_frames.sum(axis=1) / 2
        rfft_res = numpy.fft.rfft(decoded_frames) / frames_per_sample
        rfft_res = numpy.abs(rfft_res)
        avg = numpy.average(rfft_res)
        peaks = []
        last_was_peak = False
        cluster = []
        for i, item in enumerate(rfft_res):
            if item > avg*20:
                cluster.append((i, item))
                last_was_peak = True
            else:
                if last_was_peak:
                    sorted_cluster = sorted(cluster, key=(lambda a: a[1]), reverse=True)
                    last_was_peak = False
                    #add choosing middle one
                    peaks.append(sorted_cluster[0])
                    #print(cluster)
                    cluster = []
        print(peaks)
        peaks.sort(key=lambda a: a[1])
    wav.close()


parse_wave(sys.argv[1])