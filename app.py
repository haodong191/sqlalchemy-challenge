# import dependencies 
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# import sqlite file
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

app = Flask(__name__)

# delcare classes
hawaii_measurement = Base.classes.measurement
hawaii_station = Base.classes.station

# set routes
@app.route("/")
def Home():
    return (
        f"This is the homepage<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/2016-08-23<br/>"
        f"/api/v1.0/2016-08-23/2017-08-23<br/>"
    )

# define what will be on /api/v1.0/precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
#     pull all data and prcp data from hawaii_measurement
    results = session.query(hawaii_measurement.date, hawaii_measurement.prcp).all()
    session.close()
    data = list(np.ravel(results))

    return jsonify(data)

# define what will be on /api/v1.0/stations
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
#     pull all station data from hawaii_station
    results = session.query(hawaii_station.station).all()
    session.close()
    data = list(np.ravel(results))

    return jsonify(data)

# define what will be on /api/v1.0/tobs
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
#     pull data <= 2017-08-23 and >= 2016-08-23 of date and tobs from hawaii_measurement
    results = session.query(hawaii_measurement.date, hawaii_measurement.tobs).\
            filter(hawaii_measurement.date <= "2017-08-23").\
            filter(hawaii_measurement.date >= "2016-08-23").\
            filter(hawaii_measurement.station == station_USC00519281).all()
    session.close()
    data = list(np.ravel(results))

    return jsonify(data)

# define what will be on /api/v1.0/2016-08-23
@app.route("/api/v1.0/2016-08-23")
def start():
    session = Session(engine)
#     pull data >= 2016-08-23 of tobs and run min, avg, and max function, from hawaii_measurement
    results = session.query(func.min(hawaii_measurement.tobs), func.avg(hawaii_measurement.tobs), func.max(hawaii_measurement.tobs)).\
        filter(hawaii_measurement.date >= "2016-08-23").all()
    session.close()
    data = list(np.ravel(results))
    return jsonify(data)


# define what will be on api/v1.0/2016-08-23/2017-08-23
@app.route("/api/v1.0/2016-08-23/2017-08-23")
def start_end():
    session = Session(engine)
#     pull data <= 2017-08-23 and >= 2016-08-23 of tobs and run min, avg, and max function, from hawaii_measurement
    results = session.query(func.min(hawaii_measurement.tobs), func.avg(hawaii_measurement.tobs), func.max(hawaii_measurement.tobs)).\
        filter(hawaii_measurement.date >= "2016-08-23").filter(hawaii_measurement.date <= "2017-08-23").all()
    session.close()
    data = list(np.ravel(results))
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
