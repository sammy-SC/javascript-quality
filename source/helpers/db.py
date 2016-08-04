from source.helpers.env import env
import psycopg2


try:
    host = env('db.host', '192.168.130.181')
    db = env('db.name', 'ubuntu')
    user = env('db.user', 'ubuntu')
    connect_str = "dbname='{}' user='{}' host='{}'".format(db, user, host)
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
