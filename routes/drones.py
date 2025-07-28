from fastapi import HTTPException, APIRouter

from utils.drones import violated_drones, append_owner_details, log_offender
import requests

import asyncio
import os
import logging

drones_route = APIRouter()
logger = logging.getLogger(__name__)

@drones_route.get("/drones", response_model=list[Drone])
def drones():
	"""
	The `/drones` endpoint retrieves information from the `DRONES_API_BASE_URL` returning a JSON file
	with the list of all drones within sight of the radar. Upon detecting a violation, we log the offender
	drone into the database.
	"""
	url = os.environ["DRONES_API_BASE_URL"] + "drones"
	try:
		res = requests.get(url)
	except Exception as err:
		logger.error("Error occurred from request url:{}".format(url))
		logger.error(err)
		raise HTTPException(500, "Internal server error")
	
	if res.status_code != 200:
		logger.error("Received status code {} from {}".format(res.status_code, url))
		raise HTTPException(500, "Internal server error")

	try:
		body = res.json()
	except:
		logger.error("Failed to parse the response body")
		raise HTTPException(500, "Internal server error")

	drones = violated_drones(body)
	if drones:
		if not append_owner_details(drones):
			return HTTPException(500, "Internal server error")
		log_offender(drones)
	return body
