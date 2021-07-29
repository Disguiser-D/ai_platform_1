import os


def search_log():
    res = []
    for root, dirs, files in os.walk('log'):
        for name in files:
            res.append(name)
    return res
