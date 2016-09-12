import MySQLdb
from source.helpers.db import fetch, execute

conn = MySQLdb.connect('127.0.0.1', user='ght', db='ghtorrent')


def fetch_ghtorrent(query, parameters=None):
    '''
    Returns cursor which can be iterated.
    Don't forget to call .close on the cursor after done with it
    '''
    cur = conn.cursor()
    cur.execute(query, parameters)
    return cur

# def fetch_repos():
#     cur = fetch_ghtorrent((
#         'SELECT created_at '
#         'FROM commits '
#         'WHERE project_id '
#     ))


def insert_commit(id, repo_id, created_at):
    execute((
        'INSERT INTO commits '
        '(id, repo_id, date) '
        'VALUES (%s, %s, %s)'
    ), (id, repo_id, created_at))


def fetch_repos(repo, owner):
    url = 'https://api.github.com/repos/{}/{}'.format(owner, repo)
    cur = fetch_ghtorrent((
        'SELECT commits.id, commits.created_at '
        'FROM commits '
        'JOIN projects '
        'ON projects.id = commits.project_id '
        'WHERE projects.url=%s'
    ), (url,))

    return cur


cursor = fetch((
    'SELECT repos.id, name, owner '
    'FROM repos '
    'LEFT JOIN commits '
    'ON repos.id=commits.repo_id '
    'WHERE commits.id is NULL'
))


for i, repo in enumerate(cursor):
    print('Fetching commits from ghtorrent: {} / {}'.format(i, cursor.rowcount))

    commits_cursor = fetch_repos(repo[1], repo[2])

    print('Inserting: {} commits'.format(commits_cursor.rowcount))

    for c in commits_cursor:
        try:
            insert_commit(c[0], repo[0], c[1])
        except:
            print('There was an error inserting commits for repo with id: {}'.format(repo[0]))

    commits_cursor.close()


cursor.close()
