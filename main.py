from fastapi import FastAPI
from routes.drones import drones_route
from routes.health import health_route
from routes.nfz import nfz_route
from utils.setup import initialize_vars
from dotenv import load_dotenv
from utils.database import create_db
import logging

logging.basicConfig(filename="air_guardian.log", level=logging.INFO, format="[%(asctime)s:%(levelname)s:%(message)s]")
logger = logging.getLogger(__name__)
logger.info("Initializing app...")
initialize_vars()
load_dotenv()
create_db()
air_guardian = FastAPI()
air_guardian.include_router(health_route)
air_guardian.include_router(drones_route)
air_guardian.include_router(nfz_route)
logger.info("Successfully started the server")
