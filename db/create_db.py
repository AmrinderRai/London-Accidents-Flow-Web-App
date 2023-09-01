import sqlite3 
from sqlite3 import Error
from utils.connect_to_db import create_connection

def main():
    # Following tutorial: https://www.sqlitetutorial.net/sqlite-python/creating-tables/
    # TO BE COMPLETED 
    database = "./sqlite/db/london_viz.db"

    sql_create_collision_vehicle_table = ""

    sql_create_collision_casualties_table = ""

    sql_create_collision_attendant_table = ""

    sql_create_flow_table = ""

    conn = create_connection(database)


if __name__ == '__main__':
    main()

