import psycopg2
from config2 import load_config

def connect(config2):
    """ Connect to the PostgreSQL database server """
    try:
        with psycopg2.connect(**config2) as conn:
            print('Connected to the PostgreSQL server.')
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

if __name__ == '__main__':
    config2 = load_config()
    connect(config2)
    conn = psycopg2.connect("dbname=suppliers user=postgres password=dikossia06")