import re

def lcs(str1, str2):  # Creates common part of two strings
    s = set(str1)
    t = set(str2)
    intersect = s & t
    value = ""
    for val in intersect:
        value += val
    return value


def string_contains(str1, str2):  # checks if str1 contains all characters of str2
    for x in str2:
        if x not in str1:
            return False
    return True


def file_len(file_name):  # Returns number of lines in file
    with open(file_name) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def equal_string(str1, str2):
    return len(str1) == len(str2) and sorted(str1) == sorted(str2)


def tid_from_file(file_name):  # returns list of transaction identifiers in given bd
    transactions_id = []
    num = file_len(file_name)
    for line in range(num):
        transactions_id.append(line + 1)
    return transactions_id

def delete_subset(superset,subset):
    return re.sub('[' + subset + ']', '', superset)
