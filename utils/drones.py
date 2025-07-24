import math
import requests
import os

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
        req = requests.get(url)
        if req.status_code != 200:
            return False
        try:
            body = req.json()
            drone["first_name"] = body["first_name"]
            drone["last_name"] = body["last_name"]
            drone["social_security_number"] = body["social_security_number"]
            drone["phone_number"] = body["phone_number"]
        except:
            return False
    return True