#__________________________________________________________________

# Importing Flask
from flask import Flask, jsonify
# Python SQL toolkit and Object Relational Mapper
import sqlalchemy, numpy as np, pandas as pd, datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#__________________________________________________________________

# Defining engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#__________________________________________________________________

# Creating app
app = Flask(__name__)

#__________________________________________________________________

# Defining index route
@app.route("/")
def routes():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/startend<br/>"
    )

#__________________________________________________________________

# Precipitation API

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Defining session
    session = Session(engine)
    # Query to retrieve the last 12 months of precipitation data
    prcp = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-23').order_by(Measurement.date.asc()).all()

    session.close()

    rain = list(np.ravel(prcp))
    return jsonify(rain)

#__________________________________________________________________

# Stations API

@app.route("/api/v1.0/stations")
def station():
    # Defining session
    session = Session(engine)
    # Query to retrieve stations
    stats = session.query(Station.station, Station.name).all()

    session.close()

    sta = list(np.ravel(stats))
    return jsonify(sta)

#__________________________________________________________________

# Tobs API

@app.route("/api/v1.0/tobs")
def tobs():
    # Defining session
    session = Session(engine)
    # Query to retrieve tobs
    tob = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= '2016-08-23').all()

    session.close()

    temp = list(np.ravel(tob))
    return jsonify(temp) 

#__________________________________________________________________

# Start API
    
@app.route("/api/v1.0/start")
def start():
    # Defining session
    session = Session(engine)
    # Query
    star = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= '2017-08-18').all()

    session.close()

    strt = list(np.ravel(star))
    return jsonify(strt)
     


    
#__________________________________________________________________

# Start and End Dates API

@app.route("/api/v1.0/startend")
def startend():
    session = Session(engine)
    stend = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= '2017-01-01').filter(Measurement.date <= '2017-02-01').all()

    session.close()

    stnd = list(np.ravel(stend))
    return jsonify(stnd)

    
#__________________________________________________________________
   
    # Allowing to run server from Terminal with: python app.py
if __name__ == "__main__":
    app.run(debug=True)