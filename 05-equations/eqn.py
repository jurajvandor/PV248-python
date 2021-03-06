import numpy
import re
import sys
import collections


def parse():
    file = open(sys.argv[1], 'r')
    variables = []
    list_of_lists = []
    other_side_of_eq = []
    length = 0
    for line in file:
        line = line.strip()
        if line == "":
            continue
        split = line.split(" ")
        lst = [0]*length
        split = list(filter(lambda a: a != '', split))
        for i, ex in enumerate(split):
            if i+1 == len(split):
                other_side_of_eq.append(int(ex))
            res = re.match(r"([0-9]*)([a-z])", ex)
            if res is None:
                continue
            if res.group(1) != "":
                coefficient = int(res.group(1))
            else:
                coefficient = 1
            variable = res.group(2)
            if i != 0 and split[i-1] == "-":
                coefficient *= -1
            if variable in variables:
                index = variables.index(variable)
                lst[index] = coefficient
            else:
                lst.append(coefficient)
                variables.append(variable)
                length += 1
                for l in list_of_lists:
                    l.append(0)
        list_of_lists.append(lst)
    file.close()
    return list_of_lists, variables, other_side_of_eq


def compute(parsed_lists):
    matrix = numpy.array(parsed_lists[0])
    list_of_constants = numpy.array(parsed_lists[2])
    rank_matrix = numpy.linalg.matrix_rank(matrix)
    augumented_matrix = numpy.hstack((matrix, numpy.expand_dims(list_of_constants, axis=1)))
    rank_augumented_matrix = numpy.linalg.matrix_rank(augumented_matrix)
    if rank_augumented_matrix != rank_matrix:
        print("no solution")
        return
    if len(parsed_lists[1]) != rank_augumented_matrix:
        print("solution space dimension: " + str(abs(len(parsed_lists[1]) - rank_augumented_matrix)))
        return
    result = numpy.linalg.solve(matrix, list_of_constants)
    d = dict(zip(parsed_lists[1], result))
    ordered_dict = collections.OrderedDict(sorted(d.items()))
    s = "solution: "
    for variable, value in ordered_dict.items():
        s += variable + " = " + str(value) + ", "
    print(s[:-2])


compute(parse())
