import sys
import re
from collections import Counter


def readfile():
    f = open(sys.argv[1], 'r')
    if sys.argv[2] == 'composer':
        composer(f)
    if sys.argv[2] == 'century':
        century(f)
    f.close()


def composer(f):
    ctr = Counter()
    for line in f:
        r = re.compile(r"Composer: (.*)")
        res = r.match(line)
        if res is not None:
            res2 = res.group(1).split(";")
            for item in res2:
                res3 = re.sub(r'\([^)]*\)', '', item)
                ctr[res3.strip()] += 1
    ctr.pop('')
    for k,v in ctr.items():
        print(k + ': ' + str(v))


def century(f):
    ctr = Counter()
    for line in f:
        r = re.compile(r"Composition Year: (.*)")
        res = r.match(line)
        if res is not None:
            res2 = re.match(".*([1-2][0-9]{3})", res.group(1).strip())
            if res2 is not None:
                century = int(res2.group(1))/100 + 1
                ctr[int(century)] += 1
            else:
                res3 = re.match(".*([0-9]{2})th century(.*)", res.group(1))
                if res3 is not None:
                    ctr[int(res3.group(1))] += 1
    for k,v in ctr.items():
        print(str(k) + 'th century: ' + str(v))


readfile()
