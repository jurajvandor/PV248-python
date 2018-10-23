import numpy
import re
import sys


def parse():
    file = open(sys.argv[1])
    variables = []
    list_of_lists = []
    other_side_of_eq = []
    length = 0
    for line in file:
        split = line.split(" ")
        list = [0]*length
        for i, ex in enumerate(split):
            if i+1 == len(split):
                other_side_of_eq.append(int(ex))
            res = re.match(r"([0-9]*)([a-zA-Z])", ex)
            if res is None:
                continue
            coefficient = int(res.group(1))
            variable = res.group(2)
            if i != 0 and split[i-1] == "-":
                coefficient *= -1
            if variable in variables:
                index = variables.index(variable)
                list[index] = coefficient
            else:
                list.append(coefficient)
                variables.append(variable)
                length += 1
                for l in list_of_lists:
                    l.append(0)
        list_of_lists.append(list)
    file.close()
    return list_of_lists, variables, other_side_of_eq



result = parse()

print(result[0])
print(result[1])
print(result[2])

