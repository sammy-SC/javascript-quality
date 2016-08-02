import json

f = open('environment.json')
data = json.load(f)


def env(key, default=None):
    splitted = key.split('.')
    temp = data
    for k in splitted:
        temp = temp.get(k)

    return temp or default
