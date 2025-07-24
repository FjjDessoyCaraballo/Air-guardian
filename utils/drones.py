import math
import requests
import os
import logging

logger = logging.getLogger(__name__)

def violated_drones(drones):
    violated = []
    for drone in drones:
        distance = math.sqrt(drone["x"]**2 + drone["y"]**2)
        if distance < 1000:
            violated.append(drone)
    return violated

def append_owner_details(violated_drones):
    for drone in violated_drones:
        url = os.environ["DRONES_API_BASE_URL"] + "users/" + str(drone["owner_id"])
        try:
            res = requests.get(url)
        except Exception as err:
            logger.error("Error occurred while fetching owner details:{}".format(url))
            logger.error(err)
            return False
        if res.status_code != 200:
            logger.error("Received status code {} from {}".format(res.status_code, url))
            return False
        try:
            body = res.json()
        except:
            logger.error("Failed to parse the response body")
            return False
        try:
            drone["first_name"] = body["first_name"]
            drone["last_name"] = body["last_name"]
            drone["social_security_number"] = body["social_security_number"]
            drone["phone_number"] = body["phone_number"]
        except Exception as err:
            logger.error("Error occured while updating drone's owner details \n{}".format(err))
            return False
    return True