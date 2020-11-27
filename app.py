import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

Base.classes.keys()

Measurement = Base.classes.measurement
station = Base.classes.station

app = Flask(__name__)

app.route("/")
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
    results = session.query(measurement.date, measurement.percipitation).all()

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
	tobs_year = []
	results = session.query(measurement.tobs).filter(measurement.date >= "08-23-2017").all()

	tobs_year = list(np.ravel(results))

	return jsonify(tobs_year)