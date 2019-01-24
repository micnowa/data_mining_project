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
            for key in layers[i-1]:
                layers[i-1][key] = len(layers[i-1][key])
    for key in layers[-1]:
        layers[-1][key] = len(layers[-1][key])
    return layers


def closed_to_frequent(layers):
    k = len(layers) - 1
    for k in range(k,0,-1):
        for key, value in layers[k].items():
           Itemset_subsets = subsets(key)
           itemsetSupport = value
           for subset in Itemset_subsets:
               subIndex = len(subset) - 1
               if subset not in layers[subIndex]:
                   layers[subIndex][subset] = itemsetSupport
    return layers


def Apriori(itemset, minConf = 0.7):
    supportData = calcSupport(itemset,file_name)
    Rules = []
    for i in range(1, len(itemset)):
        for freqSet in itemset[i]:
            H1 = [item for item in freqSet]
            if (i > 1):
                rulesFromConseq(freqSet, H1, supportData, Rules, minConf)
            else:
                calcConf(freqSet, H1, supportData, Rules, minConf)
    return Rules



file_name = input('Enter file name: ')
if os.path.exists(file_name):
    with open(file_name, 'r') as f:
        print("processing file ... " + file_name)
else:
    raise IOError("No such file")

minSup = input('Enter minimal support:   ')
if int(minSup) < 1:
    raise ValueError('Cannot process when minSup is less than 1')


closed_itemsets = charm(file_name, int(minSup))
print("Closed itemsets:")
print(closed_itemsets,"\n")
print("*"*80)



frequent_itemsets = closed_to_frequent(closed_itemsets)
print("Frequent itemsets:")
print(frequent_itemsets,"\n")
print("*"*80)


print("Association rules:")
rules = Apriori(frequent_itemsets, minConf = 0.4)



