from FileStringOperations import *


def get_common_transactions(trans1, trans2):
    tab = []
    for x in trans1:
        if x in trans2:
            tab.append(x)
    return tab


def get_longest_transaction_length(db):
    length = 0
    for item in db:
        length_candidate = len(db[item])
        if length_candidate > length:
            length = length_candidate
    return length


def build_database(file_name):  # Creates database from file
    file = open(file_name, "r")
    table = {}
    trans_id = 0
    for line in file:
        trans_id += 1
        line = line[0:]
        table[str(trans_id)] = ""
        for character in line:
            if character.isalpha():
                table[str(trans_id)] = table[str(trans_id)] + character
    return table


def transactional_database(database):  # Coverts database into transactional database
    trans_db = {"null": []}
    for i in database:
        trans_db["null"].append(i)
        for element in database[i]:
            if element not in trans_db:
                trans_db[element] = []
            trans_db[element].append(i)
    return trans_db


def build_layer(trans_db):
    layer = {}
    if "null" in trans_db:
        del trans_db["null"]
    used_elements = []
    for x in trans_db:
        for y in trans_db:
            value = False
            candidate = merge_items_with_no_tid(x, y)
            if len(x) == 1 and len(y) == 1:
                if x != y and y not in used_elements:
                    value = True
                else:
                    value = False
            else:
                if equal_string(x, y) is False:
                    if any(s in x for s in y):
                        keys = list(layer.keys())
                        value = True
                        for key in keys:
                            if equal_string(candidate, key):
                                value = False
            if value is True:
                layer[candidate] = get_common_transactions(trans_db[x], trans_db[y])
        used_elements.append(x)
    return layer


def remove_infrequent_items(trans_db, minimal_support):
    new_database = {}
    for x in trans_db:
        if len(trans_db[x]) >= minimal_support:
            new_database[x] = trans_db[x]
    return new_database


def merge_items_with_no_tid(items1, items2):
    key = ""
    for x in items1:
        key += x
    for y in items2:
        if y not in key:
            key += y
    return key


def determine_closed_items(items1, items2):
    if "null" in items1:
        del items1["null"]
    closed_items = {}
    closed = True
    for x in items1:
        for y in items2:
            if string_contains(y, x):
                if str(len(items2[y])) == str(len(items1[x])):
                    closed = False
                    continue
        if closed is True:
            closed_items[x] = items1[x]
        closed = True
    return closed_items

#---------Closed to Frequent

def subsets(itemset):
    subs = []
    for i in itemset:
        subs.append(str(i))
    k = len(subs)
    if k > 2:
        for i in range(k - 1):
            for j in range(k - 1 - i):
                temp = ""
                temp = str(subs[i]) + str(subs[i + j + 1])
                subs.append(temp)
    return subs

#-----------Apriori

def calcSupport(itemset,file_name):
    numItems = file_len(file_name)
    supportSet = {}
    for i in range(len(itemset)):
        for key, value  in itemset[i].items():
            supportSet[key] = value/numItems
    return supportSet


def apriori_Gen(Lk, k): #creates Ck
    Ck = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i+1, lenLk):
            L1 = list(Lk[i])[:k-2]; L2 = list(Lk[j])[:k-2]
            L1.sort(); L2.sort()
            if L1==L2:
                Ck.append(Lk[i] + Lk[j])
    return Ck





def calcConf(freqSet, H, supportData, rules, minConf=0.7):
    Hn = []
    for Hi in H:
        confidence = supportData[freqSet]/supportData[delete_subset(freqSet,Hi)]  #calc confidence
        if confidence >= minConf:
            print (delete_subset(freqSet,Hi),'-->',Hi,'confidence:',confidence)
            rules.append((delete_subset(freqSet,Hi), "," ,Hi, Hi, confidence))
            Hn.append(Hi)
    return H


def rulesFromConseq(freqSet, H, supportData, rules, minConf=0.7):
    m = len(H[0])
    if (len(freqSet) > (m + 1)):
        Hmp1 = apriori_Gen(H, m+1)
        Hmp1 = calcConf(freqSet, Hmp1, supportData, rules, minConf)
        if (len(Hmp1) > 1):
            rulesFromConseq(freqSet, Hmp1, supportData, rules, minConf)

