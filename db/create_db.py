import sqlite3 
from sqlite3 import Error

def create_connection(string: db_file):
    """ create a db connection to sqlite db """

    conn = None

    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    create_connection("./sqlite/db/london_viz.db")

