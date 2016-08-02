import fetch_all
import http.client
import json
import sys
import os

try:
    from source.helpers.db import execute
except:
    sys.path.append(
        os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
    from source.helpers.db import execute


def fetch_individual():
    counter = 0
    all_data = fetch_all.load_data()

    for e in all_data:
        try:
            con = http.client.HTTPConnection("registry.npmjs.org")
            con.request("GET", "/{}".format(e['name']))
            r1 = con.getresponse()
            data = json.loads(r1.read().decode('UTF-8'))

            latest_tag = data['dist-tags']['latest']
            latest = data['versions'][latest_tag]

            dependencies_counter = len(latest.get('dependencies', {}).keys())
            mainteiners_counter = len(latest.get('maintainers', []))
            contributors_counter = len(latest.get('contributors', []))
            has_tests = latest.get('scripts', {}).get('test') is not None
            has_readme = data.get('readmeFilename') is not None

            execute('''
                UPDATE repos SET dependencies_count=(%s),
                mainteiners_count=(%s),
                contributors_count=(%s),
                has_tests=(%s),
                has_readme=(%s)
                WHERE
                name=(%s);
                ''', (dependencies_counter, mainteiners_counter,
                      contributors_counter, has_tests, has_readme, e['name']))

            counter += 1
            print("{} / {}".format(counter, len(all_data)), end='\r')
        except:
            print("Unexpected error: ", sys.exc_info())
            continue


if __name__ == '__main__':
    fetch_individual()
