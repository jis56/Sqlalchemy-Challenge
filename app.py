import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()

measurement = Base.classes.measurement
station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/percipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<YYYY/MM/DD>"
        f"/api/v1.0/<YYYY/MM/DD/YYYY/MM/DD>"
    )

@app.route("/api/v1.0/percipitation")
def percipitation():
    session = Session(engine)
    results = session.query(measurement.date, measurement.prcp).all()
    session.close()

    all_percipitation = []
    for date, percipitation in results:
        percipitation_dict = {}
        percipitation_dict["date"] = date
        percipitation_dict["percipitation"] = percipitation
        all_percipitation.append(percipitation_dict)
        
    return jsonify(all_percipitation)

@app.route("/api/v1.0/stations") 
def stations():
    session = Session(engine)
    results = session.query(station.name).all()
    session.close()

    station_list = list(np.ravel(results))

    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def temperature():
    session = Session(engine)
    twelve_date = dt.datetime(2016, 8, 23)
    results = session.query(measurement.date, measurement.tobs).\
        filter(measurement.date >= twelve_date).\
        filter(measurement.station == "USC00519281").all()
    session.close()
    
    tobs_year = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        tobs_year.append(tobs_dict)

    return jsonify(tobs_year)

@app.route("/api/v1.0/<start>")
def start_temp(start):
    session = Session(engine)

    results = session.query(func.min(measurement.tobs),func.avg(measurement.tobs),func.max(measurement.tobs)).\
                filter(measurement.date >= start).all()

    session.close()

    start_results = list(np.ravel(results))

    return jsonify(start, start_results)

@app.route("/api/v1.0/<start>/<end>")

def start_end_date (start, end):
    session = Session(engine)

    results = session.query(func.min(measurement.tobs),func.avg(measurement.tobs),func.max(measurement.tobs)).\
    filter(measurement.date >= start).\
    filter(measurement.date <= end).all()  

    session.close()

    return jsonify(start, end, results)  

if __name__ == '__main__':
    app.run(debug=True)