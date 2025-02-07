import glob
import pandas as pd
from models.constructor import constructors, circuits, drivers, races, pit_stops, results, qualifying, lap_times
from config.db import connection
from sqlalchemy.sql.sqltypes import Integer, Float, Date, Time

# constructors
firstConstructor = connection.execute((constructors.select())).first()
if firstConstructor is None:
    constructors = pd.read_json('Datasets/constructors.json', lines=True)
    constructors = constructors.rename(
        {'constructorId': 'id', 'constructorRef': 'ref'}, axis='columns')
    constructors.to_sql('constructor', connection,
                        index=False, if_exists='append')

# circuits
firstCircuit = connection.execute((circuits.select())).first()
if firstCircuit is None:
    circuits = pd.read_csv('Datasets/circuits.csv')
    circuits = circuits.rename(
        {'circuitId': 'id', 'circuitRef': 'ref'}, axis='columns')
    circuits.to_sql('circuit', connection, index=False,
                    dtype={'lat': Float, 'lng': Float, 'alt': Integer}, if_exists='append')

# drivers
firstDriver = connection.execute((drivers.select())).first()
if firstDriver is None:
    drivers = pd.read_json('Datasets/drivers.json', lines=True)
    names = pd.json_normalize(drivers['name'])
    drivers = pd.concat([drivers, names], axis=1)
    drivers = drivers.drop(columns=['name'])
    drivers['number'] = pd.to_numeric(drivers['number'], errors='coerce')
    drivers = drivers.replace('\\N', '')
    drivers = drivers.rename(
        {'driverId': 'id', 'driverRef': 'ref'}, axis='columns')
    drivers.to_sql('driver', connection, index=False,
                   dtype={'number': Integer, 'dob': Date}, if_exists='append')

# races
firstRace = connection.execute((races.select())).first()
if firstRace is None:
    races = pd.read_csv('Datasets/races.csv')
    races = races.rename(
        {'raceId': 'id'}, axis='columns')
    races = races.replace('\\N', '')
    races.to_sql('race', connection, index=False,
                 dtype={'date': Date, 'time': Time}, if_exists='append')

# pit_stops
firstPit_stop = connection.execute((pit_stops.select())).first()
if firstPit_stop is None:
    pit_stops = pd.read_json('Datasets/pit_stops.json')
    pit_stops.to_sql('pit_stop', connection, index=False,
                     dtype={'time': Time}, if_exists='append')

# results
firstResult = connection.execute((results.select())).first()
if firstResult is None:
    results = pd.read_json('Datasets/results.json', lines=True)
    results = results.rename({'resultId': 'id'}, axis='columns')
    results['number'] = pd.to_numeric(results['number'], errors='coerce')
    results['position'] = pd.to_numeric(results['position'], errors='coerce')
    results['milliseconds'] = pd.to_numeric(
        results['milliseconds'], errors='coerce')
    results['fastestLap'] = pd.to_numeric(
        results['fastestLap'], errors='coerce')
    results['rank'] = pd.to_numeric(results['rank'], errors='coerce')
    results = results.replace('\\N', '')
    results.to_sql('result', connection, index=False,
                   dtype={'number': Integer, 'position': Integer}, if_exists='append')

# qualifying
firstQualifying = connection.execute((qualifying.select())).first()
if firstQualifying is None:
    qualifying = pd.DataFrame()
    filenames = glob.glob('Datasets/Qualifying/qualifying*.json')
    for f in filenames:
        qualifying_split = pd.read_json(f)
        qualifying = pd.concat(
            [qualifying_split, qualifying], ignore_index=True)
    qualifying = qualifying.rename({'qualifyId': 'id'}, axis='columns')
    qualifying = qualifying.replace('\\N', '')
    qualifying.to_sql('qualifying', connection, index=False,
                      dtype={'number': Integer, 'position': Integer}, if_exists='append')


# lap_times
firstLap_times = connection.execute((lap_times.select())).first()
if firstLap_times is None:
    lap_times = pd.DataFrame()
    filenames = glob.glob('Datasets/lap_times/lap_times*.csv')
    column_names = ['raceId', 'driverId', 'lap',
                    'position', 'time', 'milliseconds']
    for f in filenames:
        lap_times_split = pd.read_csv(f, names=column_names)
        lap_times = pd.concat([lap_times_split, lap_times], ignore_index=True)
    lap_times.to_sql('lap_time', connection, index=False, if_exists='append')
