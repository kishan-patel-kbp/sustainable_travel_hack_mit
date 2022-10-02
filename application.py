import re
from flask import Flask, render_template, session, request
from flask_session import Session
app = Flask(__name__)
import sqlite3
from collections import defaultdict
from cs50 import SQL
from urllib.parse import urlparse
from urllib.parse import parse_qs
import flightapi
import sqldb



@app.route('/')
@app.route('/index')
def index():
    name = 'Kishan Bob'
    return render_template('index.html', title='Fly Low', username=name)

@app.route('/about')
def about():
    return render_template("about.html")
    

Session(app)

if __name__ == '__main__':
    app.run(host='127.0.0.1')

db = SQL("sqlite:///flights_with_emissions.db")

@app.route('/loading', methods=["GET", "POST"])
def loading():
    if request.method == "POST":
        # Ensure start date was submitted
        if not request.form.get("start_date"):
            return "RIP"
        
        # Ensure end date was submitted
        if not request.form.get("end_date"):
            return "RIP"
        
        # Ensure starting airport was submitted
        if not request.form.get("src"):
            return "RIP"

        # get these variables
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")
        origin = request.form.get("src")

        # Validate start date before end date
        if start_date > end_date:
            return "RIP"

        # Validate length of origin
        if len(origin) != 3:
            return "RIP"
        
        return render_template('loading.html', start = start_date, end = end_date, origin = origin)

    else:
        return "RIP"

@app.route("/search", methods=["GET", "POST"])
def search():
    
    parsed_url = urlparse(request.url)
    start_date = parse_qs(parsed_url.query)['start_date'][0]
    end_date = parse_qs(parsed_url.query)['end_date'][0]
    origin = parse_qs(parsed_url.query)['origin'][0]

    data = sqldb.create_sql_db(start_date, origin)
    data = sqldb.add_carbon_emissions(data)
    sqldb.create_table(data)

    search_query = "SELECT * FROM Flight_Data WHERE ? >= depart_date AND return_date >= ? AND origin = ? GROUP BY carbon_emissions LIMIT 10"
    
    flights = db.execute(search_query, start_date, end_date, origin)
    print(flights)
    return render_template('flights.html', flights = flights)

@app.route("/destinations", methods=["GET", "POST"])
def destinations():
    sentence = "There are a variety of sustainable travel solutions just minutes away, just fill out the form now"
    return render_template('destinations.html', sentence = sentence)

@app.route("/methodology")
def methodology():
    sentence = "To implement FlyLow we used the Flight Labs API to find flights from our origin to possible destinations. We extract the cost for flights and then pass the flight information to the Climatiq API to retrieve carbon emission information. We populate these results in a SQL database and then retrieve flights based on the users origin and dates entered."
    return render_template('methodology.html', sentence = sentence)

