def lcs(str1, str2):  # Creates common part of two strings
    s = set(str1)
    t = set(str2)
    intersect = s & t  # or s.intersection(t)
    value = ""
    for val in intersect:
        value += val
    return value


def get_common_transactions(trans1, trans2):
    tab = []
    for x in trans1:
        if x in trans2:
            tab.append(x)
    return tab


def string_contains(str1, str2):  # checks if str1 contains all characters of str2
    for x in str2:
        if x not in str1:
            return False
    return True


def file_len(file_name):
    with open(file_name) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def tid_from_file(file_name):  # returns list of transaction identifiers in given bd
    transactions_id = []
    num = file_len(file_name)
    for line in range(num):
        transactions_id.append(line + 1)
    return transactions_id


def equal_string(str1, str2):
    return len(str1) == len(str2) and sorted(str1) == sorted(str2)


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


def merge_items(items1, items2, regular_db):
    key = ""
    value = ""
    for x in items1:
        key = x
    for x in items2:
        for sub in x:
            if sub not in key:
                key += sub
    for tid in regular_db:
        if string_contains(regular_db[tid], key):
            value += tid
    return {key: value}


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
    return layers


print(charm("test.txt", 2))
# A, B, C, D, E, F
# B, D, F
# A, C, E
# E, F, H
# A, E, I
# B, C, D, F
# A, E, F
# B, C, D, E
