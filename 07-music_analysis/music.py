import wave
import numpy
import sys
import struct


def parse_wave(file):
    wav = wave.open(file, 'r')
    frames = wav.readframes(wav.getnframes())
    decoded_frames = struct.unpack("%ih" % (wav.getnframes() * wav.getnchannels()), frames)
    decoded_frames = numpy.array(decoded_frames)
    if wav.getnchannels() == 2:
        decoded_frames = decoded_frames.reshape(-1, 2)
        decoded_frames = decoded_frames.sum(axis=1) / 2
    frames_per_sample = wav.getframerate()
    offset = 0
    step = wav.getframerate()//10
    last_result = ""
    segment_start = None
    while (offset*step + frames_per_sample) <= wav.getnframes():
        sample = decoded_frames[offset*step:(offset*step+frames_per_sample)]
        rfft_res = numpy.fft.rfft(sample) / frames_per_sample
        rfft_res = numpy.abs(rfft_res)
        avg = numpy.average(rfft_res)
        peaks = []
        cluser_start = None
        cluster = []
        for i, item in enumerate(rfft_res):
            if item > avg*20:
                cluster.append((i, item))
                cluser_start = i
            else:
                if cluser_start is not None:
                    sorted_cluster = sorted(cluster, key=(lambda a: a[1]), reverse=True)
                    tops = []
                    for it in sorted_cluster:
                        if it[1] == sorted_cluster[0][1]:
                            tops.append(it)
                    tops.sort(key=lambda a: a[0]-((cluser_start + i)//2))
                    peaks.append(tops[0])
                    cluster = []
                    cluser_start = None
        result = get_results(peaks)
        if last_result != "" and last_result != result:
            time = "{0:.1f}".format(segment_start / 10) + "-" + "{0:.1f}".format(offset / 10)
            print(time + " " + last_result)
            last_result = result
            if result != "":
                segment_start = offset
            else:
                segment_start = None
        if last_result == "" and result != "":
            last_result = result
            segment_start = offset
        offset += 1
    if last_result != "":
        time = "{0:.1f}".format(segment_start / 10) + "-" + "{0:.1f}".format(offset / 10)
        print(time + " " + last_result)
    wav.close()


def get_results(peaks):
    peaks.sort(key=lambda a: a[1], reverse=True)
    string = ""
    for i, freq in enumerate(peaks):
        if freq[0] == 0:
            continue
        if i == 3:
            break
        A4 = int(sys.argv[1])
        C0 = A4 * pow(2, -4.75)
        name = ["c", "cis", "d", "es", "e", "f", "fis", "g", "gis", "a", "bes", "b"]
        cap_name = ["C", "Cis", "D", "Es", "E", "F", "Fis", "G", "Gis", "A", "Bes", "B"]
        h = int(round(12 * numpy.log2(freq[0] / C0)))
        octave = int(h // 12)
        n = int(h % 12)
        a = pow(2, 1/12)
        c = 1200 * numpy.log2(freq[0]/(A4*pow(a, h-57)))
        if octave < 3:
            string += cap_name[n] + (2-octave)*","
        else:
            string += name[n] + (octave-3)*"'"
        if c >= 0:
            string += "+"
        string += str(int(round(c))) + "#" + str(freq) + " "
    return string.strip()


parse_wave(sys.argv[2])