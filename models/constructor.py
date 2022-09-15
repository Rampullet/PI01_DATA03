from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, Float, Date, Time
from config.db import metadata, engine


constructors = Table('constructor', metadata,
                     Column('id', Integer, primary_key=True),
                     Column('ref', String(255)),
                     Column('name', String(255)),
                     Column('nationality', String(255)),
                     Column('url', String(255)))

circuits = Table('circuit', metadata,
                 Column('id', Integer, primary_key=True),
                 Column('ref', String(255)),
                 Column('name', String(255)),
                 Column('location', String(255)),
                 Column('country', String(255)),
                 Column('lat', Float),
                 Column('lng', Float),
                 Column('alt', Integer),
                 Column('url', String(255)))

drivers = Table('driver', metadata,
                Column('id', Integer, primary_key=True),
                Column('ref', String(255)),
                Column('number', Integer),
                Column('code', String(15)),
                Column('forename', String(255)),
                Column('surname', String(255)),
                Column('dob', Date),
                Column('nationality', String(255)),
                Column('url', String(255)))

races = Table('race', metadata,
              Column('id', Integer, primary_key=True),
              Column('year', Integer),
              Column('round', Integer),
              Column('circuitId', Integer, ForeignKey('circuit.id')),
              Column('name', String(255)),
              Column('date', Date),
              Column('time', Time),
              Column('url', String(255)))

pit_stops = Table('pit_stop', metadata,
                  Column('raceId', Integer, ForeignKey('race.id')),
                  Column('driverId', Integer, ForeignKey('driver.id')),
                  Column('stop', Integer),
                  Column('lap', Integer),
                  Column('time', Time),
                  Column('duration', String(255)),
                  Column('milliseconds', Integer))

results = Table('result', metadata,
                Column('id', Integer, primary_key=True),
                Column('raceId', Integer, ForeignKey('race.id')),
                Column('driverId', Integer, ForeignKey('driver.id')),
                Column('constructorId', Integer, ForeignKey('constructor.id')),
                Column('number', Integer),
                Column('grid', Integer),
                Column('position', Integer),
                Column('positionText', String(15)),
                Column('positionOrder', Integer),
                Column('points', Float),
                Column('laps', Integer),
                Column('time', String(255)),
                Column('milliseconds', Integer),
                Column('fastestLap', Integer),
                Column('rank', Integer),
                Column('fastestLapTime', String(255)),
                Column('fastestLapSpeed', String(255)),
                Column('statusId', Integer))

qualifying = Table('qualifying', metadata,
                   Column('id', Integer, primary_key=True),
                   Column('raceId', Integer, ForeignKey('race.id')),
                   Column('driverId', Integer, ForeignKey('driver.id')),
                   Column('constructorId', Integer,
                          ForeignKey('constructor.id')),
                   Column('number', Integer),
                   Column('position', Integer),
                   Column('q1', String(255)),
                   Column('q2', String(255)),
                   Column('q3', String(255)))

lap_times = Table('lap_time', metadata,
                  Column('raceid', Integer, ForeignKey('race.id')),
                  Column('driverId', Integer, ForeignKey('driver.id')),
                  Column('lap', Integer),
                  Column('position', Integer),
                  Column('time', String(255)),
                  Column('milliseconds', Integer))

metadata.create_all(engine, checkfirst=True)
