from select import select
from fastapi import APIRouter
import sqlalchemy as db
from config.db import connection, engine, metadata
from models.constructor import constructors, circuits, drivers, races, pit_stops, results, qualifying, lap_times


constructor = APIRouter()


@constructor.get('/constructors')
# def allConstructors():
#     constructors = db.Table('constructors', metadata,
#                             autoload=True, autoload_with=engine)
#     query = db.select([constructors])
#     ResultProxy = connection.execute(query)
#     ResultSet = ResultProxy.fetchall()
#     return ResultSet
def getConstructors():
    return connection.execute(constructors.select()).fetchall()


@constructor.get('/circuits')
def getCircuits():
    return connection.execute(circuits.select()).fetchall()


@constructor.get('/drivers')
def getDrivers():
    return connection.execute(drivers.select()).fetchall()


@constructor.get('/races')
def getRaces():
    return connection.execute(races.select()).fetchall()


@constructor.get('/pit-stops')
def getPitStops():
    return connection.execute(pit_stops.select()).fetchall()


@constructor.get('/results')
def getResults():
    return connection.execute(results.select()).fetchall()


@constructor.get('/qualifying')
def getQualifying():
    return connection.execute(qualifying.select()).fetchall()


@constructor.get('/lap-times')
def getLapTimes():
    return connection.execute(lap_times.select()).fetchall()
