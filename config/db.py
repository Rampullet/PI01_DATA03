from importlib.metadata import metadata
from sqlalchemy import create_engine, MetaData


engine = create_engine("mysql+pymysql://root:HRF5t3z8fp5mpg@localhost:3306/races")

metadata= MetaData()

connection = engine.connect()