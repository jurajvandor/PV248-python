import pandas
import sys
import json
import numpy
import datetime


def column_name(column, type):
    if type == "dates":
        return column[:-3]
    if type == "exercises":
        return column[-2:]
    
    
def dict_of_values(stud, type):
    dict_values = dict()
    for key in stud.keys():
        if column_name(key, type) not in dict_values.keys():
            dict_values[column_name(key, type)] = stud[key]
        else:
            dict_values[column_name(key, type)] = dict_values.get(column_name(key, type)) + stud[key]
    return dict_values
    
    
def print_json(stud):
    dict_exercises = dict_of_values(stud, "exercises")
    json_dict = dict()
    json_dict["mean"] = numpy.mean(list(dict_exercises.values()))
    json_dict["median"] = numpy.median(list(dict_exercises.values()))
    json_dict["total"] = float(numpy.sum(list(dict_exercises.values())))
    json_dict["passed"] = int(numpy.sum(numpy.array(list(dict_exercises.values())).astype(bool)))
    dict_dates = dict_of_values(stud, "dates")
    dates = numpy.array([int(datetime.datetime(int(key[0:4]), int(key[5:7]), int(key[8:10])).timestamp()//(60*60*24)) for key in dict_dates.keys()])
    delta = datetime.datetime(2018, 9, 17).timestamp() // (60 * 60 * 24)
    dates = dates - delta
    cumulated_points = numpy.cumsum(numpy.array([dict_dates[key] for key in dict_dates.keys()]))
    dates = numpy.vstack([dates, numpy.zeros(len(dates))]).T
    m, c = numpy.linalg.lstsq(dates, cumulated_points, rcond=None)[0]
    json_dict["regression slope"] = m
    result = numpy.linalg.solve([[m]], [c+16])
    json_dict["date 16"] = str(datetime.datetime.fromtimestamp((result+delta)*60*60*24))[0:10]
    result = numpy.linalg.solve([[m]], [c+20])
    json_dict["date 20"] = str(datetime.datetime.fromtimestamp((result+delta)*60*60*24))[0:10]
    json.dump(json_dict, sys.stdout, indent=4)


csv = pandas.read_csv(sys.argv[1])
if sys.argv[2] != "average":
    csv = csv.set_index("student")
    stud = csv.loc[int(sys.argv[2])]
    print_json(stud)
else:
    csv = csv.drop("student", axis=1)
    print_json(csv.mean())
