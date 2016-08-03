import psycopg2
from source.helpers.env import env


try:
    host = env('db.host', 'localhost')
    db = env('db.name', 'ubuntu')
    user = env('db.user', 'ubuntu')
    connect_str = "dbname='{}' user='{}' host='{}'".format(db, user, host)
    print(connect_str)
    conn = psycopg2.connect(connect_str)
    print('Connected to DB')

except Exception as e:
    print("Uh oh, can't connect. Invalid dbname, user or password?")
    print(e)


def execute(query, parameters):
    '''
    '''
    cur = conn.cursor()
    cur.execute(query, parameters)
    conn.commit()


def fetch(query, parameters=None):
    '''
    '''
    cur = conn.cursor()
    cur.execute(query, parameters)
    return cur
