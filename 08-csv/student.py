import pandas
import sys
import json
import numpy
import time
import datetime


def print_json(stud):
    dict_exercises = dict()
    for key in stud.keys():
        if key[-2:] not in dict_exercises.keys():
            dict_exercises[key[-2:]] = stud[key]
        else:
            dict_exercises[key[-2:]] = dict_exercises.get(key[-2:]) + stud[key]
    json_dict = dict()
    json_dict["mean"] = numpy.mean(list(dict_exercises.values()))
    json_dict["median"] = numpy.median(list(dict_exercises.values()))
    json_dict["total"] = float(numpy.sum(list(dict_exercises.values())))
    json_dict["passed"] = int(numpy.sum(numpy.array(list(dict_exercises.values())).astype(bool)))

    dict_dates = dict()
    for key in stud.keys():
        if key[:-3] not in dict_dates.keys():
            dict_dates[key[:-3]] = stud[key]
        else:
            dict_dates[key[:-3]] = dict_dates.get(key[:-3]) + stud[key]
    dates = numpy.array([int(datetime.datetime(int(key[0:4]), int(key[5:7]), int(key[8:10])).timestamp()//(60*60*24)-17799) for key in dict_dates.keys()])
    print(dates[1])
    cumulated_points = numpy.cumsum(numpy.array([dict_dates[key] for key in dict_dates.keys()]))
    dates = numpy.vstack([dates, numpy.ones(len(dates))]).T
    print(dates)
    print(cumulated_points)
    m, c = numpy.linalg.lstsq(dates, cumulated_points, rcond=None)[0]
    json_dict["regression slope"] = m
    print(c)
    result = numpy.linalg.solve([[m]], [c+20])
    json_dict["date 20"] = str(datetime.datetime.fromtimestamp((result+17799)*60*60*24))[0:10]
    result = numpy.linalg.solve([[m]], [c+16])
    json_dict["date 16"] = str(datetime.datetime.fromtimestamp((result+17799)*60*60*24))[0:10]
    json.dump(json_dict, sys.stdout, indent=4)


csv = pandas.read_csv(sys.argv[1])
if sys.argv[2] != "average":
    csv = csv.set_index("student")
    stud = csv.loc[int(sys.argv[2])]
    print_json(stud)
else:
    csv = csv.drop("student", axis=1)
    print_json(csv.mean())
