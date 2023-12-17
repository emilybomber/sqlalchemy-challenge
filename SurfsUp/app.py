# Import the dependencies.
import numpy as np
import sqlalchemy
import datetime as dt
from flask import Flask, jsonify
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


#################################################
# Database Setup
#################################################
engine = create_engine(f"sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base

# reflect the tables
Base.prepare(autoload_with=engine)


# Save references to each table
Measurement = Base.classes.measurement
Station = Base.clasess.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route('/')
def welcome():
    return(
        f"Welcome!<br/>"
        f"Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"#/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br>"
        )

@app.route('/api/v1.0/precipitation')
def precipitation():
    #Calculate the date 1 year ago from the last date in teh date base
    prev_year = dt.date(2017, 9, 23) - dt.timedelta(days=365)

    # Query data from the last year
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_year).all()
    session.close()

    # Convert the query results to a dictionary
    precipitation_data = {date: prcp for date, prcp in results}

    return jsonify(precipitation_data)

@app.route('/api/v1.0/stations')
def stations():
    #Return list of stations
    result = session.query(Station.station).all()
    session.close()

    #Unravel out results
    result = list(np.ravel(result))
    return jsonify(result)

@app.route('/api/v1.0/tobs')
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= prev_year).all()
    # Convert the query results to a list of dictionaries
    temp_data = [{"date": date, "tobs": tobs} for date, tobs in results]

    return jsonify(temp_data)

# Add routes for /api/v1.0/<start> and /api/v1.0/<start>/<end> here

if __name__ == '__main__':
    app.run()