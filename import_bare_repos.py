'''
- fetches all repos without commits from database
- loads bare repo from github
- extracts commit data from it and saves it into database
- deletes bare repo
'''
import source.helpers.db as db
from git import Repo
import os
import shutil
from datetime import datetime


dir_path = os.path.dirname(os.path.realpath(__file__))


def get_target_path(owner, name):
    return 'bare_repos/{}/{}.git'.format(owner, name)


def insert_into_db(repo_id, owner, name):
    target_path = get_target_path(owner, name)
    path = os.path.join(dir_path, target_path)
    repo = Repo.init(path, bare=True)

    conn = db.get_connection()

    try:
        for c in repo.iter_commits('master'):
            message = c.message
            timestamp = datetime.fromtimestamp(c.committed_date)
            db.execute_without_commit((
                'INSERT INTO commits '
                '(repo_id, date, message) '
                'VALUES (%s, %s, %s)'
            ), (repo_id, timestamp, message))
    except:
        print('failed to checkout master for: {}/{}'.format(owner, name))

    conn.commit()


cursor = db.fetch((
    'SELECT repos.id, name, owner '
    'FROM repos '
    'LEFT JOIN commits '
    'ON repos.id=commits.repo_id '
    'WHERE commits.id is NULL'
))


for i, r in enumerate(cursor):
    print('Progress: {} / {}'.format(i, cursor.rowcount))
    repo_id = r[0]
    name = r[1]
    owner = r[2]
    url = "git@github.com:{}/{}".format(owner, name)

    target_path = get_target_path(owner, name)

    if os.path.isdir(target_path) is False:
        os.makedirs(target_path)
        try:
            print('Fetching repo from github: {}/{}'.format(owner, name))
            Repo.clone_from(url, target_path, bare=True)
            insert_into_db(repo_id, owner, name)
        except:
            print('failed to clone repo: {}/{}'.format(owner, name))
            continue
    else:
        print('Using cache')
        insert_into_db(repo_id, owner, name)

    shutil.rmtree(target_path)

cursor.close()
