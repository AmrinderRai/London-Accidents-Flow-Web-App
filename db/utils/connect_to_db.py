import sqlite3 
from sqlite3 import Error

def create_connection(db_file: str):
    """ create a db connection to sqlite db """

    conn = None

    try:
        conn = sqlite3.connect(db_file)
        return conn 
    except Error as e:
        print(e)
    
    return conn 