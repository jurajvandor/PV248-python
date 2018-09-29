import scorelib
import sys

prints = scorelib.load(sys.argv[1])
for p in prints:
    p.format()
    print()
