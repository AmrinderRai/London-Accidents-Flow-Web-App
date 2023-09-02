import pandas as pd 
import json 
from utils.connect_to_db import create_connection

def main():

    database = "./sqlite/db/london_viz.db"
    conn = create_connection(database)

    with open('data_sources.json') as file:
        flow_data_url = json.load(file)[1]
    
    df = pd.read_csv(flow_data_url)

    df.to_sql(name='flow', con=conn, if_exists='replace')

if __name__ == '__main__':
    main()