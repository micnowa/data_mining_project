def lcs(str1, str2):
    m = len(str1)
    n = len(str2)
    counter = [[0] * (n + 1) for x in range(m + 1)]
    longest = 0
    lcs_set = set()
    for i in range(m):
        for j in range(n):
            if str1[i] == str2[j]:
                c = counter[i][j] + 1
                counter[i + 1][j + 1] = c
                if c > longest:
                    lcs_set = set()
                    longest = c
                    lcs_set.add(str1[i - c + 1:i + 1])
                elif c == longest:
                    lcs_set.add(str1[i - c + 1:i + 1])

    string = ""
    for x in lcs_set:
        string += x

    return string


def file_len(file_name):
    with open(file_name) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def tid_from_file(file_name):
    file = open(file_name, "r")
    tid = []
    for line in file:
        tid.append(ord(line[0]) - 48)
    return tid


def first_layer_item_support(file_name):
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


def build_database(file_name):
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


def transactional_database(table):
    trans_db = {"null": ""}
    for i in table:
        trans_db["null"] = trans_db["null"] + i
        print(i)
        for element in table[i]:
            if element not in trans_db:
                trans_db[element] = ""
            trans_db[element] = trans_db[element] + i
    print(trans_db)
    return trans_db


def build_layer(trans):
    layer = {}
    if "null" in trans:
        del trans["null"]
    used_elements = []
    for x in trans:
        for y in trans:
            if x != y and y not in used_elements:
                layer[x+y] = lcs(trans[x], trans[y])
        used_elements.append(x)

    return layer


database = build_database("test.txt")
print(database)

tid = tid_from_file("test.txt")
print(tid)

db = transactional_database(database)

print(build_layer(transactional_database(database)))
