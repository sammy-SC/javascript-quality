# https://github.com/npm/download-counts
import json
import sys
import os
import http.client

try:
    from source.helpers.db import fetch, execute
except:
    sys.path.append(
        os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
    from source.helpers.db import fetch, execute


def parseJSON(string):
    return json.loads(string.decode('utf-8'))


repos = fetch('''SELECT repos.id, repos.name
                    FROM repos
                    LEFT OUTER JOIN downloads
                    ON repos.id = downloads.repo_id
                    GROUP BY repos.id;''')

# https://api.npmjs.org/downloads/range/2014-01-01:2016-08-02/jquery
counter = 0
for r in repos:
    print("")
    try:
        con = http.client.HTTPSConnection("api.npmjs.org")
        con.request("GET", "/downloads/range/2015-01-01:2016-08-01/{}".format(r[1]))
        r1 = con.getresponse()
        data = json.loads(r1.read().decode('UTF-8'))

        for e in data['downloads']:
            execute('''INSERT INTO downloads
                (day, count, repo_id)
                VALUES (%s, %s, %s);
                ''', (e['day'], e['downloads'], r[0]))
    except:
        print("Unexpected error: ", sys.exc_info())
        print("for package: ", r)
        continue
