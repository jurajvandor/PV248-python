import pandas
import sys
import json


def column_name(column):
    if sys.argv[2] == "dates":
        return column[:-3]
    if sys.argv[2] == "exercises":
        return column[-2:]


def transform_dataframe(csv):
    dict_of_new_vectors = dict()
    for column in csv:
        if column == "student":
            continue
        if column_name(column) not in dict_of_new_vectors.keys():
            dict_of_new_vectors[column_name(column)] = csv[column]
        else:
            dict_of_new_vectors[column_name(column)] = dict_of_new_vectors.get(column_name(column)) + csv[column]
    data_frame = pandas.concat(dict_of_new_vectors, axis=1)
    return data_frame


def print_data(data_frame):
    mean = data_frame.mean()
    quantile_75 = data_frame.quantile(0.75)
    quantile_25 = data_frame.quantile(0.25)
    median = data_frame.quantile()
    non_zero_count = data_frame.astype(bool).sum(axis=0)
    d = dict()
    for i in mean.keys():
        column = dict()
        d[i] = column
        column["mean"] = mean[i]
        column["median"] = median[i]
        column["first"] = quantile_25[i]
        column["last"] = quantile_75[i]
        column["passed"] = int(non_zero_count[i])
    json.dump(d, sys.stdout, indent=4)


csv = pandas.read_csv(sys.argv[1])
if sys.argv[2] == "deadlines":
    csv = csv.drop("student", axis=1)
    print_data(csv)
else:
    print_data(transform_dataframe(csv))
