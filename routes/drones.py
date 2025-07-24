from fastapi import HTTPException, APIRouter
from utils.drones import violated_drones, append_owner_details
import requests
import os

drones_route = APIRouter()

@drones_route.get("/drones")
def drones():
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
		print("violation detected")
		if not append_owner_details(drones):
			return HTTPException(500, "Internal server error")
		#update db
	return body