from fastapi import APIRouter, Request, HTTPException
from utils.nfz import authenticate
import os
import psycopg

nfz_route = APIRouter()

@nfz_route.get("/nfz")
def nfz(req: Request):
	authenticated = authenticate(req.headers.get("X-Secret"))
	if not authenticated:
		return HTTPException(401, "Unauthorized")

	list = retrieve_nfz_list()
	
	if list is None:
		return HTTPException(204, "No content")

	return list


def retrieve_nfz_list():
	connection_string = (
		f"host=localhost port=5432 "
		f"dbname={os.getenv('DB_NAME')} "
		f"user={os.getenv('DB_USER')} "
		f"password={os.getenv('DB_PASSWORD')}"
		)
	
	with psycopg.connect(connection_string) as conn:
		with conn.cursor() as cur:
			list = cur.fetchall()
	
	return list