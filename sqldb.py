from codecs import ignore_errors
from locale import D_FMT
import flightapi
import climateapi
from sqlalchemy import create_engine
import sqlite3
import pandas as pd
import sqlite3
from contextlib import closing

pd.options.mode.chained_assignment = None 
 
def create_sql_db(period, origin_iata):
    engine = create_engine('sqlite:///test.db',
                        echo = False)

    data = flightapi.create_pd_df(period, origin_iata)
    data['carbon_emissions'] = None
    return data

def delete_repeats():
    conn = sqlite3.connect("flights.db")
    cur = conn.cursor()
    sql_query = """
        WITH cte AS (
        SELECT 
            origin, 
            destination, 
            value, 
            ROW_NUMBER() OVER (
                PARTITION BY 
                    origin, 
                    destination, 
                    value
                ORDER BY 
                    origin, 
                    destination, 
                    value
            ) row_num
        FROM 
            flights.Flight_Data
    )
    DELETE FROM cte
    WHERE row_num > 1;
    """
    cur.execute(sql_query)
    conn.close()
    
def get_origin_destination():
    conn = sqlite3.connect("flights_with_emissions.db")
    with closing(conn.cursor()) as cur:
        cur.execute("SELECT origin, destination FROM Flight_Data")
        return cur.fetchall()

def add_carbon_emissions(data):
    # engine = create_engine('sqlite:///flights.db', echo = False)
    # df = pd.concat([pd.DataFrame([idx, climateapi.get_carbon_emission(trip[0], trip[1])], columns=['carbon_emissions']) for idx, trip in enumerate(get_origin_destination())])
    conn = sqlite3.connect("flights.db")
    with closing(conn.cursor()) as cur:
        count = 0
        for trip in get_origin_destination():
            origin = trip[0]
            destination = trip[1]
            carbon_emission = climateapi.get_carbon_emission(origin, destination)
            if carbon_emission == None:
                carbon_emission = 0
            data["carbon_emissions"][count] = carbon_emission
            count += 1
        return data

def create_table(data):
    """
    write code here
    data is a pandas dataframe
    """
    conn = sqlite3.connect("flights_with_emissions.db")
    with closing(conn.cursor()) as cur:
        sql_query = """
            CREATE TABLE IF NOT EXISTS "Flight_Data" (
            "index" INTEGER PRIMARY KEY AUTOINCREMENT, 
            value FLOAT, 
            ttl BIGINT, 
            trip_class BIGINT, 
            return_date TEXT, 
            origin TEXT, 
            number_of_changes FLOAT, 
            distance BIGINT, 
            destination TEXT, 
            depart_date TEXT, 
            airline TEXT,
            carbon_emissions FLOAT
    );

        """
        cur.execute(sql_query)

        for index, row in data.iterrows():
            #print(row['ttl'], row['value'], row['carbon_emissions'])
            if row['carbon_emissions'] != 0:
                sql_query = """
                INSERT INTO Flight_Data (value, ttl, trip_class, return_date, origin, number_of_changes, distance, destination, depart_date, airline, carbon_emissions)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                """

                cur.execute(sql_query, tuple([row['value'], row['ttl'], row['trip_class'], row['return_date'], row['origin'], row['number_of_changes'], row['distance'], row['destination'], row['depart_date'], row['airline'], row['carbon_emissions']]))
                
        # TEST
        cur.execute("SELECT * FROM Flight_Data")
        conn.commit()

