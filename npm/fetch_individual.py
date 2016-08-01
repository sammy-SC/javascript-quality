import fetch_all
import http.client
import pprint
import json
import sys

data = {}
counter = 0
all_data = fetch_all.load_data()
for e in all_data:
    con = http.client.HTTPConnection("registry.npmjs.org")
    con.request("GET", "/{}".format(e['name']))
    r1 = con.getresponse()
    data = json.loads(r1.read().decode('UTF-8'))

    try:
        latest_tag = data['dist-tags']['latest']
        latest = data['versions'][latest_tag]

        dependencies_counter = len(latest.get('dependencies', {}).keys())
        mainteiners_counter = len(latest['maintainers'])
        contributors_counter = len(latest.get('contributors', []))
        has_tests = latest.get('scripts', {}).get('test') is not None
        has_readme = data.get('readmeFilename') is not None

        data[e['name']] = {
            'dependencies_counter': dependencies_counter,
            'mainteiners_counter': mainteiners_counter,
            'contributors_counter': contributors_counter,
            'has_tests': has_tests,
            'has_readme': has_readme,
        }

        counter += 1
        print("{} / {}".format(counter, len(all_data)), end='\r')

    except:
        print("Unexpected error: ", sys.exc_info())
        continue

file = open('../data/npm-invidivual.pickled', 'wb')
pickle.dump(data, file, pickle.HIGHEST_PROTOCOL)
