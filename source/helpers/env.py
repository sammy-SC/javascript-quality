import json
import os.path


def env(key, default=None):
    if not os.path.isfile('environment.json'):
        return default

    f = open('environment.json')
    data = json.load(f)
    splitted = key.split('.')
    temp = data
    for k in splitted:
        temp = temp.get(k)

    return temp or default
