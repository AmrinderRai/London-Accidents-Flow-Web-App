import pandas as pd 
import json 
from utils.connect_to_db import create_connection
import requests
import io 

def main():

    database = "./sqlite/db/london_viz.db"
    conn = create_connection(database)

    with open('data_sources.json') as file:
        flow_data_url = json.load(file)[1]
    
    with requests.Session() as s: 
        download = s.get(flow_data_url).content.decote('utf-8')

    df = pd.read_csv(io.StringIO(download))
    df.to_sql(name='flow', con=conn, if_exists='replace')

if __name__ == '__main__':
    main()