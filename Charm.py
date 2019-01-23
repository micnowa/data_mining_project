import os
from ItemsetOperations import *


def charm(file_name, minSup):
    if minSup < 1:
        return {}
    db = build_database(file_name)
    trans = transactional_database(db)
    if "null" in trans:
        del trans["null"]
    layers = []
    for i in range(get_longest_transaction_length(db)):
        if i is 0:
            layers.append(trans)
        else:
            layers.append(build_layer(layers[i - 1]))
        tmp = layers[i]
        for x in list(tmp):
            if len(tmp[x]) < minSup:
                del tmp[x]
        if i is not 0:
            layers[i - 1] = determine_closed_items(layers[i - 1], layers[i])
            print(layers[i-1])
            for key in layers[i-1]:
                layers[i-1][key] = len(layers[i-1][key])
    for key in layers[-1]:
        layers[-1][key] = len(layers[-1][key])
    return layers


file_name = input('Enter file name: ')
if os.path.exists(file_name):
    with open(file_name, 'r') as f:
        print("processing file ... " + file_name)
else:
    raise IOError("No such file")

minSup = input('Enter minimal support:   ')
if int(minSup) < 1:
    raise ValueError('Cannot process when minSup is less than 1')

print(charm(file_name, int(minSup)))
# A, B, C, D, E, F
# B, D, F
# A, C, E
# E, F, H
# A, E, I
# B, C, D, F
# A, E, F
# B, C, D, E