from fastapi import FastAPI
from routes.constructors import constructor
import etl


app = FastAPI()


app.include_router(constructor)
