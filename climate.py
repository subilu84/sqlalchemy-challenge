import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

start_dt = '2016-06-29'
end_dt = '2016-07-05'

engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station


app = Flask(__name__)


@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/station<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start-end<br/>"

    )


@app.route("/api/v1.0/precipitation")
def precipitation():

    session = Session(engine)

    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    all_measurement = []
    for date, prcp in results:
        m_dict = {}
        m_dict["date"] = date
        m_dict["precipitation"] = prcp
        all_measurement.append(m_dict)

    return jsonify(all_measurement)


@app.route("/api/v1.0/station")
def station():
    
    session = Session(engine)

    results = session.query(Station.station).all()

    session.close()

    all_station = list(np.ravel(results))

    return jsonify(all_station)


@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(engine)

    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >='2016-08-23').all()

    session.close()

    all_tobs = list(np.ravel(results))

    return jsonify(all_tobs)

@app.route("/api/v1.0/start")
def start():
    session = Session(engine)

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date == start_dt).all()

    session.close()

    start_date = list(np.ravel(results))

    return jsonify(start_date)


@app.route("/api/v1.0/start-end")
def start_end():
    session = Session(engine)

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_dt).filter(Measurement.date <= end_dt).all()

    session.close()

    start_end = list(np.ravel(results))

    return jsonify(start_end)

   
if __name__ == '__main__':
    app.run(debug=True)
