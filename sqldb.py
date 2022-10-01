import flightapi
from sqlalchemy import create_engine
import sqlite3
 
def create_sql_db():
    engine = create_engine('sqlite:///flights.db',
                        echo = False)

    data = flightapi.create_pd_df()
    data.to_sql('Flight_Data', con = engine, if_exists='append')
    delete_repeats()

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
    

conn = sqlite3.connect("flights.db")
cur = conn.cursor()
cur.execute("SELECT value, origin, destination FROM Flight_Data")
print(cur.fetchall())