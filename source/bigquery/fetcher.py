from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.client import GoogleCredentials
import sys
import os
import datetime

try:
    from source.helpers.db import execute, fetch
except:
    sys.path.append(
        os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
    from source.helpers.db import execute, fetch

PROJECT_ID = "javascript-module-quality"
credentials = GoogleCredentials.get_application_default()
bigquery_service = build('bigquery', 'v2', credentials=credentials)


def populate_events():
    repos = fetch('''SELECT repos.id, repos.github_id
                        FROM repos
                        LEFT OUTER JOIN events
                        ON repos.id = events.repo_id
                        GROUP BY repos.id;''')

    for r in repos:
        repo_id = r[0]
        github_id = r[1]

        events = _query_for_lib(github_id)

        for e in events:
            print(e)
            # execute('''
            #             INSERT INTO events
            #             VALUES (%s, %s, %s, %s);
            #         ''',
            #         (e['id'], e['type'], e['created_at'], repo_id)
            #         )

        break


def _query_for_lib(github_id):
    '''
    queries google big query for all events related to particular github repo in year 2015
    and in 2016 until august

    returns result in an array of dictionaries, each dictionary has 3 keys
    `id`, `date` and `type`.
    `type` is explain in readme file under `Event types` section
    '''
    result = []
    try:
        query_request = bigquery_service.jobs()
        query_data = {
            'query':
                '''
                SELECT id, type, created_at
                FROM [githubarchive:year.2015],
                        [githubarchive:month.201608],
                        [githubarchive:month.201607],
                        [githubarchive:month.201606],
                        [githubarchive:month.201605],
                        [githubarchive:month.201604],
                        [githubarchive:month.201603],
                        [githubarchive:month.201602],
                        [githubarchive:month.201601],
                WHERE repo.id = {};
                '''.format(github_id)
        }

        query_response = query_request.query(
            projectId=PROJECT_ID,
            body=query_data).execute()

        # [START print_results]
        print('Query Results:')
        for row in query_response['rows']:
            id = row['f'][0]['v']
            type = row['f'][1]['v']
            timestamp = row['f'][2]['v']
            result.append({
                "id": id,
                "date": datetime.datetime.fromtimestamp(float(timestamp)),
                "type": type
            })

    except HttpError as err:
        print('Error: {}'.format(err.content))
        raise err

    return result


if __name__ == '__main__':
    populate_events()
