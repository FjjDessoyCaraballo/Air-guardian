from dotenv import load_dotenv
import os
import sys
import logging

logger = logging.getLogger(__name__)

def initialize_vars():
    load_dotenv()
    required_vars = ["X-SECRET", "DRONES_API_BASE_URL"]
    missing = []
    for var in required_vars:
        if var not in os.environ:
            missing.append(var)
    if missing:
        logger.error("Missing env vars: {}".format(missing))
        sys.exit(1)

def initialize_celery_vars():
    load_dotenv()
    required_vars = ["BROKER_URL", "LOCAL_HOST_URL"]
    missing = []
    for var in required_vars:
        if var not in os.environ:
            missing.append(var)
    if missing:
        logger.error("Missing env vars: {}".format(missing))
        sys.exit(1) 