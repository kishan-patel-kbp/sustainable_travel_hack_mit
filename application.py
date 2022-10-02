import re
from flask import Flask, render_template, session, request
from flask_session import Session
app = Flask(__name__)
import sqlite3
from collections import defaultdict
import mysql.connector
from cs50 import SQL

import flightapi
import sqldb



@app.route('/')
@app.route('/index')
def index():
    name = 'Kishan Bob'
    return render_template('index.html', title='Fly Low', username=name)

Session(app)

if __name__ == '__main__':
    app.run(host='127.0.0.1')

db = SQL("sqlite:///flights_with_emissions.db")

@app.route("/search", methods=["GET", "POST"])
def search():
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

        data = sqldb.create_sql_db(start_date, origin)
        data = sqldb.add_carbon_emissions(data)
        sqldb.create_table(data)

        flights = db.execute("SELECT * FROM Flight_Data LIMIT 10")
        print(flights)
        return render_template('flights.html', flights = flights)

@app.route("/destinations", methods=["GET", "POST"])
def destinations():
    sentence = "There are a variety of sustainable travel solutions just minutes away, just fill out the form now"
    return render_template('destinations.html', sentence = sentence)