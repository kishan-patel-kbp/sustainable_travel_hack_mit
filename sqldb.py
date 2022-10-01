import flightapi
from sqlalchemy import create_engine
import sqlite3
 
def create_sql_db():
    engine = create_engine('sqlite:///flights.db',
                        echo = False)

    data = flightapi.create_pd_df()

    
    # attach the data frame to the sql
    # with a name of the table
    # as "Employee_Data"
    data.to_sql('Flight_Data', con = engine)
 
conn = sqlite3.connect("flights.db")
cur = conn.cursor()
cur.execute("SELECT value, destination FROM Flight_Data")
print(cur.fetchall())