from fastapi import HTTPException, APIRouter
from utils.drones import violated_drones
import requests

drones_route = APIRouter()

@drones_route.get("/drones")
def drones():
	res = requests.get("https://drones-api.hive.fi/drones")
	if res.status_code != 200:
		# log error
		return HTTPException(500, "Internal server error")

	try:
		body = res.json()
	except:
		# log error
		return HTTPException(500, "Internal server error")

	drones = violated_drones(body)
	if len(drones):
		print("violation detected")
		#update db
	return body