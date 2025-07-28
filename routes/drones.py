from fastapi import HTTPException, APIRouter

from utils.drones import violated_drones, append_owner_details, log_offender
import requests

import asyncio
import os

drones_route = APIRouter()

@drones_route.get("/drones")
def drones():
	"""
	The `/drones` endpoint retrieves information from the `DRONES_API_BASE_URL` returning a JSON file
	with the list of all drones within sight of the radar. Upon detecting a violation, we log the offender
	drone into the database.
	"""
	url = os.environ["DRONES_API_BASE_URL"] + "drones"
	res = requests.get(url)
	if res.status_code != 200:
		# log error
		return HTTPException(500, "Internal server error")

	try:
		body = res.json()
	except:
		# log error
		return HTTPException(500, "Internal server error")

	drones = violated_drones(body)
	if drones:
		if not append_owner_details(drones):
			return HTTPException(500, "Internal server error")
		log_offender(drones)
	return body
