from fastapi import FastAPI
from routes.drones import drones_route
from routes.health import health_route
from routes.nfz import nfz_route
from dotenv import load_dotenv
from utils.database import create_db

load_dotenv()
create_db()
air_guardian = FastAPI()
air_guardian.include_router(health_route)
air_guardian.include_router(drones_route)
air_guardian.include_router(nfz_route)
