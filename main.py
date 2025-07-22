from fastapi import FastAPI
from routes.drones import drones_route
from routes.health import health_route
from routes.nfz import nfz_route
import sqlite3

conn = sqlite3.connect("mydb.db")
air_guardian = FastAPI()
air_guardian.include_router(health_route)
air_guardian.include_router(drones_route)
air_guardian.include_router(nfz_route)
