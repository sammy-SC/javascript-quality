'''
script loads general info about all packages and then starts to
request more data about individual packages from npm. Results are saved into DB
'''
import http.client
import json
import sys
import os

try:
    from source.helpers.db import execute, fetch
except:
    sys.path.append(
        os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
    from source.helpers.db import execute, fetch


def _load_it():
    return fetch('SELECT name FROM repos WHERE has_tests is null ORDER BY id DESC;')


def _get_count():
    cur = fetch('SELECT COUNT(*) FROM repos WHERE has_tests is null;')
    return cur.fetchone()[0]


def fetch_individual():
    '''
    fetches individual info about packages and saves result into DB
    '''
    counter = 0
    all_data = _load_it()
    total = _get_count()

    for e in all_data:
        name = e[0]
        counter += 1
        print("{} / {}".format(counter, total))

        try:
            con = http.client.HTTPConnection("registry.npmjs.org")
            con.request("GET", "/{}".format(name))
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
                      contributors_counter, has_tests, has_readme, name))

        except:
            print("Unexpected error: ", sys.exc_info())
            print("for package: ", name)
            continue


if __name__ == '__main__':
    fetch_individual()
