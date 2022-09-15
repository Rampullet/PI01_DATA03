from sqlalchemy import select, func
from fastapi import APIRouter, Query
from config.db import connection
from models.constructor import constructors, circuits, drivers, races, pit_stops, results, qualifying, lap_times


constructor = APIRouter()


@constructor.get('/constructors')
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


@constructor.get('/year-with-more-races')
def getYear():
    return connection.execute(select(races.c.year)
                              .group_by(races.c.year)
                              .order_by(func.count('*').desc())).first()


@constructor.get('/winningest-driver')
def getWinningestDriver():
    return connection.execute(select(drivers)
                              .join(results, results.c.driverId == drivers.c.id)
                              .where(results.c.positionOrder == 1)
                              .group_by(drivers.c.id)
                              .order_by(func.count('*').desc())).first()


@constructor.get('/circuit-with-more-races')
def getCircuit():
    circuitId = connection.execute(select(races.c.circuitId)
                                   .group_by(races.c.circuitId)
                                   .order_by(func.count('*').desc())).first()
    return connection.execute(select(circuits).where(circuits.c.id == circuitId.circuitId)).fetchall()


@constructor.get("/highest-scoring-driver-by-constructor/")
def getHighestScoringDriver(nationality: list[str] | None = Query(default=None)):
    highestScoringDriverId = connection.execute(select(results.c.driverId)
                                                .join(constructors, results.c.constructorId == constructors.c.id)
                                                .where(constructors.c.nationality.in_(nationality))
                                                .group_by(results.c.driverId)
                                                .order_by(func.sum(results.c.points).desc())).first()
    return connection.execute(select(drivers).where(drivers.c.id == highestScoringDriverId.driverId)).fetchall()
