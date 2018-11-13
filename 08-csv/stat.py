import pandas
import sys


def parse():
    csv = pandas.read_csv(sys.argv[1])
    if sys.argv[2] == "dates":
        dic = dates(csv)
    if sys.argv[2] == "deadlines":
        dic = deadlines(csv)
    if sys.argv[2] == "exercises":
        dic = exercises(csv)


def dates(csv):
    dict_of_dates = dict()
    #for item in csv:
        #if item == "student":
            #continue
        #else:
            #dict_of_dates[item[:-3]] = pandas.DataFrame()
    for column in csv:
        if column == "student":
            continue
        #for row in csv[column]:
        #    dict_of_dates[column[:-3]] = dict_of_dates[column[:-3]].append({column[:-3]: row}, ignore_index=True)
        added = pandas.concat([pandas.DataFrame([row], columns=[column[:-3]]) for row in csv[column]], ignore_index=True)
        if column[:-3] not in dict_of_dates.keys():
            dict_of_dates[column[:-3]] = added
        else:
            dict_of_dates[column[:-3]] = pandas.concat([dict_of_dates[column[:-3]], added], ignore_index=True)
    data_frame = pandas.concat(dict_of_dates.values(), axis=1)
    data_frame = data_frame
    print(data_frame)


def deadlines(csv):
    pass


def exercises(csv):
    pass


parse()