import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
from datetime import datetime


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Stations = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all prcp and date"""
    # Query all precipitation
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > '2016-08-22').all()

    session.close()
    
    # Create a dictionary from the row data and append to a list of precipitation with date
    all_prcp = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query all passengers
    results = session.query(Stations.station, Stations.name).all()

    session.close()

    # Convert list of tuples into normal list
    all_station = list(np.ravel(results))

    return jsonify(all_station)



@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all date & tobs"""
    # Query results
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > '2016-08-22').filter(Measurement.station == 'USC00519281').all()
                                                                       
    session.close()

    # Create a dictionary from the row data and append to a list of all_tobs
    all_tobs = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)


@app.route("/api/v1.0/<start>")
def start(start):
    
    start = datetime.strptime(start, "%Y-%m-%d").date()

    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all date & tobs"""
    # Query results
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()   
        
    session.close()

    # Create a dictionary from the row data and append to a list of all_tobs
    all_temp = []
    for minimum, average, maximum in results:
        temp_dict = {}
        temp_dict["minimum"] = minimum
        temp_dict["average"] = average
        temp_dict["maximum"] = maximum
        all_temp.append(temp_dict)

    return jsonify(all_temp)


@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    
    start = datetime.strptime(start, "%Y-%m-%d").date()
    end = datetime.strptime(end, "%Y-%m-%d").date()
        
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all date & tobs"""
    # Query results
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()   
        
    session.close()

    # Create a dictionary from the row data and append to a list of all_tobs
    all_temp2 = []
    for minimum, average, maximum in results:
        temp_dict2 = {}
        temp_dict2["minimum"] = minimum
        temp_dict2["average"] = average
        temp_dict2["maximum"] = maximum
        all_temp2.append(temp_dict2)

    return jsonify(all_temp2)


if __name__ == '__main__':
    app.run(debug=True)

