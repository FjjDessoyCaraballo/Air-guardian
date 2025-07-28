import math
import requests
import os
import psycopg
import logging
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

def violated_drones(drones):
    """
    This function is responsible for detecting any drone that comes within a radius of
    1000m of the no-fly zone (nfz).
    
    :Parameter: drones - A list of dictionaries
    
    :Returns: violated - A list of dictionaries with appended new offender.
    """
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
            body = req.json()
            drone["id"] = body["id"]
            drone["first_name"] = body["first_name"]
            drone["last_name"] = body["last_name"]
            drone["social_security_number"] = body["social_security_number"]
            drone["phone_number"] = body["phone_number"]
        except Exception as err:
            logger.error("Error occured while updating drone's owner details \n{}".format(err))
            return False
    return True

def log_offender(drones_list):
    """
    This function is responsible for logging offending drones into our database. It requires an
    `.env` variable. If you do not know how to make your own `.env` variable, there is an `.env.example`
    for you to follow.  
    
    :Parameters: drones_list - A list of dictionaries with offending drones.    
    
    :Returns: True/False if either successful or failure.
    """
    connection_string = (
        f"host=localhost port=5432 "
        f"dbname={os.getenv('DB_NAME')} "
        f"user={os.getenv('DB_USER')} "
        f"password={os.getenv('DB_PASSWORD')}"
        )
    
    try:
        with psycopg.connect(connection_string) as conn:
            with conn.cursor() as cur:
                for drone in drones_list:
                    cur.execute('''
                        INSERT INTO nfz_offender (
                            drone_uuid, position_x, position_y, position_z,
                            first_name, last_name, social_security, phone_number
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s
                    ) ON CONFLICT (drone_uuid) DO UPDATE SET
                        time = NOW(),
                        position_x = EXCLUDED.position_x,
                        position_y = EXCLUDED.position_y,
                        position_z = EXCLUDED.position_z
                    ''', (
                        drone['id'],
                        drone['x'],
                        drone['y'],
                        drone['z'],
                        drone['first_name'],
                        drone['last_name'],
                        drone['social_security_number'],
                        drone['phone_number'],
                    )) #here are the values coming from drone
                conn.commit()
    except psycopg.Error as e:
        print(f'Database insertion failed: {e}')
        return False
    except Exception as e:
        print(f'Unknown exception: {e}')
        return False
    return True