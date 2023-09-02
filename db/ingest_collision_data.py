import pandas as pd 
from utils.connect_to_db import create_connection
from utils.bng_to_latlong import BNGtoLatLong
import json

def main():

    database = "./sqlite/db/london_viz.db"
    conn = create_connection(database)

    with open('data_sources.json') as file:
        collision_data_sources = json.load(file)[0]

    for year, data_urls in collision_data_sources.items():
        vehicles_df = pd.read_csv(data_urls['vehicles'])
        attendant_df = pd.read_csv(data_urls['attendant'])

        collisions_df = pd.merge(vehicles_df[['AREFNO', 'Vehicle Type (Banded)']], attendant_df, left_on="AREFNO", right_on="Accident Ref.")
        collisions_df['year'] = year
        collisions_df[['latitude', 'longitude']] = collisions_df.apply(BNGtoLatLong, axis=1)

        collisions_df.to_sql(name='collisions', con=conn, if_exists='append')


if __name__ == '__main__':
    main()