from codecs import ignore_errors
from locale import D_FMT
import flightapi
import climateapi
from sqlalchemy import create_engine
import sqlite3
import pandas as pd

pd.options.mode.chained_assignment = None 
 
def create_sql_db():
    engine = create_engine('sqlite:///test.db',
                        echo = False)

    data = flightapi.create_pd_df()
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
    
def get_origin_destination():
    conn = sqlite3.connect("flights.db")
    cur = conn.cursor()
    cur.execute("SELECT origin, destination FROM Flight_Data")
    return cur.fetchall()

def add_carbon_emissions(data):
    # engine = create_engine('sqlite:///flights.db', echo = False)
    # df = pd.concat([pd.DataFrame([idx, climateapi.get_carbon_emission(trip[0], trip[1])], columns=['carbon_emissions']) for idx, trip in enumerate(get_origin_destination())])
    conn = sqlite3.connect("flights.db")
    cur = conn.cursor()
    count = 0
    for trip in get_origin_destination():
        origin = trip[0]
        destination = trip[1]
        carbon_emission = climateapi.get_carbon_emission(origin, destination)
        if carbon_emission == None:
            carbon_emission = 0
        data["carbon_emissions"][count] = carbon_emission
        count += 1
    print(data)

def create_table(data):
    """
    write code here
    data is a pandas dataframe
    """
    pass

data = create_sql_db()
data = add_carbon_emissions(data)
create_table(data)
