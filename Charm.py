def lcs(str1, str2):  # Creates common part of two strings
    s = set(str1)
    t = set(str2)
    intersect = s & t  # or s.intersection(t)
    value = ""
    for val in intersect:
        value += val
    return value


def string_contains(str1, str2):  # checks if str1 contains all characters of str2
    for x in str2:
        if x not in str1:
            return False
    return True


def tid_from_file(file_name):  # returns list of transaction identifiers in given bd
    file = open(file_name, "r")
    tid = []
    for line in file:
        tid.append(ord(line[0]) - 48)
    return tid


def build_database(file_name):  # Creates database from file
    file = open(file_name, "r")
    table = {}
    for line in file:
        tid = line[0]
        line = line[3:]
        table[tid] = ""
        for character in line:
            if character.isalpha():
                table[tid] = table[tid] + character
    return table


def first_layer_item_support(file_name):  # returns item sets of length 1 from db in file
    file = open(file_name, "r")
    items = {}
    for line in file:
        line = line[3:]
        for character in line:
            if character.isalpha():
                if character in items:
                    items[character] += 1
                else:
                    items[character] = 1
    return items


def transactional_database(table):  # Coverts database into transactional database
    trans_db = {"null": ""}
    for i in table:
        trans_db["null"] = trans_db["null"] + i
        for element in table[i]:
            if element not in trans_db:
                trans_db[element] = ""
            trans_db[element] = trans_db[element] + i
    return trans_db


def equal_string(str1, str2):
    return len(str1) == len(str2) and sorted(str1) == sorted(str2)


def build_next_layer(trans_db):
    layer = {}
    if "null" in trans_db:
        del trans_db["null"]
    used_elements = []
    for x in trans_db:
        for y in trans_db:
            if len(x) == 1 and len(y) == 1:
                if x != y and y not in used_elements:
                    item = merge_items_with_no_tid(x, y)
                    layer[item] = lcs(trans_db[x], trans_db[y])
            else:
                if equal_string(x, y) is False:  # nie mogą być takie same
                    if any(s in x for s in y):  # muszą mieć wspólny element
                        candidate = merge_items_with_no_tid(x, y)
                        keys = list(layer.keys())
                        value = True
                        for key in keys:
                            if equal_string(candidate, key):
                                value = False
                        if value is not False:
                            item = candidate
                            layer[item] = lcs(trans_db[x], trans_db[y])
    used_elements.append(x)
    return layer


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


def count_item_support(item):
    for x in item:
        return len(item[x])


database = build_database("test.txt")
print(database)

tid = tid_from_file("test.txt")
print("________________")
print(tid)
print("________________")

db = transactional_database(database)

print(build_next_layer(transactional_database(database)))
print(build_next_layer(build_next_layer(transactional_database(database))))
print(build_next_layer(build_next_layer(build_next_layer(transactional_database(database)))))
print(build_next_layer(build_next_layer(build_next_layer(build_next_layer(transactional_database(database))))))
print(build_next_layer(build_next_layer(build_next_layer(build_next_layer(build_next_layer(transactional_database(database)))))))
print(build_next_layer(build_next_layer(build_next_layer(build_next_layer(build_next_layer(transactional_database(database)))))))

print(merge_items({"BC": "168"}, {"CD": "168"}, database))

print(lcs("bca", "abcefa"))
